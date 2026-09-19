output "hosted_zone_id" {
  description = "Route53 hosted zone ID for evolvia.hu"
  value       = data.aws_route53_zone.evolvia.zone_id
}

output "hosted_zone_name" {
  description = "Route53 hosted zone name"
  value       = data.aws_route53_zone.evolvia.name
}

output "lab_backend_api_cert_arn" {
  description = "ARN of the DNS-validated ACM certificate"
  value       = aws_acm_certificate_validation.lab_backend_api.certificate_arn
}

output "lab_backend_api_domain" {
  description = "API custom domain (from 20-certificates)"
  value       = local.lab_backend_api_domain
}

output "lab_backend_api_target" {
  description = "API Gateway regional target for the alias"
  value       = aws_apigatewayv2_domain_name.lab_backend_api.domain_name_configuration[0].target_domain_name
}
