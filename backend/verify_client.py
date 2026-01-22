import httpx
from config import Settings


def verify_lab(
    settings: Settings,
    user: str,
    email: str,
    cloud: str,
    lab: str,
) -> dict:
    url = f"{settings.verify_lab_host}{settings.verify_lab_path}"
    headers = {"X-API-Key": settings.internal_verify_api_key}
    payload = {
        "user": user,
        "email": email,
        "cloud": cloud,
        "lab": lab,
    }

    response = httpx.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()
