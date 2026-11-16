# Infra

OpenTofu az izolált platform accountban. Alkalmazáskód: `backend/`, `cleanup-trigger/`, `authorizer/` — a CI buildeli, nem a tofu.

Átállás: [docs/atallas.md](../docs/atallas.md). **Layer terv:** [docs/layers.md](../docs/layers.md).

## AWS belépés

A provider és az S3 backend a helyi SSO profilt olvassa (platform account, `eu-north-1`). A profil beállítása a gépen marad: név, account ID és start URL nem kerül ide.

```bash
aws sso login --profile <profil>
aws sts get-caller-identity --profile <profil>
```

A session lejár; utána újra ugyanez a login. A tofu a kódban lévő profilnevet használja. AWS CLI parancshoz ugyanaz a `--profile`, vagy az `AWS_PROFILE` változó.

## OpenTofu

A parancs `tofu`. Verzió `>= 1.10.7` (CI: `1.12.5`).

```bash
brew install opentofu
tofu version
```

Belépés után, layerenként (a state a `s3://evolvia-platform-iac-state` bucketben van, `eu-north-1`):

```bash
cd infra/aws/60-backend
tofu init
tofu plan
```

Apply ugyanabból a mappából: `tofu apply`. Sorrend lent.

Apply: kisebbtől nagyobbig, **nincs visszalépés**. `aws_route53_record` csak `22-dns`.

```
infra/
  00-remote-state/      # kész
  aws/
    12-oidc/            # apply kész
    20-certificates/    # apply kész
    21-ses/             # apply kész
    22-dns/             # apply kész (ACM ISSUED, SES verified)
    34-dynamodb/        # apply kész
    50-ecr/             # apply kész
    52-lambda/          # apply kész
    55-scheduler/       # apply kész
    60-backend/         # apply kész
```

40–49 (SQS) üres.

Sorrend: `00` → `12` → `20` → `21` → `22` → `34` → `50` → `52` → `55` → `60`.

Későbbi layer `data.terraform_remote_state`. Nincs másolt account ID / ARN. Nincs `local-exec`. A provider profilneve a kódban marad.

State: `s3://evolvia-platform-iac-state`.
