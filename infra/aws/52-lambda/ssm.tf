resource "aws_ssm_parameter" "api_keys" {
  for_each = local.api_key_names

  name  = "${local.api_keys_path}/${each.value}"
  type  = "SecureString"
  value = "replace-me"

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "github_token" {
  name  = local.github_token_path
  type  = "SecureString"
  value = "replace-me"

  lifecycle {
    ignore_changes = [value]
  }
}
