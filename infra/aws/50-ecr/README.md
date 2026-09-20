# 50-ecr

Apply kész. `local.repositories`: `backend`, `cleanup`, `authorizer`. Új repo: **újra apply**, aztán image push, aztán 52.

Lifecycle mindkettőn: `latest` + 5× `*.*` + untagged 180 nap. GitHub policy mindkét repo ARN-jére.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/ecr/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

## Apply

```bash
cd infra/aws/50-ecr
tofu init
tofu apply
```

## Név

`local.repositories` — `{prefix}-{key}` → `evolvia-backend`, `evolvia-cleanup`, `evolvia-authorizer`.

## Outputs

- `repositories` (name / url / arn)
- `ecr_repository_url` / `ecr_repository_arn` (backend, compat)

## Első push

[02-infra-tofu — első ECR push](../../../docs/steps/02-infra-tofu.md#első-ecr-push) — backend, cleanup, authorizer külön. Authorizer catch-up: [ugyanott](../../../docs/steps/02-infra-tofu.md#authorizer-catch-up-3c-előre).

## Következő

Cleanup image push, aztán `52-lambda`.
