resource "aws_iam_role_policy" "tofu" {
  for_each = local.github_repos

  name = "${aws_iam_role.github_actions[each.key].name}-tofu"
  role = aws_iam_role.github_actions[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "State"
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetBucketLocation",
          "s3:GetBucketVersioning",
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:PutObject",
          "s3:DeleteObject",
        ]
        Resource = [
          "arn:aws:s3:::evolvia-platform-iac-state",
          "arn:aws:s3:::evolvia-platform-iac-state/*",
        ]
      },
      {
        Sid    = "Tofu"
        Effect = "Allow"
        Action = [
          "acm:*",
          "apigateway:*",
          "cloudwatch:*",
          "dynamodb:*",
          "ecr:*",
          "events:*",
          "iam:*",
          "lambda:*",
          "logs:*",
          "route53:*",
          "scheduler:*",
          "ses:*",
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath",
          "sts:GetCallerIdentity",
        ]
        Resource = "*"
      },
    ]
  })
}
