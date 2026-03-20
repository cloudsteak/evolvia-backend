# cleanup_trigger.py
# This script checks for expired labs and triggers their cleanup.


import os
import httpx
import logging
from datetime import datetime, timedelta, timezone

BACKEND_URL = os.getenv("BACKEND_URL")
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")

LAB_STATUS_ENDPOINT = f"{BACKEND_URL}/lab-status/all"
CLEANUP_ENDPOINT = f"{BACKEND_URL}/clean-up-lab"
DELETE_REDIS_ENDPOINT = f"{BACKEND_URL}/lab-delete-internal"

logging.basicConfig(level=logging.INFO)
TIMEOUT = 30  # seconds
HEADERS = {"X-Internal-Secret": INTERNAL_SECRET}

def is_expired(lab):
    status = lab.get("status", "ready")
    
    # Use started_at for ready labs, error_at for failed labs
    timestamp_str = lab.get("started_at") if status == "ready" else lab.get("error_at")
    ttl_seconds = lab.get("lab_ttl", 5400)  # Default TTL is 5400 seconds (1.5 hours)
    
    if not timestamp_str:
        logging.debug(f"No timestamp found for lab {lab.get('username')} with status {status}")
        return False

    try:
        timestamp = datetime.fromisoformat(timestamp_str).replace(tzinfo=timezone.utc)
    except Exception as e:
        logging.error(f"Invalid timestamp for {lab.get('username')}: {timestamp_str} - {e}")
        return False

    now = datetime.now(timezone.utc)

    if status == "ready":
        expiry_time = timestamp + timedelta(seconds=ttl_seconds)
    elif status == "failed":
        expiry_time = timestamp + timedelta(seconds=14400) # 4 hours for failed labs
    else:
        # For other statuses (e.g. pending), we don't have a specific expiry yet
        return False

    return now >= expiry_time

def cleanup_expired_labs():
    response = httpx.get(LAB_STATUS_ENDPOINT, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    labs_data = response.json()
    labs = labs_data.get("labs", [])

    if not isinstance(labs, list):
        logging.error("Invalid response format: %s", labs_data)
        return

    for lab in labs:
        username = lab.get("username")
        logging.info(f"User: {username} - Lab started:{lab.get('started_at')}")
        if is_expired(lab):
            logging.info(f"[EXPIRED] Cleaning up lab {username} (status: {lab.get('status')})")
            res = httpx.post(CLEANUP_ENDPOINT, headers=HEADERS, json={"username": username}, timeout=TIMEOUT)
            if res.status_code == 200:
                logging.info(f"✔️ Lab {username} cleaned up")

                # Delete Redis record after cleanup
                del_res = httpx.post(DELETE_REDIS_ENDPOINT, headers=HEADERS, json={"username": username}, timeout=TIMEOUT)
                if del_res.status_code == 200:
                    logging.info(f"🗑️ Deleted Redis key for {username}")
                else:
                    logging.warning(f"⚠️ Failed to delete Redis key for {username}: {del_res.status_code} {del_res.text}")
            else:
                logging.warning(f"⚠️ Failed to clean up lab {username}: {res.status_code} {res.text}")
        else:
            logging.debug(f"[ACTIVE] Skipping lab {username}, still within TTL")

if __name__ == "__main__":
    cleanup_expired_labs()
