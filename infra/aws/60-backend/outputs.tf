output "api_endpoint" {
  description = "execute-api URL (stage a pathban, záró / kell a GET / -hoz)"
  value       = "${aws_apigatewayv2_api.this.api_endpoint}/${aws_apigatewayv2_stage.this.name}/"
}

output "stage_name" {
  value = aws_apigatewayv2_stage.this.name
}

output "custom_domain_name" {
  description = "API hostname — alias a 22-ben, bind itt"
  value       = local.domain
}
