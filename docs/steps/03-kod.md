# 3. Backend kódátírás

Kész. A kiadott belépési pont a Lambda handler. A `backend/main.py` és a `cleanup-trigger/cleanup_trigger.py` a korábbi konténer; a Lambda image nem másolja be.

## Hol van

| # | Hol |
|---|-----|
| 3a | DynamoDB, PK `username`. `backend/labs.py`. |
| 3b | `backend/lambda_handler.py`. `start-lab`: DDB + GitHub apply. |
| 3c | `authorizer/lambda_handler.py`. `X-API-Key` → SSM `/prod/evolvia/api-keys/` (wordpress, github, internal). Bind: 60 CUSTOM. `GET /health` nyitva. |
| 3d | `backend/templates/lab_ready_default.html`, `backend/emailer.py`. From: `Cloud Mentor <noreply@evolvia.hu>`. Azure user `…@evolvia.hu`. |
| 3e | `cleanup-trigger/lambda_handler.py`. `lab-status/all` → lejárt: `clean-up-lab` (GitHub destroy) → `lab-delete-internal`. Ütemezés: 55. |

Végpontok: `/`, `/health`, `start-lab`, `lab-ready`, `verify-lab`, `lab-status/all`, `clean-up-lab`, `lab-delete-internal`.

Részletek: [backend](../../backend/README.md), [cleanup-trigger](../../cleanup-trigger/README.md), [authorizer](../../authorizer/README.md).

`LOG_LEVEL` mindhárom Lambdán `INFO` (`52` `functions.*.log_level`).

**Később (ne felejtsük):** kulcs-scope. Most mindhárom kulcs minden védett route-ra jó. Kell: wordpress / github ne listázza a labokat (`GET /lab-status/all`), ne töröljön (`clean-up-lab`, `lab-delete-internal`). Az internal igen. Az authorizer `isAuthorized` mellé context (pl. `key_name`) + a handler vagy route-szintű ellenőrzés.

## Következő

[4. CI/CD](./04-cicd.md)
