output "lab_backend_api_cert_arn" {
  description = "ARN of the ACM certificate (issued after 22-dns validation)"
  value       = aws_acm_certificate.lab_backend_api.arn
}

output "lab_backend_api_domain" {
  description = "API custom domain this certificate covers"
  value       = local.lab_backend_api_domain
}

output "acm_validation_records" {
  description = "DNS validation records for 22-dns"
  value = {
    for dvo in aws_acm_certificate.lab_backend_api.domain_validation_options : dvo.domain_name => {
      name  = dvo.resource_record_name
      type  = dvo.resource_record_type
      value = dvo.resource_record_value
    }
  }
}
