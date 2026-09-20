locals {
  prefix                      = data.terraform_remote_state.oidc.outputs.prefix
  env                         = "prod"
  alias_name                  = "live"
  ecr                         = data.terraform_remote_state.ecr.outputs.repositories
  ssm_api_keys                = "/${local.env}/${local.prefix}/api-keys"
  ssm_github                  = "/${local.env}/${local.prefix}/github"
  ssm_github_token            = "${local.ssm_github}/token"
  ssm_github_repo             = "${local.ssm_github}/repo"
  github_workflow_filename    = "-lab-manager.yaml"
  ssm_portal                  = "/${local.env}/${local.prefix}/portal"
  ssm_portal_azure_url        = "${local.ssm_portal}/azure"
  ssm_portal_aws_url          = "${local.ssm_portal}/aws"
  ssm_verify_azure_url        = "/${local.env}/${local.prefix}/verify/azure/url"
  ssm_verify_azure_key        = "/${local.env}/${local.prefix}/verify/azure/key"
  ssm_verify_aws_url          = "/${local.env}/${local.prefix}/verify/aws/url"
  ssm_verify_aws_key          = "/${local.env}/${local.prefix}/verify/aws/key"
  ssm_verify_gcp_url          = "/${local.env}/${local.prefix}/verify/gcp/url"
  ssm_verify_gcp_key          = "/${local.env}/${local.prefix}/verify/gcp/key"
  ssm_wordpress               = "/${local.env}/${local.prefix}/wordpress"
  ssm_wordpress_webhook_url   = "${local.ssm_wordpress}/webhook-url"
  ssm_wordpress_webhook_token = "${local.ssm_wordpress}/webhook-token"

  functions = {
    backend = {
      name           = "${local.prefix}-backend"
      image_tag      = "1.0.13"
      timeout        = 60
      log_level      = "DEBUG"
      ses            = true
      dynamodb       = true
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
      name           = "${local.prefix}-authorizer"
      image_tag      = "1.0.3"
      timeout        = 10
      log_level      = "DEBUG"
      ses            = false
      dynamodb       = false
      ssm            = true
      github         = false
      verify         = false
      wordpress      = false
      invoke_backend = false
    }
  }

  github_backend_role_name = element(
    split("/", data.terraform_remote_state.oidc.outputs.github_actions_role_arns[local.functions.backend.name]),
    1,
  )

  github_lambda_policy_name = "${local.github_backend_role_name}-lambda"
}
