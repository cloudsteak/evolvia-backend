locals {
  prefix     = data.terraform_remote_state.oidc.outputs.prefix
  alias_name = "live"
  ecr        = data.terraform_remote_state.ecr.outputs.repositories

  functions = {
    backend = {
      name      = "${local.prefix}-backend"
      image_tag = "1.0.2"
      timeout   = 30
      ses       = true
    }
    cleanup = {
      name      = "${local.prefix}-cleanup"
      image_tag = "1.0.0"
      timeout   = 60
      ses       = false
    }
  }

  github_backend_role_name = element(
    split("/", data.terraform_remote_state.oidc.outputs.github_actions_role_arns[local.functions.backend.name]),
    1,
  )

  github_lambda_policy_name = "${local.github_backend_role_name}-lambda"
}
