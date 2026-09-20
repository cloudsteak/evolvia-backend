locals {
  prefix     = data.terraform_remote_state.oidc.outputs.prefix
  api_name   = "${local.prefix}-backend"
  stage_name = "live"
  domain     = data.terraform_remote_state.dns.outputs.lab_backend_api_domain
  backend    = data.terraform_remote_state.lambda.outputs.functions.backend
  authorizer = data.terraform_remote_state.lambda.outputs.functions.authorizer

  routes = {
    root                = { key = "GET /", auth = true }
    health              = { key = "GET /health", auth = false }
    start_lab           = { key = "POST /start-lab", auth = true }
    lab_ready           = { key = "POST /lab-ready", auth = true }
    verify_lab          = { key = "POST /verify-lab", auth = true }
    lab_status_all      = { key = "GET /lab-status/all", auth = true }
    clean_up_lab        = { key = "POST /clean-up-lab", auth = true }
    lab_delete_internal = { key = "POST /lab-delete-internal", auth = true }
  }

  # Hívók: evolvia.hu (WP shortcode, böngésző) + github.com (Actions; Origin ritka, de ne felejtsük).
  cors_allow_origins = [
    "https://evolvia.hu",
    "https://github.com",
  ]
  cors_allow_methods = ["GET", "POST", "OPTIONS"]
  cors_allow_headers = ["Content-Type", "X-API-Key", "Authorization"]

  # Stage default — összes route. Túllépés: 429.
  throttle_rate  = 20
  throttle_burst = 50
}
