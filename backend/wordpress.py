import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request

import boto3

_STATUS = {"ready": "success", "failed": "error"}


def _ssm(name):
    return boto3.client("ssm").get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]


def notify(lab, status_value):
    url_name = os.environ.get("SSM_WORDPRESS_WEBHOOK_URL")
    token_name = os.environ.get("SSM_WORDPRESS_WEBHOOK_TOKEN")
    if not url_name or not token_name:
        return
    try:
        base = _ssm(url_name)
        token = _ssm(token_name)
    except Exception:
        logging.warning("WordPress webhook skipped: SSM url/token missing")
        return

    cloud = (lab.get("cloud_provider") or "").strip().lower()
    name = (lab.get("lab_name") or "").strip().lower()
    lab_id = f"{cloud}-{name}" if cloud and name else "unknown"
    webhook_status = _STATUS.get(status_value, "pending")
    url = f"{base}?{urllib.parse.urlencode({'secret_key': token})}"
    body = json.dumps(
        {
            "email": lab.get("email"),
            "lab_id": lab_id,
            "status": webhook_status,
        }
    ).encode()
    logging.info("WordPress webhook %s %s", lab.get("email"), lab_id)
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError) as err:
        logging.warning("Failed to call WordPress webhook: %s", err)
