# 4. CI/CD

Nulláról az első image **laptop**: [02-infra-tofu — első ECR push](./02-infra-tofu.md#első-ecr-push). Main után ugyanez: `.github/workflows/ecr-backend.yml`. OIDC secret: `AWS_GITHUB_ROLE_ARN`.

Két PR, nem egyben:

| PR | Mit | CI AWS-ben |
|----|-----|------------|
| 1 | `backend/` + `pyproject.toml` verzió | build + push ECR: **`{verzió}` és `latest`** (ugyanaz a digest; a `latest` mindig az utolsó build) |
| 2 | te beírod a **verziótaget** `52-lambda` `local.image_tag`-be | `tofu apply` — a Lambda a pinelt taget húzza, **nem** a `latest`-et |

A CI nem írja a `locals.tf`-et. `infra/aws/**` változás: tofu plan/apply. Nincs script, nincs `local-exec`. `profile = "prod"` marad.

Image: `FROM public.ecr.aws/lambda/python:3.13` (SnapStart). A mai slim Dockerfile később cserélendő.

## Következő

[5. GitHub lab-ready](./05-github-lab-ready.md)
