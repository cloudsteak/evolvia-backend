locals {
  prefix     = data.terraform_remote_state.oidc.outputs.prefix
  table_name = "${local.prefix}-platform-labs"
}
