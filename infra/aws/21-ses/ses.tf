resource "aws_ses_domain_identity" "mail" {
  domain = local.hosted_zone_name
}

resource "aws_ses_domain_dkim" "mail" {
  domain = aws_ses_domain_identity.mail.domain
}

# MAIL FROM resource only. MX/SPF Route53 records are 22-dns on bounce.*,
# never on the apex — inbound MX stays cPanel (evolvia.hu → 0 evolvia.hu).
resource "aws_ses_domain_mail_from" "mail" {
  domain                 = aws_ses_domain_identity.mail.domain
  mail_from_domain       = local.mail_from_domain
  behavior_on_mx_failure = "UseDefaultValue"
}
