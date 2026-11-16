# Cleanup

Lambda. Belépés: `lambda_handler.handler`. Image: `Dockerfile.lambda`. Ütemezés: [55-scheduler](../infra/aws/55-scheduler/README.md), `rate(30 minutes)`, a `cleanup:live` alias.

A `cleanup_trigger.py` és a `Dockerfile` a korábbi konténer (HTTP, `X-Internal-Secret`). A Lambda image nem másolja be.

A scheduler a backend Lambdát invoke-olja (`BACKEND_FUNCTION_NAME` + `BACKEND_ALIAS`), nem a HTTP API-t. Authorizer nincs a híváson.

1. `GET /lab-status/all`
2. Lejárt lab: `POST /clean-up-lab` (GitHub destroy)
3. Sikeres destroy után: `POST /lab-delete-internal`

A GitHub hiba esetén a DynamoDB sor megmarad.

Lejárat a státusz időbélyegétől:

| Státusz | Idő |
|---------|-----|
| `ready` | `lab_ttl`, alap 5400 s (`started_at`) |
| `pending` | 7200 s (`created_at`, ha nincs `error_at`) |
| `failed` és minden más | 14400 s |

Env: `LOG_LEVEL`, `BACKEND_FUNCTION_NAME`, `BACKEND_ALIAS`. A függvény a [52-lambda](../infra/aws/52-lambda/README.md).
