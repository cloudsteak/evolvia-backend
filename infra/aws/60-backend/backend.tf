terraform {
  backend "s3" {
    bucket  = "evolvia-platform-iac-state"
    key     = "aws/backend/state.tfstate"
    region  = "eu-north-1"
    profile = "prod"

    use_lockfile = true
  }
}
