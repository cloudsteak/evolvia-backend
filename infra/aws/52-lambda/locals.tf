locals {
  prefix        = data.terraform_remote_state.oidc.outputs.prefix
  env           = "prod"
  alias_name    = "live"
  ecr           = data.terraform_remote_state.ecr.outputs.repositories
  api_keys_path = "/${local.env}/${local.prefix}/api-keys"
  api_key_names  = toset(["wordpress", "github", "internal"])

  functions = {
    backend = {
      name      = "${local.prefix}-backend"
      image_tag = "1.0.3"
      timeout   = 30
      ses       = true
      dynamodb  = true
      ssm       = false
    }
    cleanup = {
      name      = "${local.prefix}-cleanup"
      image_tag = "1.0.0"
      timeout   = 60
      ses       = false
      dynamodb  = true
      ssm       = false
    }
    authorizer = {
      name      = "${local.prefix}-authorizer"
      image_tag = "1.0.0"
      timeout   = 10
      ses       = false
      dynamodb  = false
      ssm       = true
    }
  }

  github_backend_role_name = element(
    split("/", data.terraform_remote_state.oidc.outputs.github_actions_role_arns[local.functions.backend.name]),
    1,
  )

  github_lambda_policy_name = "${local.github_backend_role_name}-lambda"
}
