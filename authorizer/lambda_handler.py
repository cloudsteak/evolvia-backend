import logging
import os

import boto3

_level = getattr(logging, (os.getenv("LOG_LEVEL") or "INFO").upper(), logging.INFO)
logging.basicConfig(level=_level)
logging.getLogger().setLevel(_level)

_PLACEHOLDER = "replace-me"
_keys = None


def _load_keys():
    global _keys
    if _keys is not None:
        return _keys

    path = os.environ["API_KEYS_PATH"]
    resp = boto3.client("ssm").get_parameters_by_path(
        Path=path,
        Recursive=True,
        WithDecryption=True,
    )
    _keys = {
        item["Value"]
        for item in resp.get("Parameters", [])
        if item.get("Value") and item["Value"] != _PLACEHOLDER
    }
    return _keys


def _api_key(event):
    headers = event.get("headers") or {}
    for name, value in headers.items():
        if name.lower() == "x-api-key":
            return (value or "").strip()

    sources = event.get("identitySource") or []
    if sources:
        return (sources[0] or "").strip()
    return ""


def handler(event, context):
    key = _api_key(event)
    authorized = bool(key) and key in _load_keys()
    if authorized:
        logging.debug("authorized")
    else:
        logging.info("unauthorized")
    return {"isAuthorized": authorized}
