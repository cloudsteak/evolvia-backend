variable "aws_region" {
  default = "eu-north-1"
}

variable "aws_profile" {
  description = "AWS CLI profile for the platform / SES account"
  type        = string
  default     = "prod"
}

variable "prefix" {
  description = "Resource prefix"
  type        = string
  default     = "evolvia"
}

variable "github_org" {
  description = "GitHub organization name"
  type        = string
  default     = "cloudsteak"
}

variable "default_tags" {
  type        = map(string)
  description = "Default tags to apply to all resources"
  default = {
    Environment = "Production"
    Project     = "Evolvia"
    ManagedBy   = "OpenTofu"
    Type        = "oidc"
  }
}
