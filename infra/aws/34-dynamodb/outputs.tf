output "labs_table_name" {
  description = "DynamoDB table name for lab records"
  value       = aws_dynamodb_table.labs.name
}

output "labs_table_arn" {
  description = "DynamoDB table ARN for lab records"
  value       = aws_dynamodb_table.labs.arn
}
