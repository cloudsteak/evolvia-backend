#!/usr/bin/env bash
# Bootstrap S3 bucket for OpenTofu remote state (platform account).
#
# Prerequisites:
#   - AWS CLI configured for the isolated platform / SES account
#   - AWS_PROFILE set to that account (do not use the lab/foundation profile)
#
# Usage:
#   AWS_PROFILE=prod ./aws-evolvia-platform-iac-state-bucket.sh
#
# Creates:
#   - Bucket: evolvia-platform-iac-state
#   - Versioning, public access block, AES256 default encryption

set -euo pipefail

AWS_REGION="eu-north-1"
BUCKET_NAME="evolvia-platform-iac-state"

echo ">> Creating S3 bucket: ${BUCKET_NAME} in ${AWS_REGION}"

aws s3api create-bucket \
  --bucket "${BUCKET_NAME}" \
  --region "${AWS_REGION}" \
  --create-bucket-configuration LocationConstraint="${AWS_REGION}"

echo ">> Enabling versioning"
aws s3api put-bucket-versioning \
  --bucket "${BUCKET_NAME}" \
  --versioning-configuration Status=Enabled

echo ">> Blocking public access"
aws s3api put-public-access-block \
  --bucket "${BUCKET_NAME}" \
  --public-access-block-configuration \
    'BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true'

echo ">> Enabling default SSE (AES256)"
aws s3api put-bucket-encryption \
  --bucket "${BUCKET_NAME}" \
  --server-side-encryption-configuration '{
    "Rules": [
      {
        "ApplyServerSideEncryptionByDefault": {
          "SSEAlgorithm": "AES256"
        }
      }
    ]
  }'

echo ">> Done."
