import json
import logging
import os
import urllib.error
import urllib.request

import boto3

_SUPPORTED = ("azure", "aws", "gcp")


class VerifyError(Exception):
    def __init__(self, status, message, extra=None):
        super().__init__(message)
        self.status = status
        self.message = message
        self.extra = extra or {}


def _upstream_detail(raw):
    text = (raw or "").strip()
    if not text:
        return ""
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return text[:500]
    if isinstance(parsed, dict):
        detail = parsed.get("detail") or parsed.get("message") or parsed.get("error") or text
        if not isinstance(detail, str):
            detail = json.dumps(detail)
        return detail[:500]
    return text[:500]


def _ssm(name):
    return boto3.client("ssm").get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]


def _config(cloud):
    normalized = cloud.strip().lower()
    if normalized not in _SUPPORTED:
        raise ValueError(
            f"Unsupported cloud provider: '{cloud}'. Supported providers: azure, aws, gcp."
        )
    env = normalized.upper()
    return _ssm(os.environ[f"SSM_VERIFY_{env}_URL"]), _ssm(os.environ[f"SSM_VERIFY_{env}_KEY"])


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
        raw = err.read().decode(errors="replace")
        detail = _upstream_detail(raw)
        logging.warning(
            "Verify service returned status %s for cloud '%s', lab '%s': %s",
            err.code,
            cloud,
            lab,
            detail or raw[:500],
        )
        extra = {
            "cloud": cloud.strip().lower(),
            "lab": lab,
            "upstream_status": err.code,
        }
        if detail:
            extra["upstream"] = detail
        if 400 <= err.code < 500:
            msg = f"Verify {cloud} / {lab} failed ({err.code})"
            if detail:
                msg = f"{msg}: {detail}"
            raise VerifyError(err.code, msg, extra)
        msg = f"Verify {cloud} / {lab} unavailable ({err.code})"
        if detail:
            msg = f"{msg}: {detail}"
        raise VerifyError(502, msg, extra)
    except urllib.error.URLError as err:
        reason = getattr(err, "reason", err)
        logging.error("Verify service communication error for %s / %s: %s", cloud, lab, reason)
        raise VerifyError(
            502,
            f"Verify {cloud} / {lab} unreachable: {reason}",
            extra={"cloud": cloud.strip().lower(), "lab": lab},
        )
