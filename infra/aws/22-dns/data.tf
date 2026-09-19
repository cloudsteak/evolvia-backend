data "terraform_remote_state" "certificates" {
  backend = "s3"

  config = {
    bucket  = "evolvia-platform-iac-state"
    key     = "aws/certificates/state.tfstate"
    region  = "eu-north-1"
    profile = "prod"
  }
}

data "terraform_remote_state" "ses" {
  backend = "s3"

  config = {
    bucket  = "evolvia-platform-iac-state"
    key     = "aws/ses/state.tfstate"
    region  = "eu-north-1"
    profile = "prod"
  }
}
