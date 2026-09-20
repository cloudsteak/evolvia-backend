output "repositories" {
  description = "ECR repos: name, url, arn — keyed like 52 functions"
  value = {
    for k, r in aws_ecr_repository.this : k => {
      name = r.name
      url  = r.repository_url
      arn  = r.arn
    }
  }
}

output "ecr_repository_url" {
  description = "Backend ECR URL (compat)"
  value       = aws_ecr_repository.this["backend"].repository_url
}

output "ecr_repository_arn" {
  description = "Backend ECR ARN (compat)"
  value       = aws_ecr_repository.this["backend"].arn
}
