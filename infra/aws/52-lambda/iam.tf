resource "aws_iam_role" "this" {
  for_each = local.functions

  name = "${local.prefix}-lambda-${each.key}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "logs" {
  for_each = local.functions

  name = "${aws_iam_role.this[each.key].name}-logs"
  role = aws_iam_role.this[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Resource = "${aws_cloudwatch_log_group.this[each.key].arn}:*"
      }
    ]
  })
}

resource "aws_iam_role_policy" "dynamodb" {
  for_each = { for k, v in local.functions : k => v if v.dynamodb }

  name = "${aws_iam_role.this[each.key].name}-dynamodb"
  role = aws_iam_role.this[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
        ]
        Resource = [data.terraform_remote_state.dynamodb.outputs.labs_table_arn]
      }
    ]
  })
}

resource "aws_iam_role_policy" "ses" {
  for_each = { for k, v in local.functions : k => v if v.ses }

  name = "${aws_iam_role.this[each.key].name}-ses"
  role = aws_iam_role.this[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail",
        ]
        Resource = [data.terraform_remote_state.ses.outputs.mail_identity_arn]
      }
    ]
  })
}

resource "aws_iam_role_policy" "ssm" {
  for_each = { for k, v in local.functions : k => v if v.ssm }

  name = "${aws_iam_role.this[each.key].name}-ssm"
  role = aws_iam_role.this[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath",
        ]
        Resource = [
          "arn:aws:ssm:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:parameter${local.api_keys_path}",
          "arn:aws:ssm:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:parameter${local.api_keys_path}/*",
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "github_token" {
  for_each = { for k, v in local.functions : k => v if v.github }

  name = "${aws_iam_role.this[each.key].name}-ssm-github"
  role = aws_iam_role.this[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
        ]
        Resource = [
          "arn:aws:ssm:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:parameter${local.github_token_path}",
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "github_lambda" {
  name = local.github_lambda_policy_name
  role = local.github_backend_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:GetFunction",
          "lambda:GetFunctionConfiguration",
          "lambda:UpdateFunctionCode",
          "lambda:PublishVersion",
          "lambda:GetAlias",
          "lambda:UpdateAlias",
        ]
        Resource = flatten([
          for fn in aws_lambda_function.this : [fn.arn, "${fn.arn}:*"]
        ])
      }
    ]
  })
}
