# cleanup_trigger.py
# This script checks for expired labs and triggers their cleanup.


import logging
import os
from datetime import datetime, timedelta, timezone

import httpx

BACKEND_URL = os.getenv("BACKEND_URL")
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")

LAB_STATUS_ENDPOINT = f"{BACKEND_URL}/lab-status/all"
CLEANUP_ENDPOINT = f"{BACKEND_URL}/clean-up-lab"
DELETE_REDIS_ENDPOINT = f"{BACKEND_URL}/lab-delete-internal"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
TIMEOUT = 30  # seconds
HEADERS = {"X-Internal-Secret": INTERNAL_SECRET}

def is_expired(lab):
    status = lab.get("status", "ready")
    
    # Priority: started_at (ready) > error_at (failed) > created_at (pending/fallback)
    timestamp_str = lab.get("started_at") if status == "ready" else lab.get("error_at")
    if not timestamp_str:
        timestamp_str = lab.get("created_at")

    ttl_seconds = lab.get("lab_ttl", 5400)  # Default TTL is 5400 seconds (1.5 hours)
    
    if not timestamp_str:
        logger.debug(f"No timestamp found for lab {lab.get('username')} with status {status}")
        return False

    try:
        timestamp = datetime.fromisoformat(timestamp_str).replace(tzinfo=timezone.utc)
    except (TypeError, ValueError) as e:
        logger.error(f"Invalid timestamp for {lab.get('username')}: {timestamp_str} - {e}")
        return False

    now = datetime.now(timezone.utc)

    if status == "ready":
        expiry_time = timestamp + timedelta(seconds=ttl_seconds)
    elif status == "failed":
        expiry_time = timestamp + timedelta(seconds=14400) # 4 hours for failed labs
    elif status == "pending":
        expiry_time = timestamp + timedelta(seconds=7200) # 2 hours for stuck pending labs
    else:
        # For other unknown statuses, use a safe default of 4 hours
        expiry_time = timestamp + timedelta(seconds=14400)

    return now >= expiry_time

def cleanup_expired_labs():
    if not BACKEND_URL:
        logger.error("BACKEND_URL environment variable is not set")
        return

    try:
        response = httpx.get(LAB_STATUS_ENDPOINT, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except httpx.ConnectError as e:
        logger.error(f"❌ Connection Error: Could not resolve or connect to backend at {BACKEND_URL}. Check K8s service name and DNS. Error: {e}")
        return
    except httpx.HTTPStatusError as e:
        logger.error(f"❌ HTTP Error: Backend returned {e.response.status_code} for {LAB_STATUS_ENDPOINT}")
        return
    except httpx.RequestError as e:
        logger.error(f"❌ Unexpected Error: {e}")
        return

    labs_data = response.json()
    labs = labs_data.get("labs", [])

    if not isinstance(labs, list):
        logger.error("Invalid response format: %s", labs_data)
        return

    for lab in labs:
        username = lab.get("username")
        logger.info(f"User: {username} - Lab started:{lab.get('started_at')}")
        if is_expired(lab):
            logger.info(f"[EXPIRED] Cleaning up lab {username} (status: {lab.get('status')})")
            res = httpx.post(CLEANUP_ENDPOINT, headers=HEADERS, json={"username": username}, timeout=TIMEOUT)
            if res.status_code == 200:
                logger.info(f"✔️ Lab {username} cleaned up")

                # Delete Redis record after cleanup
                del_res = httpx.post(DELETE_REDIS_ENDPOINT, headers=HEADERS, json={"username": username}, timeout=TIMEOUT)
                if del_res.status_code == 200:
                    logger.info(f"🗑️ Deleted Redis key for {username}")
                else:
                    logger.warning(f"⚠️ Failed to delete Redis key for {username}: {del_res.status_code} {del_res.text}")
            else:
                logger.warning(f"⚠️ Failed to clean up lab {username}: {res.status_code} {res.text}")
        else:
            logger.debug(f"[ACTIVE] Skipping lab {username}, still within TTL")

if __name__ == "__main__":
    cleanup_expired_labs()
