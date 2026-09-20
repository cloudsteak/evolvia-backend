# 3. Backend kódátírás

Még nincs implementálva. A kód a `backend/` és `cleanup-trigger/` alatt marad; az infra nem ide kerül.

## Sorrend a 3. lépésen belül

| # | Mit |
|---|-----|
| 3a | DynamoDB repository — PK `username`. `backend/labs.py`. `main.py` Redis nélkül. Live: `lab-status/all` / `lab-delete-internal` a handlerben. |
| 3b | API Lambda — natív handler, path routing. Ne Mangum. |
| 3c | Authorizer — `X-API-Key` → SSM (wordpress, github, internal). **Előrehozva:** 52 Lambda + SSM, 60 CUSTOM. Infra kész az apply/push után; a 8/5 kliens még Auth0. |
| 3d | SES — `lab_ready_default.html` + `emailer.py`. `From: Evolvia <noreply@evolvia.hu>`. Azure user `…@evolvia.hu`. `messenger_client.py` törölve. |
| 3e | Cleanup: `lab-status/all` → lejárt: `clean-up-lab` (GitHub destroy) → `lab-delete-internal` (DDB). |

Végpontok: `/`, `/health`, `start-lab`, `lab-ready`, `verify-lab`, `lab-status/all`, `clean-up-lab`, `lab-delete-internal`.

**Később (ne felejtsük):**
- kulcs-scope. Most mindhárom kulcs minden védett route-ra jó. Kell: wordpress / github **ne** listázza a labokat (`GET /lab-status/all`), ne töröljön (`clean-up-lab`, `lab-delete-internal`). Az internal igen. Az authorizer `isAuthorized` mellé context (pl. `key_name`) + a handler vagy route-szintű ellenőrzés.
- `52` `log_level` mindhárom Lambda: most `DEBUG` (élesítés). **Végén vissza `INFO`.**

## Következő

[4. CI/CD](./04-cicd.md)
