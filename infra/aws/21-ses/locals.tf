locals {
  hosted_zone_name = "evolvia.hu"
  from_address     = "noreply@${local.hosted_zone_name}"
  # Subdomain only. Apex evolvia.hu MX is cPanel and must not be changed.
  mail_from_domain = "bounce.${local.hosted_zone_name}"
}
