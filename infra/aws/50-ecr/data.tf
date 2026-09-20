data "terraform_remote_state" "oidc" {
  backend = "s3"

  config = {
    bucket  = "evolvia-platform-iac-state"
    key     = "aws/oidc/state.tfstate"
    region  = "eu-north-1"
    profile = "prod"
  }
}
