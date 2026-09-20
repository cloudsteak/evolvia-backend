variable "aws_region" {
  default = "eu-north-1"
}

variable "aws_profile" {
  description = "AWS CLI profile for the platform / SES account"
  type        = string
  default     = "prod"
}

variable "default_tags" {
  type        = map(string)
  description = "Default tags to apply to all resources"
  default = {
    Environment = "Production"
    Project     = "Evolvia"
    ManagedBy   = "OpenTofu"
    Type        = "ses"
  }
}
