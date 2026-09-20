# --- backend/main.py ---

import logging
from datetime import datetime

import httpx
import requests
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from config import get_settings
from emailer import send_lab_ready_email
from labs import delete_lab, get_lab, put_lab, scan_labs
from models import (
    LabDeleteRequest,
    LabReadyRequest,
    LabRequest,
    VerifyLabRequest,
    status_map,
)
from utils import generate_credentials, get_rsa_key
from verify_client import verify_lab

settings = get_settings()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=settings.log_level, format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI(docs_url="/docs", redoc_url=None)
security = HTTPBearer()


async def trigger_github_workflow(
    username: str,
    password: str,
    lab: str = "basic",
    action: str = "apply",
    cloud_provider: str = "aws",
):
    repo = settings.github_repo
    workflow_filename = cloud_provider + settings.github_workflow_filename
    github_token = settings.github_token

    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_filename}/dispatches"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
    }
    json_data = {
        "ref": "main",
        "inputs": {
            "lab": lab,
            "action": action,
            "student_username": username,
            "student_password": password,
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json_data)
        if response.status_code >= 300:
            raise HTTPException(
                status_code=500, detail=f"Failed to trigger workflow: {response.text}"
            )


# --- Internal secret validation ---
def verify_internal_secret(x_internal_secret: str = Header(...)):
    if not settings.internal_secret:
        raise HTTPException(status_code=500, detail="INTERNAL_SECRET not configured")
    if x_internal_secret != settings.internal_secret:
        raise HTTPException(
            status_code=403, detail="Forbidden: Invalid internal secret"
        )


# --- Auth0 validation ---
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        rsa_key = get_rsa_key(token)
        payload = jwt.decode(
            token,
            key=rsa_key,
            audience=settings.auth0_audience,
            issuer=f"https://{settings.auth0_domain}/",
            algorithms=[settings.auth0_algorithms],
        )
        return payload
    except JWTError as e:
        logger.error(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


# Permission check helper
def has_permission(token: dict, required: str):
    permissions = token.get("permissions", [])
    if required not in permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing required permission: {required}",
        )


# --- Endpoints ---
@app.get("/")
def root():
    return {"message": "Student Lab Backend API is up and running"}


@app.post("/start-lab")
async def start_lab(request: LabRequest, token: dict = Depends(verify_token)):
    has_permission(token, "create:lab")
    username, password = generate_credentials()

    lab_data = {
        "lab_name": request.lab_name,
        "cloud_provider": request.cloud_provider,
        "lab_ttl": request.lab_ttl,
        "username": username,
        "password": password,
        "email": request.email,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
    }

    logger.info(f"Storing lab data for {username} in DynamoDB")
    put_lab(lab_data)

    # Trigger GitHub Actions - Apply
    await trigger_github_workflow(
        username=username,
        password=password,
        lab=request.lab_name,
        action="apply",
        cloud_provider=request.cloud_provider,
    )

    return {
        "message": "Lab creation is in progress",
        "username": username,
        "password": password,
    }


@app.get("/lab-status/all")
def lab_status_all(_: str = Depends(verify_internal_secret)):
    return JSONResponse(content={"labs": scan_labs()})


@app.post("/lab-ready")
async def lab_ready(request: LabReadyRequest, token: dict = Depends(verify_token)):
    has_permission(token, "notify:lab")
    username = request.username
    status_value = request.status.lower()

    lab_data = get_lab(username)
    if not lab_data:
        raise HTTPException(status_code=404, detail="Lab not found")

    if lab_data.get("status") == "ready":
        return {"message": "Lab already marked as ready"}

    now = datetime.utcnow().isoformat()

    if status_value != "ready":
        lab_data["status"] = status_value
        lab_data["error_at"] = now
        put_lab(lab_data)

        # WordPress webhook küldés hibás státusz esetén is
        if settings.wordpress_webhook_url and settings.wordpress_secret_key:
            logger.info("Sending webhook to WordPress - error case")
            webhook_url = f"{settings.wordpress_webhook_url}?secret_key={settings.wordpress_secret_key}"
            webhook_status = status_map.get(status_value, "pending")

            # Generate lab_id from cloud and lab_name
            cloud = lab_data.get("cloud_provider", "").strip().lower()
            name = lab_data.get("lab_name", "").strip().lower()
            lab_id = f"{cloud}-{name}" if cloud and name else "unknown"

            logger.info(
                f"Lab info for {lab_data.get('email')}: {lab_id} - {webhook_status} - status_map.get(status_value, 'pending')"
            )
            logger.info(f"WordPress webhook URL: {settings.wordpress_webhook_url}")
            payload = {
                "email": lab_data.get("email"),
                "lab_id": lab_id,
                "status": webhook_status,
            }
            try:
                response = requests.post(webhook_url, json=payload)
                response.raise_for_status()
            except requests.RequestException as e:
                logger.warning(f"Failed to call WordPress webhook: {e!s}")

        return {"message": f"Lab {username} reported status: {status_value}"}

    # success case (status_value == "ready")
    lab_data["status"] = "ready"
    lab_data["started_at"] = now

    send_lab_ready_email(
        username,
        lab_data["password"],
        lab_data["email"],
        lab_data["cloud_provider"],
        lab_data["lab_ttl"],
    )
    put_lab(lab_data)

    # WordPress webhook hívása ready esetén
    if settings.wordpress_webhook_url and settings.wordpress_secret_key:
        logger.info("Sending webhook to WordPress - error case")
        webhook_url = f"{settings.wordpress_webhook_url}?secret_key={settings.wordpress_secret_key}"
        webhook_status = status_map.get("ready", "pending")

        # Generate lab_id from cloud and lab_name
        cloud = lab_data.get("cloud_provider", "").strip().lower()
        name = lab_data.get("lab_name", "").strip().lower()
        lab_id = f"{cloud}-{name}" if cloud and name else "unknown"

        logger.info(
            f"Lab info for {lab_data.get('email')}: {lab_id} - {webhook_status} - status_map.get('ready', 'pending')"
        )
        logger.info(f"WordPress webhook URL: {settings.wordpress_webhook_url}")

        payload = {
            "email": lab_data.get("email"),
            "lab_id": lab_id,
            "status": webhook_status,
        }
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(f"Failed to call WordPress webhook: {e!s}")

    return {
        "message": f"Lab {username} marked as ready, email sent, WordPress notified"
    }


@app.post("/lab-delete-internal")
def delete_lab_internal(
    request: LabDeleteRequest, _: str = Depends(verify_internal_secret)
):

    if delete_lab(request.username):
        logger.info(f"Lab '{request.username}' deleted")
        return {"message": f"Lab '{request.username}' deleted"}

    logger.warning(f"Lab '{request.username}' not found")
    raise HTTPException(status_code=404, detail=f"Lab '{request.username}' not found")


@app.post("/clean-up-lab")
async def clean_up_lab(
    request: LabDeleteRequest, _: str = Depends(verify_internal_secret)
):
    lab = get_lab(request.username)
    if not lab:
        logger.warning(f"Lab data not found for {request.username}")
        raise HTTPException(status_code=404, detail="Lab not found")

    if "password" not in lab or "lab_name" not in lab:
        logger.warning(f"Lab data is incomplete for {request.username}")
        raise HTTPException(status_code=500, detail="Lab data is incomplete")

    await trigger_github_workflow(
        username=request.username,
        password="dummy",
        lab=lab["lab_name"],
        action="destroy",
        cloud_provider=lab["cloud_provider"],
    )

    logger.info(f"Triggered destroy action for {request.username}")
    return {"message": f"Destroy action triggered for {request.username}"}


@app.post("/verify-lab")
def verify_lab_endpoint(request: VerifyLabRequest, token: dict = Depends(verify_token)):
    has_permission(token, "verify:lab")

    try:
        result = verify_lab(
            settings=settings,
            user=request.user,
            email=request.email,
            cloud=request.cloud,
            lab=request.lab,
        )
        return result
    except ValueError as error:
        logger.warning("Invalid verify-lab request: %s", error)
        raise HTTPException(status_code=400, detail="Invalid verify-lab request.")
    except httpx.HTTPStatusError as error:
        upstream_status = error.response.status_code
        logger.warning(
            "Verify service returned status %s for cloud '%s', lab '%s'.",
            upstream_status,
            request.cloud,
            request.lab,
        )
        if 400 <= upstream_status < 500:
            raise HTTPException(status_code=upstream_status, detail="Verify request failed.")
        raise HTTPException(
            status_code=502, detail="Verify service is temporarily unavailable."
        )
    except httpx.HTTPError as error:
        logger.error("Verify service communication error: %s", error)
        raise HTTPException(
            status_code=502, detail="Verify service is temporarily unavailable."
        )
    except Exception:
        logger.exception("Unexpected error while processing verify-lab request.")
        raise HTTPException(status_code=500, detail="Unexpected server error.")
