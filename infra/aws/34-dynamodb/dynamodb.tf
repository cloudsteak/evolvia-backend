resource "aws_dynamodb_table" "labs" {
  name         = local.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "username"

  attribute {
    name = "username"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  # Do not enable DynamoDB TTL. Lab expiry is application logic
  # (started_at + lab_ttl) plus GitHub destroy. Native TTL would drop
  # items without tearing down the lab account.
}
