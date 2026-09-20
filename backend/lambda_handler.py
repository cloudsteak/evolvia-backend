import json
import logging
import os
from datetime import datetime, timezone

from credentials import generate_credentials
from labs import delete_lab, get_lab, put_lab, scan_labs

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
    put_lab(item)
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
        return _json(200, {"message": f"Lab {username} reported status: {status_value}"})

    lab["status"] = "ready"
    lab["started_at"] = now
    put_lab(lab)
    return _json(200, {"message": f"Lab {username} marked as ready"})


def _clean_up_lab(payload):
    username = (payload.get("username") or "").strip()
    lab = get_lab(username)
    if not lab:
        return _json(404, {"message": "Lab not found"})
    if "lab_name" not in lab:
        return _json(500, {"message": "Lab data is incomplete"})
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
            return _json(200, {"message": f"Lab '{username}' deleted"})
        return _json(404, {"message": f"Lab '{username}' not found"})

    if route.endswith("/start-lab"):
        return _start_lab(_body(event))

    if route.endswith("/lab-ready"):
        return _lab_ready(_body(event))

    if route.endswith("/clean-up-lab"):
        return _clean_up_lab(_body(event))

    if route.endswith("/verify-lab"):
        return _json(501, {"message": "Not implemented"})

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
