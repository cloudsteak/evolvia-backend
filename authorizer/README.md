# Authorizer

API Gateway Lambda authorizer. Belépés: `lambda_handler.handler`. Image: `Dockerfile.lambda` (`public.ecr.aws/lambda/python:3.13`).

A `X-API-Key` header értéke a Parameter Store `/prod/evolvia/api-keys/` alatti SecureStringekkel egyezik (wordpress, github, internal). Egyezés: `isAuthorized: true`. A kulcsok most minden védett route-ra jók. Scope: [docs/steps/03-kod.md](../docs/steps/03-kod.md).

Cache: 60 mp a függvényben és az API Gateway authorizer TTL-ben. Új kulcs a cache után érvényes; a kliensnek is az új értéket kell küldenie.

Nincs saját tofu layer. A függvény a [52-lambda](../infra/aws/52-lambda/README.md), a bind a [60-backend](../infra/aws/60-backend/README.md). `GET /health` nyitva, authorizer nélkül.

A kulcs értéke CLI `put-parameter`, a tofu csak a pathot és az IAM-ot ismeri: [02-infra-tofu](../docs/steps/02-infra-tofu.md#api-kulcsok).
