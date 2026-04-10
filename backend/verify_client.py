import httpx
from config import Settings


def _get_verify_service_config(settings: Settings, cloud: str) -> tuple[str, str]:
    normalized_cloud = cloud.strip().lower()

    if normalized_cloud == "azure":
        return (
            f"{settings.verify_lab_azure_host}{settings.verify_lab_azure_path}",
            settings.internal_verify_azure_api_key,
        )
    if normalized_cloud == "aws":
        return (
            f"{settings.verify_lab_aws_host}{settings.verify_lab_aws_path}",
            settings.internal_verify_aws_api_key,
        )
    if normalized_cloud == "gcp":
        return (
            f"{settings.verify_lab_gcp_host}{settings.verify_lab_gcp_path}",
            settings.internal_verify_gcp_api_key,
        )

    raise ValueError(
        f"Unsupported cloud provider: '{cloud}'. Supported providers: azure, aws, gcp."
    )


def verify_lab(
    settings: Settings,
    user: str,
    email: str,
    cloud: str,
    lab: str,
) -> dict:
    url, api_key = _get_verify_service_config(settings=settings, cloud=cloud)
    headers = {"X-API-Key": api_key}
    payload = {
        "user": user,
        "email": email,
        "cloud": cloud.strip().lower(),
        "lab": lab,
    }

    response = httpx.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()
