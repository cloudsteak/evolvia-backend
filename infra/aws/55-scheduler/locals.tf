locals {
  prefix     = data.terraform_remote_state.oidc.outputs.prefix
  group_name = local.prefix
  lambda     = data.terraform_remote_state.lambda.outputs.functions

  schedules = {
    cleanup = {
      name     = "${local.prefix}-cleanup"
      rate     = "30 minutes"
      function = "cleanup"
    }
  }
}
