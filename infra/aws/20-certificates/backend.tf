terraform {
  backend "s3" {
    bucket  = "evolvia-platform-iac-state"
    key     = "aws/certificates/state.tfstate"
    region  = "eu-north-1"
    profile = "prod"

    # Native S3 lock feature, no need for DynamoDB
    use_lockfile = true
  }
}
