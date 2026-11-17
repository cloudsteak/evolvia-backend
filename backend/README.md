# Evolvia lab backend

Lambda. Belépés: `lambda_handler.handler`. A kiadott image a `Dockerfile.lambda` (`public.ecr.aws/lambda/python:3.13`, `linux/arm64`).

A `main.py` és a `Dockerfile` a korábbi konténer. A Lambda image nem másolja be.

## Végpontok

A HTTP API a [60-backend](../infra/aws/60-backend/README.md). A `/health` nyitva. A többi route `X-API-Key` ([authorizer](../authorizer/README.md)).

- `GET /` , `GET /health`
- `POST /start-lab` — DynamoDB item + GitHub Actions apply
- `POST /lab-ready` — SES levél, WordPress webhook
- `POST /verify-lab` — Azure, AWS vagy GCP verify szolgáltatás
- `GET /lab-status/all`
- `POST /clean-up-lab` — GitHub Actions destroy
- `POST /lab-delete-internal` — DynamoDB sor törlése

A lab állapot a `evolvia-platform-labs` táblában van, PK `username`. Lejárat: a [cleanup](../cleanup-trigger/README.md).

## Konfig

A 52 env-je pathot ad, az értéket a Parameter Store tartja. Tofu a paramétert nem kezeli.

| Env | Szerep |
|-----|--------|
| `LOG_LEVEL` | alap `INFO` |
| `LABS_TABLE_NAME` | DynamoDB tábla |
| `SES_FROM_ADDRESS` | `noreply@evolvia.hu` |
| `SSM_PORTAL_AZURE_URL`, `SSM_PORTAL_AWS_URL` | konzol link a levélben |
| `SSM_GITHUB_REPO`, `SSM_GITHUB_TOKEN`, `GITHUB_WORKFLOW_FILENAME` | workflow dispatch. A suffix `-lab-manager.yaml` |
| `SSM_VERIFY_AZURE_{URL,KEY}` | Azure verify. Forrás: evolvia-foundation `azure/50-verify` (`verify_api_url`, Key Vault `verify-api-key`) |
| `SSM_VERIFY_{AWS,GCP}_{URL,KEY}` | AWS és GCP verify hívás, header `X-API-Key` |
| `SSM_WORDPRESS_WEBHOOK_URL`, `SSM_WORDPRESS_WEBHOOK_TOKEN` | lab státusz webhook |

A feladó `Cloud Mentor <noreply@evolvia.hu>`. Azure labnál a felhasználónév `{username}@evolvia.hu`. Sablon: `templates/lab_ready_default.html`.

Az értékek felvétele: [02-infra-tofu](../docs/steps/02-infra-tofu.md#cleanup-3e).

## Image

```bash
docker buildx build --platform linux/arm64 \
  --provenance=false --sbom=false \
  -f backend/Dockerfile.lambda \
  backend
```

A futó tag a [52-lambda](../infra/aws/52-lambda/README.md) `functions.backend.image_tag`. A CI a `latest`-et is rárakja, a Lambda a pinelt taget húzza.
