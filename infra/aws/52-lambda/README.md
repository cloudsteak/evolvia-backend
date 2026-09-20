# 52-lambda

Függvényhéjak a `local.functions` mapben (`backend`, `cleanup`, `authorizer`). OCI image + SnapStart, alias `live`. Minden Lambda itt van.

Image: `{ecr_url}:{local.image_tag}` — pinelt semver, **nem** `latest`. A CI a `latest`-et is rárakja az utolsó image-re; a Lambda azt nem használja.

1. PR: kód → CI ECR push (`{verzió}` + `latest`).
2. PR: te beírod a **verziótaget** ide → CI `tofu apply` (Lambda ezt húzza). Egy PR is lehet: merge-ön előbb image, aztán apply.

Apply csak ha a tagelt image már bent van. Az első 52 előtt le kell futnia az ECR pushnak.

A CI a taget nem írja. Apply csak ha a tagelt image már bent van.

`LOG_LEVEL` minden Lambda env-jén (`functions.*.log_level`, alap `INFO`). Scheduler = cleanup Lambda. `DEBUG`: sikeres hívások is. Jelszó / API-kulcs nincs a logban.

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

- `local.functions` — `name`, `image_tag`, `timeout`, `ses`, `dynamodb`, `ssm`
- Parameter Store pathok localsben; az érték CLI `put-parameter`, a tofu nem kezeli a paramétert. Workflow suffix: `local.github_workflow_filename`.
- role: `{prefix}-lambda-{key}`
- policies: `{role}-{capability}`; GitHub: `{github-role}-lambda`

## Outputs

- backend: `function_name` / `function_arn` / `invoke_arn` / `qualified_arn`
- cleanup: `cleanup_function_name` / `cleanup_function_arn` / `cleanup_qualified_arn`

## Következő layer

`55-scheduler`.
