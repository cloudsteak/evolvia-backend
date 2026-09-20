import json
import logging
import os
from datetime import datetime, timezone

from credentials import generate_credentials
from emailer import send_lab_ready_email
from github import dispatch
from labs import delete_lab, get_lab, put_lab, scan_labs
from verify_client import VerifyError, verify_lab
from wordpress import notify as notify_wordpress

_level = getattr(logging, (os.getenv("LOG_LEVEL") or "INFO").upper(), logging.INFO)
logging.basicConfig(level=_level)
logging.getLogger().setLevel(_level)


def _route_key(event):
    if event.get("routeKey"):
        return event["routeKey"]
    rc = event.get("requestContext") or {}
    http = rc.get("http") or {}
    method = http.get("method") or event.get("httpMethod") or "GET"
    path = event.get("rawPath") or event.get("path") or http.get("path") or "/"
    return f"{method} {path.rstrip('/') or '/'}"


def _json(status, body):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def _body(event):
    raw = event.get("body") or ""
    if event.get("isBase64Encoded"):
        import base64

        raw = base64.b64decode(raw).decode()
    if not raw:
        return {}
    return json.loads(raw)


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None).isoformat()


def _start_lab(payload):
    username, password = generate_credentials()
    item = {
        "username": username,
        "password": password,
        "lab_name": payload.get("lab_name"),
        "cloud_provider": payload.get("cloud_provider"),
        "email": payload.get("email"),
        "lab_ttl": int(payload.get("lab_ttl") or 5400),
        "status": "pending",
        "created_at": _now(),
    }
    logging.info("Storing lab data for %s in DynamoDB", username)
    put_lab(item)
    if not dispatch(item, "apply", password=password):
        return _json(500, {"message": "Failed to trigger workflow"})
    return _json(
        200,
        {
            "message": "Lab creation is in progress",
            "username": username,
            "password": password,
        },
    )


def _lab_ready(payload):
    username = (payload.get("username") or "").strip()
    status_value = (payload.get("status") or "").lower()
    lab = get_lab(username)
    if not lab:
        return _json(404, {"message": "Lab not found"})
    if lab.get("status") == "ready":
        return _json(200, {"message": "Lab already marked as ready"})

    now = _now()
    if status_value != "ready":
        lab["status"] = status_value
        lab["error_at"] = now
        put_lab(lab)
        notify_wordpress(lab, status_value)
        return _json(200, {"message": f"Lab {username} reported status: {status_value}"})

    try:
        send_lab_ready_email(
            username,
            lab.get("password") or "",
            lab.get("email") or "",
            lab.get("cloud_provider") or "aws",
            int(lab.get("lab_ttl") or 0),
        )
    except Exception:
        logging.exception("SES send failed for %s", username)
        return _json(500, {"message": "Failed to send lab-ready email"})

    lab["status"] = "ready"
    lab["started_at"] = now
    put_lab(lab)
    notify_wordpress(lab, "ready")
    return _json(200, {"message": f"Lab {username} marked as ready"})


def _verify_lab(payload):
    user = (payload.get("user") or "").strip()
    email = (payload.get("email") or "").strip()
    cloud = (payload.get("cloud") or "").strip()
    lab = (payload.get("lab") or "").strip()
    if not all((user, email, cloud, lab)):
        return _json(400, {"message": "Invalid verify-lab request."})
    try:
        return _json(200, verify_lab(user=user, email=email, cloud=cloud, lab=lab))
    except ValueError:
        logging.warning("Invalid verify-lab request: cloud=%s lab=%s", cloud, lab)
        return _json(400, {"message": "Invalid verify-lab request."})
    except VerifyError as err:
        body = {"message": err.message, **err.extra}
        return _json(err.status, body)
    except Exception:
        logging.exception("Unexpected error while processing verify-lab request.")
        return _json(500, {"message": "Unexpected server error."})


def _clean_up_lab(payload):
    username = (payload.get("username") or "").strip()
    lab = get_lab(username)
    if not lab:
        logging.warning("Lab data not found for %s", username)
        return _json(404, {"message": "Lab not found"})
    if "password" not in lab or "lab_name" not in lab:
        logging.warning("Lab data is incomplete for %s", username)
        return _json(500, {"message": "Lab data is incomplete"})
    if not dispatch(lab, "destroy", password="dummy"):
        return _json(502, {"message": f"GitHub destroy failed for {username}"})
    logging.info("Triggered destroy action for %s", username)
    return _json(200, {"message": f"Destroy action triggered for {username}"})


def _dispatch(event, route):
    if route.endswith(" /health") or route == "GET /health":
        return _json(200, {"status": "ok"})

    if route in ("GET /", "GET"):
        return _json(200, {"message": "Student Lab Backend API is up and running"})

    if route.endswith("/lab-status/all"):
        return _json(200, {"labs": scan_labs()})

    if route.endswith("/lab-delete-internal"):
        username = (_body(event).get("username") or "").strip()
        if not username:
            return _json(400, {"message": "username required"})
        if delete_lab(username):
            logging.info("Lab '%s' deleted", username)
            return _json(200, {"message": f"Lab '{username}' deleted"})
        logging.warning("Lab '%s' not found", username)
        return _json(404, {"message": f"Lab '{username}' not found"})

    if route.endswith("/start-lab"):
        return _start_lab(_body(event))

    if route.endswith("/lab-ready"):
        return _lab_ready(_body(event))

    if route.endswith("/clean-up-lab"):
        return _clean_up_lab(_body(event))

    if route.endswith("/verify-lab"):
        return _verify_lab(_body(event))

    return _json(404, {"message": "Not Found"})


def handler(event, context):
    route = _route_key(event)
    response = _dispatch(event, route)
    status = response["statusCode"]
    if status >= 400:
        logging.info("route=%s status=%s body=%s", route, status, response.get("body"))
    else:
        logging.debug("route=%s status=%s", route, status)
    return response
