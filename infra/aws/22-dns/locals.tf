locals {
  hosted_zone_name       = "evolvia.hu"
  lab_backend_api_domain = data.terraform_remote_state.certificates.outputs.lab_backend_api_domain
  lab_backend_api_alias_types = toset(["A", "AAAA"])
}
