resource "aws_iam_role" "this" {
  for_each = local.schedules

  name = "${local.prefix}-scheduler-${each.key}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "scheduler.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "invoke" {
  for_each = local.schedules

  name = "${aws_iam_role.this[each.key].name}-lambda"
  role = aws_iam_role.this[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["lambda:InvokeFunction"]
        Resource = [
          local.lambda[each.value.function].qualified_arn,
          local.lambda[each.value.function].arn,
        ]
      }
    ]
  })
}
