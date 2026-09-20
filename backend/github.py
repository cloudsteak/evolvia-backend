import json
import logging
import os
import urllib.error
import urllib.request

import boto3

_PLACEHOLDER = "replace-me"
_params = {}


def _ssm(name):
    if name not in _params:
        value = boto3.client("ssm").get_parameter(Name=name, WithDecryption=True)["Parameter"]["Value"]
        if not value or value == _PLACEHOLDER:
            raise RuntimeError(f"SSM {name} is missing or still replace-me")
        _params[name] = value
    return _params[name]


def dispatch(lab, action, password="dummy"):
    repo = _ssm(os.environ["GITHUB_REPO_PATH"])
    token = _ssm(os.environ["GITHUB_TOKEN_PATH"])
    workflow = f"{lab.get('cloud_provider') or 'aws'}{os.environ['GITHUB_WORKFLOW_FILENAME']}"
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow}/dispatches"
    body = json.dumps(
        {
            "ref": "main",
            "inputs": {
                "lab": lab["lab_name"],
                "action": action,
                "student_username": lab["username"],
                "student_password": password,
            },
        }
    ).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            ok = 200 <= resp.status < 300
            if ok:
                logging.debug("GitHub %s dispatched for %s", action, lab.get("username"))
            return ok
    except urllib.error.HTTPError as err:
        logging.error(
            "GitHub %s failed for %s: %s %s",
            action,
            lab.get("username"),
            err.code,
            err.read().decode()[:500],
        )
        return False
