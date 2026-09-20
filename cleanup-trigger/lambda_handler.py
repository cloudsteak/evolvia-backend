import json
import logging
import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

import boto3

from labs import delete_lab, scan_labs

logging.basicConfig(level=logging.INFO)
_PLACEHOLDER = "replace-me"


def is_expired(lab):
    status = lab.get("status", "ready")
    timestamp_str = lab.get("started_at") if status == "ready" else lab.get("error_at")
    if not timestamp_str:
        timestamp_str = lab.get("created_at")
    if not timestamp_str:
        return False

    ttl_seconds = int(lab.get("lab_ttl") or 5400)
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
    except ValueError:
        logging.error("Invalid timestamp for %s: %s", lab.get("username"), timestamp_str)
        return False

    now = datetime.now(timezone.utc)
    if status == "ready":
        expiry = timestamp + timedelta(seconds=ttl_seconds)
    elif status == "pending":
        expiry = timestamp + timedelta(seconds=7200)
    else:
        expiry = timestamp + timedelta(seconds=14400)
    return now >= expiry


def _github_token():
    name = os.environ["GITHUB_TOKEN_PATH"]
    resp = boto3.client("ssm").get_parameter(Name=name, WithDecryption=True)
    value = resp["Parameter"]["Value"]
    if not value or value == _PLACEHOLDER:
        raise RuntimeError("GitHub token is missing or still replace-me")
    return value


def _destroy(lab, token):
    repo = os.environ["GITHUB_REPO"]
    workflow = f"{lab.get('cloud_provider') or 'aws'}{os.environ['GITHUB_WORKFLOW_FILENAME']}"
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow}/dispatches"
    body = json.dumps(
        {
            "ref": "main",
            "inputs": {
                "lab": lab["lab_name"],
                "action": "destroy",
                "student_username": lab["username"],
                "student_password": "dummy",
            },
        }
    ).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return 200 <= resp.status < 300
    except urllib.error.HTTPError as err:
        logging.error(
            "GitHub destroy failed for %s: %s %s",
            lab.get("username"),
            err.code,
            err.read().decode()[:500],
        )
        return False


def cleanup_expired_labs():
    token = _github_token()
    cleaned = []
    for lab in scan_labs():
        username = lab.get("username")
        if not username or not is_expired(lab):
            continue
        logging.info("Expired lab %s status=%s", username, lab.get("status"))
        if not lab.get("lab_name"):
            logging.warning("Incomplete lab %s — skip", username)
            continue
        if not _destroy(lab, token):
            continue
        if delete_lab(username):
            logging.info("Deleted DynamoDB item %s", username)
            cleaned.append(username)
    return cleaned


def handler(event, context):
    cleaned = cleanup_expired_labs()
    return {"cleaned": cleaned}
