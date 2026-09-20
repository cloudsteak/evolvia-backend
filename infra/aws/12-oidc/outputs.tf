output "github_actions_role_arns" {
  description = "Map of GitHub repo name to IAM role ARN"
  value       = { for k, v in aws_iam_role.github_actions : k => v.arn }
}

output "oidc_provider_arn" {
  description = "ARN of the GitHub Actions OIDC provider"
  value       = aws_iam_openid_connect_provider.github.arn
}

output "prefix" {
  description = "Resource prefix for downstream layers"
  value       = var.prefix
}

