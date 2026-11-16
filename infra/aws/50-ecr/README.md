# 50-ecr

Apply kész. `local.repositories`: `backend`, `cleanup`, `authorizer`. Új repo: **újra apply**, aztán image push, aztán 52.

Lifecycle mindhárom repón: `latest` + 5× `*.*` + untagged 30 nap. A GitHub policy mindhárom repo ARN-jére megy.

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

[02-infra-tofu — első ECR push](../../../docs/steps/02-infra-tofu.md#első-ecr-push) — backend és cleanup. Authorizer image és API-kulcs: [API-kulcsok](../../../docs/steps/02-infra-tofu.md#api-kulcsok).

## Következő

`52-lambda`. Apply kész. Az image tag a 52 `functions.*.image_tag`.
