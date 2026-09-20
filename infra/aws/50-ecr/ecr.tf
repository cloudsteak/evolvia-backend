resource "aws_ecr_repository" "this" {
  for_each = local.repositories

  name                 = each.value.name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }
}

resource "aws_ecr_lifecycle_policy" "this" {
  for_each = local.repositories

  repository = aws_ecr_repository.this[each.key].name
  policy     = local.ecr_lifecycle_policy
}

resource "aws_iam_role_policy" "github_ecr" {
  name = local.github_ecr_policy_name
  role = local.github_backend_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ecr:GetAuthorizationToken"]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
        ]
        Resource = [for r in aws_ecr_repository.this : r.arn]
      }
    ]
  })
}
