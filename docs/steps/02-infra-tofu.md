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

A 52 `functions` kulcsa = 50 `repositories` kulcsa (`backend`, `cleanup`, `authorizer`). Main után: CI (`ecr-backend.yml`; cleanup/authorizer workflow később).

## Authorizer catch-up (3c előre)

50 apply **előbb** (repo). Image push a **repo gyökérből**. 52 apply **után**.

`"${URI}:latest"` — kapcsos zárójel. `--provenance=false --sbom=false` — a Lambda nem fogad Image Indexet.

```bash
cd infra/aws/50-ecr
tofu apply
```

```bash
export AWS_PROFILE=prod
export AWS_REGION=eu-north-1

URI=$(aws ecr describe-repositories --repository-names evolvia-authorizer --region eu-north-1 --query 'repositories[0].repositoryUri' --output text)
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin "${URI}"
docker buildx build --platform linux/amd64 \
  --provenance=false --sbom=false \
  -f authorizer/Dockerfile.lambda \
  -t "${URI}:1.0.0" \
  -t "${URI}:latest" \
  --push \
  authorizer
```

```bash
cd infra/aws/52-lambda
tofu apply
```

Ha a paraméter már létezik (`ParameterAlreadyExists`): **import**, ne overwrite (az `replace-me`-t ráírná).

```bash
cd infra/aws/52-lambda
tofu import 'aws_ssm_parameter.api_keys["wordpress"]' /prod/evolvia/api-keys/wordpress
tofu import 'aws_ssm_parameter.api_keys["github"]' /prod/evolvia/api-keys/github
tofu import 'aws_ssm_parameter.api_keys["internal"]' /prod/evolvia/api-keys/internal
tofu apply
```

A három SecureStringt te írod felül (`replace-me` nem kulcs). Új kulcs (első feltöltés és **rotation** ugyanaz):

```bash
openssl rand -hex 32
```

256 bit, header-barát. A `github` kulcs új (eddig Auth0); nem a `ghp_` PAT.

```bash
export AWS_PROFILE=prod
export AWS_REGION=eu-north-1

aws ssm put-parameter --name /prod/evolvia/api-keys/wordpress --type SecureString --overwrite --value '…'
aws ssm put-parameter --name /prod/evolvia/api-keys/github --type SecureString --overwrite --value '…'
aws ssm put-parameter --name /prod/evolvia/api-keys/internal --type SecureString --overwrite --value '…'
```

Rotation: új `openssl rand -hex 32`, ugyanaz a `put-parameter --overwrite`. Az authorizer cache 60 mp; utána a kliens (plugin / GitHub secret) is az új értéket küldje.

```bash
cd infra/aws/60-backend
tofu apply
```

`GET /health` nyitva. A többi route: header `X-API-Key`.

## 52 apply

Már lefutott. Authorizer: fenti catch-up.

## 55 apply

Már lefutott.

## 60 apply

Stage `live`. Alias: `https://backend.api.evolvia.hu/`. Authorizer: fenti catch-up.

## Cleanup (3e)

Repo és portal URL **nem** locals: Parameter Store, String. Workflow suffix (`-lab.yml`) locals. Token: SecureString. Tofu csak path + `replace-me` (`ignore_changes`). Érték: `put-parameter`. Ha a paraméter már van: import, ne overwrite tofu-val.

```bash
aws ssm put-parameter --name /prod/evolvia/github/repo --type String --overwrite --value 'cloudsteak/evolvia-labs'
aws ssm put-parameter --name /prod/evolvia/portal/azure --type String --overwrite --value 'https://portal.azure.com'
aws ssm put-parameter --name /prod/evolvia/portal/aws --type String --overwrite --value 'https://evolvia.signin.aws.amazon.com/console'
```

Import, ha AWS-ben már megvan, state-ben nem:

```bash
tofu import 'aws_ssm_parameter.config["github_repo"]' /prod/evolvia/github/repo
tofu import 'aws_ssm_parameter.config["portal_azure"]' /prod/evolvia/portal/azure
tofu import 'aws_ssm_parameter.config["portal_aws"]' /prod/evolvia/portal/aws
```

```bash
export AWS_PROFILE=prod
export AWS_REGION=eu-north-1

# ha még nincs a state-ben, de AWS-ben igen:
# tofu import aws_ssm_parameter.github_token /prod/evolvia/github/token

aws ssm put-parameter --name /prod/evolvia/github/token --type SecureString --overwrite --value '…'

URI=$(aws ecr describe-repositories --repository-names evolvia-cleanup --region eu-north-1 --query 'repositories[0].repositoryUri' --output text)
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin "${URI}"
docker buildx build --platform linux/amd64 \
  --provenance=false --sbom=false \
  -f cleanup-trigger/Dockerfile.lambda \
  -t "${URI}:1.0.1" \
  -t "${URI}:latest" \
  --push \
  cleanup-trigger

cd infra/aws/52-lambda
tofu apply
```

Scheduler: group `evolvia`, `evolvia-cleanup`, 30 perc. Log: `/aws/lambda/evolvia-cleanup`. GitHub hiba esetén a DynamoDB sort **nem** törli.
