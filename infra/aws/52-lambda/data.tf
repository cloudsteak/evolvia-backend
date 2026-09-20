data "terraform_remote_state" "oidc" {
  backend = "s3"

  config = {
    bucket  = "evolvia-platform-iac-state"
    key     = "aws/oidc/state.tfstate"
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

data "terraform_remote_state" "dynamodb" {
  backend = "s3"

  config = {
    bucket  = "evolvia-platform-iac-state"
    key     = "aws/dynamodb/state.tfstate"
    region  = "eu-north-1"
    profile = "prod"
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "terraform_remote_state" "ecr" {
  backend = "s3"

  config = {
    bucket  = "evolvia-platform-iac-state"
    key     = "aws/ecr/state.tfstate"
    region  = "eu-north-1"
    profile = "prod"
  }
}
