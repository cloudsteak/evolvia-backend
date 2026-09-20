output "functions" {
  description = "Lambda functions: name, arns, image_uri, alias"
  value = {
    for k, fn in aws_lambda_function.this : k => {
      name          = fn.function_name
      arn           = fn.arn
      image_uri     = fn.image_uri
      invoke_arn    = aws_lambda_alias.live[k].invoke_arn
      qualified_arn = aws_lambda_alias.live[k].arn
    }
  }
}

output "function_name" {
  description = "Backend Lambda name"
  value       = aws_lambda_function.this["backend"].function_name
}

output "invoke_arn" {
  description = "Backend alias invoke ARN for API Gateway (60)"
  value       = aws_lambda_alias.live["backend"].invoke_arn
}

output "qualified_arn" {
  description = "Backend alias ARN"
  value       = aws_lambda_alias.live["backend"].arn
}

output "cleanup_qualified_arn" {
  description = "Cleanup alias ARN for 55-scheduler"
  value       = aws_lambda_alias.live["cleanup"].arn
}
