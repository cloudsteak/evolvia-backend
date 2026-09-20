moved {
  from = aws_ecr_repository.backend
  to   = aws_ecr_repository.this["backend"]
}

moved {
  from = aws_ecr_lifecycle_policy.backend
  to   = aws_ecr_lifecycle_policy.this["backend"]
}
