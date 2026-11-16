# EVOLVIA-BACKEND

Lab környezetek (Azure, AWS, GCP) indítása. A lab állapot DynamoDB-ben van, a kész labról SES küld emailt. A HTTP API Lambda mögött fut. A védett route-ok `X-API-Key` headert várnak. `GET /health` nyitva.

Átállás: [docs/atallas.md](docs/atallas.md). Layer terv: [docs/layers.md](docs/layers.md).

## Kód

- [backend/](backend/README.md) — API (lab indítás, státusz, verify, email)
- [cleanup-trigger/](cleanup-trigger/README.md) — lejárt labok törlése
- [authorizer/](authorizer/README.md) — `X-API-Key` ellenőrzés SSM-ből

A kiadott image mindháromnál a `Dockerfile.lambda`. A `backend/Dockerfile` és a `cleanup-trigger/Dockerfile` a korábbi konténer.

## Infra

OpenTofu, apply sorrend: [infra/README.md](infra/README.md).

- [infra/00-remote-state/](infra/00-remote-state/README.md)
- [infra/aws/12-oidc/](infra/aws/12-oidc/README.md)
- [infra/aws/20-certificates/](infra/aws/20-certificates/README.md)
- [infra/aws/21-ses/](infra/aws/21-ses/README.md)
- [infra/aws/22-dns/](infra/aws/22-dns/README.md)
- [infra/aws/34-dynamodb/](infra/aws/34-dynamodb/README.md)
- [infra/aws/50-ecr/](infra/aws/50-ecr/README.md)
- [infra/aws/52-lambda/](infra/aws/52-lambda/README.md)
- [infra/aws/55-scheduler/](infra/aws/55-scheduler/README.md)
- [infra/aws/60-backend/](infra/aws/60-backend/README.md)

## API

Host: `https://backend.api.evolvia.hu`. A `/health` kivételével minden route `X-API-Key`.

- `GET /` , `GET /health`
- `POST /start-lab`
- `POST /lab-ready`
- `POST /verify-lab`
- `GET /lab-status/all`
- `POST /clean-up-lab`
- `POST /lab-delete-internal`
