output "mail_domain" {
  description = "SES domain identity (verified after 22-dns records)"
  value       = aws_ses_domain_identity.mail.domain
}

output "mail_identity_arn" {
  description = "SES domain identity ARN"
  value       = aws_ses_domain_identity.mail.arn
}

output "from_address" {
  description = "Header From used by the lab-ready mailer"
  value       = local.from_address
}

output "mail_from_domain" {
  description = "Custom MAIL FROM / bounce domain"
  value       = local.mail_from_domain
}

output "ses_dns_records" {
  description = "DNS records for 22-dns. No Route53 in this layer."
  value = merge(
    {
      ses_verification = {
        name    = "_amazonses.${local.hosted_zone_name}"
        type    = "TXT"
        records = [aws_ses_domain_identity.mail.verification_token]
      }
      ses_mail_from_mx = {
        name    = local.mail_from_domain
        type    = "MX"
        records = ["10 feedback-smtp.${var.aws_region}.amazonses.com"]
      }
      ses_mail_from_spf = {
        name    = local.mail_from_domain
        type    = "TXT"
        records = ["v=spf1 include:amazonses.com ~all"]
      }
    },
    {
      for i, token in aws_ses_domain_dkim.mail.dkim_tokens :
      "ses_dkim_${i}" => {
        name    = "${token}._domainkey.${local.hosted_zone_name}"
        type    = "CNAME"
        records = ["${token}.dkim.amazonses.com"]
      }
    }
  )
}
