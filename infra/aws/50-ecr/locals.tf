locals {
  prefix = data.terraform_remote_state.oidc.outputs.prefix

  repositories = {
    backend = {
      name = "${local.prefix}-backend"
    }
    cleanup = {
      name = "${local.prefix}-cleanup"
    }
    authorizer = {
      name = "${local.prefix}-authorizer"
    }
  }

  ecr_keep_count          = 5
  ecr_expire_days         = 30
  ecr_version_tag_pattern = "*.*"

  ecr_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep latest"
        selection = {
          tagStatus      = "tagged"
          tagPatternList = ["latest"]
          countType      = "imageCountMoreThan"
          countNumber    = 1
        }
        action = { type = "expire" }
      },
      {
        rulePriority = 2
        description  = "Keep ${local.ecr_keep_count} version tags"
        selection = {
          tagStatus      = "tagged"
          tagPatternList = [local.ecr_version_tag_pattern]
          countType      = "imageCountMoreThan"
          countNumber    = local.ecr_keep_count
        }
        action = { type = "expire" }
      },
      {
        rulePriority = 3
        description  = "Expire untagged older than ${local.ecr_expire_days} days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = local.ecr_expire_days
        }
        action = { type = "expire" }
      }
    ]
  })

  github_backend_role_name = element(
    split("/", data.terraform_remote_state.oidc.outputs.github_actions_role_arns[local.repositories.backend.name]),
    1,
  )

  github_ecr_policy_name = "${local.github_backend_role_name}-ecr"
}
