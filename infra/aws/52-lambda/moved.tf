moved {
  from = aws_cloudwatch_log_group.backend
  to   = aws_cloudwatch_log_group.this["backend"]
}

moved {
  from = aws_lambda_function.backend
  to   = aws_lambda_function.this["backend"]
}

moved {
  from = aws_lambda_alias.live
  to   = aws_lambda_alias.live["backend"]
}

moved {
  from = aws_iam_role.backend
  to   = aws_iam_role.this["backend"]
}

moved {
  from = aws_iam_role_policy.backend_logs
  to   = aws_iam_role_policy.logs["backend"]
}

moved {
  from = aws_iam_role_policy.backend_dynamodb
  to   = aws_iam_role_policy.dynamodb["backend"]
}

moved {
  from = aws_iam_role_policy.backend_ses
  to   = aws_iam_role_policy.ses["backend"]
}
