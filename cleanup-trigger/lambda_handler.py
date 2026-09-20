import json
import logging
import os
from datetime import datetime, timedelta, timezone

import boto3

logger = logging.getLogger(__name__)
_level = getattr(logging, (os.getenv("LOG_LEVEL") or "INFO").upper(), logging.INFO)
logging.basicConfig(level=_level)
logger.setLevel(_level)

TIMEOUT = 30


def is_expired(lab):
    status = lab.get("status", "ready")

    # Priority: started_at (ready) > error_at (failed) > created_at (pending/fallback)
    timestamp_str = lab.get("started_at") if status == "ready" else lab.get("error_at")
    if not timestamp_str:
        timestamp_str = lab.get("created_at")

    ttl_seconds = lab.get("lab_ttl", 5400)

    if not timestamp_str:
        logger.debug("No timestamp found for lab %s with status %s", lab.get("username"), status)
        return False

    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError) as e:
        logger.error("Invalid timestamp for %s: %s - %s", lab.get("username"), timestamp_str, e)
        return False

    now = datetime.now(timezone.utc)

    if status == "ready":
        expiry_time = timestamp + timedelta(seconds=ttl_seconds)
    elif status == "failed":
        expiry_time = timestamp + timedelta(seconds=14400)
    elif status == "pending":
        expiry_time = timestamp + timedelta(seconds=7200)
    else:
        expiry_time = timestamp + timedelta(seconds=14400)

    return now >= expiry_time


def _invoke(route, body=None):
    payload = {"routeKey": route}
    if body is not None:
        payload["body"] = json.dumps(body)
    resp = boto3.client("lambda").invoke(
        FunctionName=os.environ["BACKEND_FUNCTION_NAME"],
        Qualifier=os.environ["BACKEND_ALIAS"],
        Payload=json.dumps(payload).encode(),
    )
    return json.loads(resp["Payload"].read().decode() or "{}")


def cleanup_expired_labs():
    listing = _invoke("GET /lab-status/all")
    status = listing.get("statusCode", 500)
    if status >= 400:
        logger.error("HTTP Error: Backend returned %s for /lab-status/all", status)
        return

    try:
        labs_data = json.loads(listing.get("body") or "{}")
    except json.JSONDecodeError as e:
        logger.error("Unexpected Error: %s", e)
        return

    labs = labs_data.get("labs", [])
    if not isinstance(labs, list):
        logger.error("Invalid response format: %s", labs_data)
        return

    for lab in labs:
        username = lab.get("username")
        logger.info("User: %s - Lab started:%s", username, lab.get("started_at"))
        if is_expired(lab):
            logger.info("[EXPIRED] Cleaning up lab %s (status: %s)", username, lab.get("status"))
            res = _invoke("POST /clean-up-lab", {"username": username})
            if res.get("statusCode") == 200:
                logger.info("Lab %s cleaned up", username)
                del_res = _invoke("POST /lab-delete-internal", {"username": username})
                if del_res.get("statusCode") == 200:
                    logger.info("Deleted lab record for %s", username)
                else:
                    logger.warning(
                        "Failed to delete lab %s: %s %s",
                        username,
                        del_res.get("statusCode"),
                        del_res.get("body"),
                    )
            else:
                logger.warning(
                    "Failed to clean up lab %s: %s %s",
                    username,
                    res.get("statusCode"),
                    res.get("body"),
                )
        else:
            logger.debug("[ACTIVE] Skipping lab %s, still within TTL", username)


def handler(event, context):
    cleanup_expired_labs()
