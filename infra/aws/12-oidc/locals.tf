locals {
  oidc_host = "token.actions.githubusercontent.com"
  oidc_url  = "https://${local.oidc_host}"

  github_repos = toset(["evolvia-backend"])
}
