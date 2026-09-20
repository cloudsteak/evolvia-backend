resource "aws_cloudwatch_log_group" "this" {
  for_each = local.functions

  name              = "/aws/lambda/${each.value.name}"
  retention_in_days = 30
}

resource "aws_lambda_function" "this" {
  for_each = local.functions

  function_name = each.value.name
  role          = aws_iam_role.this[each.key].arn
  package_type  = "Image"
  image_uri     = "${local.ecr[each.key].url}:${each.value.image_tag}"
  architectures = ["x86_64"]
  memory_size   = 512
  timeout       = each.value.timeout
  publish       = true

  snap_start {
    apply_on = "PublishedVersions"
  }

  environment {
    variables = merge(
      {
        LOG_LEVEL = each.value.log_level
      },
      each.value.dynamodb ? {
        LABS_TABLE_NAME = data.terraform_remote_state.dynamodb.outputs.labs_table_name
      } : {},
      each.value.ses ? {
        SES_FROM_ADDRESS = data.terraform_remote_state.ses.outputs.from_address
      } : {},
      each.value.ssm ? {
        API_KEYS_PATH = local.api_keys_path
      } : {},
      each.value.github ? {
        GITHUB_REPO               = local.github_repo
        GITHUB_WORKFLOW_FILENAME  = local.github_workflow_filename
        GITHUB_TOKEN_PATH         = local.github_token_path
      } : {},
    )
  }

  depends_on = [aws_cloudwatch_log_group.this]

  timeouts {
    create = "15m"
    update = "15m"
  }

  lifecycle {
    precondition {
      condition     = each.value.image_tag != "" && lower(each.value.image_tag) != "latest"
      error_message = "functions[\"${each.key}\"].image_tag must be a pinned tag. latest is not allowed."
    }
  }
}

resource "aws_lambda_alias" "live" {
  for_each = local.functions

  name             = local.alias_name
  function_name    = aws_lambda_function.this[each.key].function_name
  function_version = aws_lambda_function.this[each.key].version
}
