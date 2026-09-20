import json
import logging
import os
import urllib.error
import urllib.request

import boto3

_PLACEHOLDER = "replace-me"
_SUPPORTED = ("azure", "aws", "gcp")
_params = {}


class VerifyError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def _ssm(name):
    if name not in _params:
        value = boto3.client("ssm").get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]
        if not value or value == _PLACEHOLDER:
            raise RuntimeError(f"SSM {name} is missing or still replace-me")
        _params[name] = value
    return _params[name]


def _config(cloud):
    normalized = cloud.strip().lower()
    if normalized not in _SUPPORTED:
        raise ValueError(
            f"Unsupported cloud provider: '{cloud}'. Supported providers: azure, aws, gcp."
        )
    base = os.environ["VERIFY_PATH"]
    return _ssm(f"{base}/{normalized}/url"), _ssm(f"{base}/{normalized}/key")


def verify_lab(user, email, cloud, lab):
    url, api_key = _config(cloud)
    body = json.dumps(
        {
            "user": user,
            "email": email,
            "cloud": cloud.strip().lower(),
            "lab": lab,
        }
    ).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "X-API-Key": api_key,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=50) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as err:
        upstream = err.code
        err.read()
        logging.warning(
            "Verify service returned status %s for cloud '%s', lab '%s'.",
            upstream,
            cloud,
            lab,
        )
        if 400 <= upstream < 500:
            raise VerifyError(upstream, "Verify request failed.")
        raise VerifyError(502, "Verify service is temporarily unavailable.")
    except urllib.error.URLError as err:
        logging.error("Verify service communication error: %s", err)
        raise VerifyError(502, "Verify service is temporarily unavailable.")
