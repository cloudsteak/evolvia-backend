data "aws_route53_zone" "evolvia" {
  name         = local.hosted_zone_name
  private_zone = false
}

resource "aws_route53_record" "acm_validation" {
  for_each = data.terraform_remote_state.certificates.outputs.acm_validation_records

  allow_overwrite = true
  zone_id         = data.aws_route53_zone.evolvia.zone_id
  name            = each.value.name
  type            = each.value.type
  ttl             = 3600
  records         = [each.value.value]
}

# Blocks apply until ACM flips the 20-certificates cert PENDING → ISSUED.
# If it never issues, this apply fails and does not write a validated cert ARN.
resource "aws_acm_certificate_validation" "lab_backend_api" {
  certificate_arn         = data.terraform_remote_state.certificates.outputs.lab_backend_api_cert_arn
  validation_record_fqdns = [for record in aws_route53_record.acm_validation : record.fqdn]

  timeouts {
    create = "45m"
  }
}

resource "aws_route53_record" "ses" {
  for_each = data.terraform_remote_state.ses.outputs.ses_dns_records

  allow_overwrite = true
  zone_id         = data.aws_route53_zone.evolvia.zone_id
  name            = each.value.name
  type            = each.value.type
  ttl             = 3600
  records         = each.value.records
}

# Blocks until 21-ses domain identity is verified. Records must exist first.
resource "aws_ses_domain_identity_verification" "mail" {
  domain = data.terraform_remote_state.ses.outputs.mail_domain

  timeouts {
    create = "45m"
  }

  depends_on = [aws_route53_record.ses]
}

# Domain + alias a 22-ben. Olvas: 20 (cert, név). 60-at nem olvassa.
resource "aws_apigatewayv2_domain_name" "lab_backend_api" {
  domain_name = local.lab_backend_api_domain

  domain_name_configuration {
    certificate_arn = aws_acm_certificate_validation.lab_backend_api.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_route53_record" "lab_backend_api" {
  for_each = local.lab_backend_api_alias_types

  zone_id = data.aws_route53_zone.evolvia.zone_id
  name    = aws_apigatewayv2_domain_name.lab_backend_api.domain_name
  type    = each.value

  alias {
    name                   = aws_apigatewayv2_domain_name.lab_backend_api.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.lab_backend_api.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}
