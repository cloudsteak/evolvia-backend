import logging
import os
from pathlib import Path
from types import SimpleNamespace

import boto3
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)
_ALLOWED_TEMPLATES = {"lab_ready_default"}
_SUBJECT = "[Evolvia] - A labor környezeted elkészült!"


class TemplateNotFoundError(Exception):
    pass


def _ssm(name):
    return boto3.client("ssm").get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]


def _settings():
    return SimpleNamespace(
        portal_azure_url=_ssm(os.environ["SSM_PORTAL_AZURE_URL"]),
        portal_aws_url=_ssm(os.environ["SSM_PORTAL_AWS_URL"]),
        email_sender=os.environ["SES_FROM_ADDRESS"],
        sender_name="Cloud Mentor",
    )


def _jinja_env() -> Environment:
    templates_dir = Path(__file__).parent / "templates"
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )


def render_template(template_name: str, context: dict) -> str:
    if template_name not in _ALLOWED_TEMPLATES:
        raise TemplateNotFoundError(f"Template not allowed: {template_name}")

    env = _jinja_env()
    filename = f"{template_name}.html"

    try:
        template = env.get_template(filename)
    except Exception as e:
        raise TemplateNotFoundError(f"Template not found: {filename}") from e

    return template.render(**context)


def build_lab_ready_context(
    settings,
    username: str,
    password: str,
    cloud_provider: str,
    ttl_seconds: int,
) -> dict:
    if cloud_provider == "azure":
        cloud_console_url = settings.portal_azure_url
        effective_username = f"{username}@evolvia.hu"
    else:
        cloud_console_url = settings.portal_aws_url
        effective_username = username

    ttl_minutes = int(ttl_seconds / 60) if ttl_seconds else 0

    return {
        "cloud_console_url": cloud_console_url,
        "username": effective_username,
        "password": password,
        "ttl_minutes": ttl_minutes,
        "cloud_provider": cloud_provider,
    }


def send_lab_ready_email(username, password, recipient, cloud_provider, ttl_seconds):
    if not recipient:
        logger.warning("lab-ready email skipped: no recipient for %s", username)
        return
    settings = _settings()
    html_content = render_template(
        "lab_ready_default",
        build_lab_ready_context(
            settings=settings,
            username=username,
            password=password,
            cloud_provider=cloud_provider,
            ttl_seconds=ttl_seconds,
        ),
    )
    boto3.client("ses").send_email(
        Source=f"{settings.sender_name} <{settings.email_sender}>",
        Destination={"ToAddresses": [recipient]},
        Message={
            "Subject": {"Data": _SUBJECT, "Charset": "UTF-8"},
            "Body": {"Html": {"Data": html_content, "Charset": "UTF-8"}},
        },
    )
    logger.debug("lab-ready email sent to %s", recipient)
