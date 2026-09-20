# Request only. Apply returns while the cert is PENDING_VALIDATION.
# Do not add aws_acm_certificate_validation here — that waiter is 22-dns.
resource "aws_acm_certificate" "lab_backend_api" {
  domain_name       = local.lab_backend_api_domain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}
