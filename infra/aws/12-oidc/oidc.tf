resource "aws_iam_openid_connect_provider" "github" {
  url             = local.oidc_url
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = []
}

resource "aws_iam_role" "github_actions" {
  for_each = local.github_repos

  name = "${var.prefix}-github-${each.key}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "${local.oidc_host}:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "${local.oidc_host}:sub" = [
              "repo:${var.github_org}/${each.key}:ref:refs/heads/main",
              "repo:${var.github_org}/${each.key}:pull_request",
            ]
          }
        }
      }
    ]
  })
}
