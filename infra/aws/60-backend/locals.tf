locals {
  prefix     = data.terraform_remote_state.oidc.outputs.prefix
  api_name   = "${local.prefix}-backend"
  stage_name = "live"
  domain  = data.terraform_remote_state.dns.outputs.lab_backend_api_domain
  backend = data.terraform_remote_state.lambda.outputs.functions.backend

  routes = {
    root                = "GET /"
    health              = "GET /health"
    start_lab           = "POST /start-lab"
    lab_ready           = "POST /lab-ready"
    verify_lab          = "POST /verify-lab"
    lab_status_all      = "GET /lab-status/all"
    clean_up_lab        = "POST /clean-up-lab"
    lab_delete_internal = "POST /lab-delete-internal"
  }

  # Hívók: evolvia.hu (WP shortcode, böngésző) + github.com (Actions; Origin ritka, de ne felejtsük).
  cors_allow_origins = [
    "https://evolvia.hu",
    "https://github.com",
  ]
  cors_allow_methods = ["GET", "POST", "OPTIONS"]
  cors_allow_headers = ["Content-Type", "X-API-Key", "Authorization"]
}
