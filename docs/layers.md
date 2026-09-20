# Layer terv

Kanonikus sávok ehhez az infra repóhoz. Egy sáv = egy concern. Egy layer = egy primitíva.

## Apply szabály

- **Kisebbtől nagyobbig.** Nincs visszalépés: 22 után 34 oké, 34 után 22 tilos.
- Későbbi layer csak `terraform_remote_state`-et olvas. Nincs másolt account ID / ARN.
- **`aws_route53_record` csak a `22-dns`-ben.** Emiatt minden DNS-értéket adó layer a 22 **előtt** van (20 ACM, 21 SES). A 22 egyszer írja a rekordokat, nincs 40→22.

A foundation számozása (`10-fundamentals`, `40-s3-lifecycle`, `50-verify`) másik account, ide nem másoljuk a jelentését.

## Sávok

| Sáv | Concern | Ez | Nem ez |
|-----|---------|----|--------|
| `00` | bootstrap | remote state bucket | IAM, DNS, app |
| `10–19` | identity | ki vagy, mit tehetsz: OIDC, IAM, később KMS / SSO / secrets | ACM, WAF, VPC. Nem „biztonság mindennel” |
| `20–29` | network | ACM, SES identity (DNS-t generál), DNS, később VPC | ECR, Lambda. Nem docker. Apex MX nem tofu (cPanel) |
| `30–39` | data | tartós store: **30–33 SQL**, **34–36 nosql**, **37 Redis**, **38–39 egyéb** | |
| `40–49` | messaging | SQS / SNS / bus | SES identity (az a 21, mert DNS kell a 22 elé), Scheduler |
| `50–59` | compute | ECR, Lambda, Scheduler | API Gateway |
| `60–69` | apps | HTTP API, authorizer, custom domain | ECR, DDB, SES, Lambda héj, Route53 |

A `backend.api.evolvia.hu` custom domain + Route53 alias a **22**-ben van (hogy legyen mire alias). A 60 csak bind: `api_mapping`.

## Layerek

A kód CI-vel megy az ECR-be, majd a Lambdára. Tofu nem buildel Python-t.

| Layer | Sáv | Mit hoz létre | Olvas | Állapot |
|-------|-----|----------------|-------|---------|
| `00-remote-state` | bootstrap | S3 state | — | kész |
| `12-oidc` | identity | GitHub OIDC + role | — | apply kész |
| `20-certificates` | network | ACM request, apply **visszatér** `PENDING_VALIDATION`-nél | — | apply kész |
| `21-ses` | network | SES identity + DKIM token + MAIL FROM. **Nincs Route53.** Apply visszatér pendingnél | — | apply kész |
| `22-dns` | network | **minden** Route53 + API GW custom domain + alias + ACM/SES waiter | 20, 21 | apply kész; alias catch-up (önálló, nem olvas 60-at) |
| `34-dynamodb` | data / nosql | lab tábla | 12 | apply kész |
| `50-ecr` | compute | ECR map: backend + cleanup + authorizer | 12 | apply kész; authorizer repo catch-up |
| `52-lambda` | compute | minden Lambda (`functions` map), SnapStart, alias `live`, SSM API kulcsok | 12, 21, 34, 50 | apply kész; authorizer catch-up |
| `55-scheduler` | compute | EventBridge Scheduler → cleanup `live`, group `{prefix}`, `rate(15 minutes)` | 12, 52 | apply kész; group catch-up **60 előtt** |
| `60-backend` | apps | HTTP API + bind + Lambda authorizer (`X-API-Key`), CORS, stage `live`. `/health` nyitva. Nincs Route53, nincs domain resource | 12, 22, 52 | apply kész; authorizer bind catch-up |

Később, ha kell: `30–33` SQL, `35–36` nosql, `37` Redis, `38–39` egyéb, `24-vpc`, `18-kms`, `40-sqs`. Üres mappa nincs előre.

State key a concern neve (`aws/ses/state.tfstate`), nem a sorszám.

## Név

`prefix` a 12-es state-ből. Két minta:

| Fajta | Minta | Példa |
|-------|--------|--------|
| termék (ECR, DDB, Lambda) | `{prefix}-{subject}` | `evolvia-backend`, `evolvia-platform-labs` |
| IAM role | `{prefix}-{actor}-{subject}` | `evolvia-github-evolvia-backend` |
| IAM policy | `{role}-{capability}` | `evolvia-github-evolvia-backend-ecr`; 52: `…-lambda` |

A név a layer `locals`-ában egyszer. DNS hostname nem ez a minta (`lab-api.evolvia.hu`).

## Apply sorrend

```
00 → 12 → 20-certificates → 21-ses → 22-dns → 34-dynamodb → 50-ecr → első image push → 52-lambda → 55-scheduler → 60-backend
```

Az első image (laptop, 50 után, 52 előtt): [02-infra-tofu](./steps/02-infra-tofu.md#első-ecr-push). Később ugyanez a CI.

A 22 és a 34 már lefutott, a 21 kimaradt. Catch-up: **21-ses apply, aztán 22-dns egyszer** (SES rekordok). Utána nincs vissza a 22-re. A 34-et nem kell újra.

## CI vs tofu

Minden tofu layer ugyanaz: `tofu init && tofu apply`. Nincs `local-exec`, nincs layer-script. A `profile = "prod"` a backendben és a providerben marad.

| Változás | Hol |
|----------|-----|
| IAM, DNS, tábla, SES, Lambda héj, API | tofu apply a saját layerben (laptop vagy CI, ugyanaz a parancs) |
| Python / image | PR1: CI build + ECR push (új tag). PR2: te `local.image_tag` → CI 52 tofu apply |

A `00-remote-state` egyszeri bootstrap volt (bucket a `tofu init` előtt); nem tofu layer, nem CI-lépés. Tovább nem ismételjük.
