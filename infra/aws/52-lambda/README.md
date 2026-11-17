# 52-lambda

Függvényhéjak a `local.functions` mapben (`backend`, `cleanup`, `authorizer`). OCI image + SnapStart, alias `live`. Minden Lambda itt van.

Image: `{ecr_url}:{image_tag}` — pinelt semver, **nem** `latest`. A CI platform `linux/arm64`. A CI a `latest`-et is rárakja az utolsó image-re; a Lambda azt nem használja. A futó architektúra függvényenként: `functions.*.architecture` (`arm64` vagy `x86_64`). Most mindhárom `arm64`, tag `1.1.0`.

1. PR: ruff, version bump, docker build. Push nincs.
2. Merge: ECR `{verzió}` + `latest`.
3. A `image_tag` és az `architecture` ide kerül, külön változásként. Egy PR is lehet: merge-ön előbb image, aztán apply. A CI a taget nem írja.

Apply csak ha a tagelt image már bent van.

`LOG_LEVEL` minden Lambda env-jén (`functions.*.log_level`, alap `INFO`). Scheduler = cleanup Lambda. `DEBUG`: sikeres hívások is. Jelszó / API-kulcs nincs a logban.

A kiadott image a `Dockerfile.lambda` (`FROM public.ecr.aws/lambda/python:3.13`). A `backend/Dockerfile` és a `cleanup-trigger/Dockerfile` a korábbi konténer, a Lambda nem ezt futtatja.

Olvas: 12, 21, 34, 50. Nincs Route53. Image: `50.repositories[<ugyanaz a kulcs>].url` + `image_tag`. A cleanup a saját repója és a saját `image_tag`-je, nem a backend image.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/lambda/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

## Apply (első ECR push után)

Előfeltétel: [első ECR push](../../../docs/steps/02-infra-tofu.md#első-ecr-push). `functions.*.image_tag` egyezzen a feltolt verzióval. `architecture` a választott platform.

```bash
cd infra/aws/52-lambda
tofu init
tofu apply
```

A `create` SnapStart snapshot miatt eltarthat.

## Név

- `local.functions` — `name`, `image_tag`, `architecture` (`arm64` vagy `x86_64`), `timeout`, `log_level`, `ses`, `dynamodb`, `ssm`, `github`, `verify`, `wordpress`, `invoke_backend`
- Parameter Store pathok localsben; az érték CLI `put-parameter`, a tofu nem kezeli a paramétert. Workflow suffix: `local.github_workflow_filename`.
- role: `{prefix}-lambda-{key}`
- policies: `{role}-{capability}`; GitHub: `{github-role}-lambda`

## Outputs

- `functions` — name, arn, image_uri, invoke_arn, qualified_arn (backend, cleanup, authorizer)
- `function_name`, `invoke_arn`, `qualified_arn` — backend alias
- `cleanup_qualified_arn` — cleanup alias, a 55 olvassa

## Következő layer

`55-scheduler`.
