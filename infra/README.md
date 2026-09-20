# Infra

OpenTofu az izolált platform accountban. Alkalmazáskód: `backend/`, `cleanup-trigger/` — a CI buildeli, nem a tofu.

Átállás: [docs/atallas.md](../docs/atallas.md). **Layer terv:** [docs/layers.md](../docs/layers.md).

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

Későbbi layer `data.terraform_remote_state`. Nincs másolt account ID / ARN. Nincs `local-exec`. `profile = "prod"` marad.

State: `s3://evolvia-platform-iac-state`. Profile: `prod`.
