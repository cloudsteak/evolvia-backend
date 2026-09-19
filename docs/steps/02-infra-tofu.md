# 2. Infra tofu

A sávok és a sorrend: **[docs/layers.md](../layers.md)**. Kisebbtől nagyobbig, nincs visszalépés.

## Állapot

| Layer | Állapot |
|-------|---------|
| 12-oidc | apply kész |
| 20-certificates | apply kész |
| 21-ses | apply kész |
| 22-dns | apply kész; **alias catch-up** (custom domain + A/AAAA) |
| 34-dynamodb | apply kész (`evolvia-platform-labs`) |
| 50-ecr | apply kész (`evolvia-backend`, `evolvia-cleanup`) |
| első ECR push | laptop kész (`1.0.0` + `latest`, mindkét repo) |
| 52-lambda | apply kész |
| 55-scheduler | apply kész |
| 60-backend | apply kész; bind a 22 alias catch-up után |

A 22 alias catch-up: ha a domain még a 60-é, 60 destroy (vagy a domain resource), aztán `cd infra/aws/22-dns && tofu apply` — a 22 létrehozza, nem importál, 60-at nem olvassa. Aztán 60 apply (bind).

## Első ECR push

Nulláról: 50 apply után, 52 apply **előtt**. Két repo, két push. Repo gyökér.

`"${URI}:latest"` — kapcsos zárójel. `--provenance=false --sbom=false` — a Lambda nem fogad Image Indexet.

```bash
export AWS_PROFILE=prod
export AWS_REGION=eu-north-1

# backend
URI=$(aws ecr describe-repositories --repository-names evolvia-backend --region eu-north-1 --query 'repositories[0].repositoryUri' --output text)
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin "${URI}"
docker buildx build --platform linux/amd64 \
  --provenance=false --sbom=false \
  -f backend/Dockerfile.lambda \
  -t "${URI}:1.0.0" \
  -t "${URI}:latest" \
  --push \
  backend

# cleanup — 50 apply után, ha a repo már létezik
URI=$(aws ecr describe-repositories --repository-names evolvia-cleanup --region eu-north-1 --query 'repositories[0].repositoryUri' --output text)
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin "${URI}"
docker buildx build --platform linux/amd64 \
  --provenance=false --sbom=false \
  -f cleanup-trigger/Dockerfile.lambda \
  -t "${URI}:1.0.0" \
  -t "${URI}:latest" \
  --push \
  cleanup-trigger
```

A 52 `functions` kulcsa = 50 `repositories` kulcsa (`backend`, `cleanup`). Main után: CI (`ecr-backend.yml`; cleanup workflow később).

## 52 apply

Már lefutott.

## 55 apply

Már lefutott.

## 60 apply

Stage `live`, 7 route. Alias: 22 catch-up után `https://backend.api.evolvia.hu/`.
