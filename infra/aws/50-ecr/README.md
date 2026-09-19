# 50-ecr

Apply kész (backend). Cleanup repo: **újra apply**. `local.repositories` map: `backend`, `cleanup`.

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

`local.repositories` — `{prefix}-{key}` → `evolvia-backend`, `evolvia-cleanup`.

## Outputs

- `repositories` (name / url / arn)
- `ecr_repository_url` / `ecr_repository_arn` (backend, compat)

## Első push

[02-infra-tofu — első ECR push](../../../docs/steps/02-infra-tofu.md#első-ecr-push) — backend és cleanup külön.

## Következő

Cleanup image push, aztán `52-lambda`.
