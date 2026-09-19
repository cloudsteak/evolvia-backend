# 52-lambda

Apply kész. Függvényhéjak a `local.functions` mapben (`backend`, `cleanup`). OCI image + SnapStart, alias `live`.

Image: `{ecr_url}:{local.image_tag}` — pinelt semver, **nem** `latest`. A CI a `latest`-et is rárakja az utolsó image-re; a Lambda azt nem használja.

1. PR: kód → `ecr-backend.yml` build + push ECR (`{verzió}` + `latest`).
2. PR: te beírod a **verziótaget** ide → CI `tofu apply` (Lambda ezt húzza).

Apply csak ha a tagelt image már bent van. Az első 52 előtt le kell futnia az ECR pushnak.

A CI a taget nem írja. Apply csak ha a tagelt image már bent van.

A mai `backend/Dockerfile` (`python:3.13-slim`) custom — a CI image `FROM public.ecr.aws/lambda/python:3.13` (vagy SnapStart label) legyen, különben a SnapStart publish elhasal.

Olvas: 12, 21, 34, 50. Nincs Route53. Image: `50.repositories[<ugyanaz a kulcs>].url` + `image_tag`. Cleanup: `evolvia-cleanup:1.0.0`, nem a backend image.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/lambda/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

## Apply (első ECR push után)

Előfeltétel: [első ECR push](../../../docs/steps/02-infra-tofu.md#első-ecr-push). `local.image_tag` egyezzen a feltolt verzióval.

```bash
cd infra/aws/52-lambda
tofu init
tofu apply
```

A `create` SnapStart snapshot miatt eltarthat.

## Név

- `local.functions` — `name`, `image_tag`, `timeout`, `ses`
- role: `{prefix}-lambda-{key}`
- policies: `{role}-{capability}`; GitHub: `{github-role}-lambda`

## Outputs

- backend: `function_name` / `function_arn` / `invoke_arn` / `qualified_arn`
- cleanup: `cleanup_function_name` / `cleanup_function_arn` / `cleanup_qualified_arn`

## Következő layer

`55-scheduler`.
