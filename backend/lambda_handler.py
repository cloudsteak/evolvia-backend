import json


def _is_health(event):
    route_key = event.get("routeKey") or ""
    if route_key == "GET /health" or route_key.endswith("/health"):
        return True

    rc = event.get("requestContext") or {}
    http = rc.get("http") or {}
    for candidate in (event.get("rawPath"), event.get("path"), http.get("path")):
        if candidate and candidate.rstrip("/").endswith("/health"):
            return True
    return False


def handler(event, context):
    if _is_health(event):
        return {
            "statusCode": 200,
            "headers": {"content-type": "application/json"},
            "body": json.dumps({"status": "ok"}),
        }

    return {"statusCode": 200, "body": "evolvia-backend placeholder"}
