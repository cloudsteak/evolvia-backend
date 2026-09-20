# 4. CI/CD

PR: csak a változott mappa. Merge (`main`): image push, aztán a változott tofu layerek apply (kisebbtől nagyobbig). A CI nem írja a `locals.tf`-et. `profile = "prod"` marad; a runner OIDC után `~/.aws/credentials` `[prod]` profilt kap.

| Változás | PR | Merge |
|----------|----|-------|
| `backend/` | ruff, version bump (`pyproject.toml`), docker build, pytest ha van | ECR `{verzió}` + `latest` |
| `cleanup-trigger/` | ugyanaz | ECR `{verzió}` + `latest` |
| `authorizer/` | ruff, docker build (nincs pyproject; tag a 52 `image_tag`) | ECR, tag a 52 `locals` |
| `infra/aws/<layer>/` | `tofu fmt` + `validate` + `plan` a **változott** layereken, sorrend a sorszám | `tofu apply` ugyanazokon |
| más (`docs/`, …) | semmi | semmi |

`infra/00-remote-state` nem tofu layer, nem CI. A layerek listája a `infra/aws/NN-*` mappákból jön, nincs hardcode.

Két PR továbbra is oké (előbb image, aztán 52 `image_tag`). Egy PR is: merge-ön előbb push, aztán 52 apply.

OIDC secret: `AWS_GITHUB_ROLE_ARN`. A 12-es role `main` + `pull_request`. **Először laptop:** `cd infra/aws/12-oidc && tofu apply` — enélkül a PR plan `AssumeRole` fail.

A K8s GHCR workflow-k (`docker-build-lab-*.yml`) még mennek `main`-re, amíg a 9. kivezetés.

Image: `FROM public.ecr.aws/lambda/python:3.13` (SnapStart). Pinelt semver, nem `latest` a Lambdán.

## Következő

[5. GitHub lab-ready](./05-github-lab-ready.md)
