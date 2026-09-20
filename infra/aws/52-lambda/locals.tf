locals {
  prefix        = data.terraform_remote_state.oidc.outputs.prefix
  env           = "prod"
  alias_name    = "live"
  ecr           = data.terraform_remote_state.ecr.outputs.repositories
  api_keys_path            = "/${local.env}/${local.prefix}/api-keys"
  api_key_names            = toset(["wordpress", "github", "internal"])
  github_path               = "/${local.env}/${local.prefix}/github"
  github_token_path         = "${local.github_path}/token"
  github_repo_path          = "${local.github_path}/repo"
  github_workflow_filename  = "-lab-manager.yaml"
  portal_path               = "/${local.env}/${local.prefix}/portal"
  portal_azure_url_path     = "${local.portal_path}/azure"
  portal_aws_url_path       = "${local.portal_path}/aws"
  verify_path               = "/${local.env}/${local.prefix}/verify"
  verify_clouds             = toset(["azure", "aws", "gcp"])
  wordpress_path            = "/${local.env}/${local.prefix}/wordpress"
  wordpress_webhook_url_path   = "${local.wordpress_path}/webhook-url"
  wordpress_webhook_token_path = "${local.wordpress_path}/webhook-token"

  config_parameters = {
    github_repo  = local.github_repo_path
    portal_azure = local.portal_azure_url_path
    portal_aws   = local.portal_aws_url_path
  }

  functions = {
    backend = {
      name      = "${local.prefix}-backend"
      image_tag = "1.0.8"
      timeout   = 30
      log_level = "DEBUG"
      ses       = true
      dynamodb  = true
      ssm            = false
      github         = true
      verify         = true
      wordpress      = true
      invoke_backend = false
    }
    cleanup = {
      name           = "${local.prefix}-cleanup"
      image_tag      = "1.0.4"
      timeout        = 60
      log_level      = "DEBUG"
      ses            = false
      dynamodb       = false
      ssm            = false
      github         = false
      verify         = false
      wordpress      = false
      invoke_backend = true
    }
    authorizer = {
      name      = "${local.prefix}-authorizer"
      image_tag = "1.0.1"
      timeout   = 10
      log_level = "DEBUG"
      ses       = false
      dynamodb  = false
      ssm       = true
      github    = false
      verify    = false
      wordpress = false
      invoke_backend = false
    }
  }

  github_backend_role_name = element(
    split("/", data.terraform_remote_state.oidc.outputs.github_actions_role_arns[local.functions.backend.name]),
    1,
  )

  github_lambda_policy_name = "${local.github_backend_role_name}-lambda"
}
