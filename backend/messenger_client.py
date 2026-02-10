import httpx
from config import Settings


def send_lab_ready_email(
    settings: Settings,
    username: str,
    password: str,
    recipient: str,
    cloud_provider: str,
    ttl_seconds: int,
) -> dict:
    url = f"{settings.messenger_host}{settings.messenger_path}"
    headers = {"X-API-Key": settings.internal_messenger_api_key}
    payload = {
        "template": settings.messenger_template,
        "recipient": recipient,
        "subject": "[Evolvia] - A labor környezeted elkészült!",
        "username": username,
        "password": password,
        "cloud_provider": cloud_provider,
        "ttl_seconds": ttl_seconds,
    }

    response = httpx.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
