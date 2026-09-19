# 3. Backend kódátírás

Még nincs implementálva. A kód a `backend/` és `cleanup-trigger/` alatt marad; az infra nem ide kerül.

## Sorrend a 3. lépésen belül

| # | Mit |
|---|-----|
| 3a | DynamoDB repository — PK `username`. Redis kimegy. |
| 3b | API Lambda — natív handler, path routing. Ne Mangum. |
| 3c | Authorizer — `X-API-Key` → SSM. Három kulcs: wordpress, github, internal. |
| 3d | SES emailer — `lab_ready_default.html` + emailer a cm-messengertől. `messenger_client.py` törölve. |
| 3e | Cleanup Lambda — közvetlen DynamoDB + GitHub destroy. `rate(15 minutes)`. |

Végpontok: `/`, `/health`, `start-lab`, `lab-ready`, `verify-lab`, `lab-status/all`, `clean-up-lab`, `lab-delete-internal`.

## Következő

[4. CI/CD](./04-cicd.md)
