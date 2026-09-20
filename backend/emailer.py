import html
import logging
import os
from pathlib import Path

import boto3

_SUBJECT = "[Evolvia] - A labor környezeted elkészült!"
_TEMPLATE = Path(__file__).with_name("lab_ready_default.html")
_IF_START = "{% if ttl_minutes > 0 %}"
_IF_END = "{% endif %}"
_PLACEHOLDER = "replace-me"
_params = {}


def _ssm(name):
    if name not in _params:
        value = boto3.client("ssm").get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]
        if not value or value == _PLACEHOLDER:
            raise RuntimeError(f"SSM {name} is missing or still replace-me")
        _params[name] = value
    return _params[name]


def _portal(cloud_provider):
    if (cloud_provider or "").lower() == "azure":
        return _ssm(os.environ["PORTAL_AZURE_URL_PATH"])
    return _ssm(os.environ["PORTAL_AWS_URL_PATH"])


def _username(username, cloud_provider):
    if (cloud_provider or "").lower() == "azure":
        return f"{username}@evolvia.hu"
    return username


def _render(username, password, cloud_provider, ttl_seconds):
    ttl_minutes = int(ttl_seconds) // 60 if ttl_seconds else 0
    text = _TEMPLATE.read_text(encoding="utf-8")
    start = text.find(_IF_START)
    end = text.find(_IF_END)
    if start != -1 and end != -1:
        inner = text[start + len(_IF_START) : end]
        text = text[:start] + (inner if ttl_minutes > 0 else "") + text[end + len(_IF_END) :]
    replacements = {
        "{{ username }}": html.escape(username),
        "{{ password }}": html.escape(password),
        "{{ cloud_console_url }}": html.escape(_portal(cloud_provider), quote=True),
        "{{ ttl_minutes }}": str(ttl_minutes),
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def send_lab_ready_email(username, password, recipient, cloud_provider, ttl_seconds):
    if not recipient:
        logging.warning("lab-ready email skipped: no recipient for %s", username)
        return
    source = os.environ["SES_FROM_ADDRESS"]
    body = _render(
        _username(username, cloud_provider),
        password,
        cloud_provider,
        ttl_seconds,
    )
    boto3.client("ses").send_email(
        Source=f"Evolvia <{source}>",
        Destination={"ToAddresses": [recipient]},
        Message={
            "Subject": {"Data": _SUBJECT, "Charset": "UTF-8"},
            "Body": {"Html": {"Data": body, "Charset": "UTF-8"}},
        },
    )
    logging.debug("lab-ready email sent to %s", recipient)
