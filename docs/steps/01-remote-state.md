# 1. Remote state bucket

Egyszer, kézzel, az új platform accountban. A `tofu init` előtt kell léteznie.

## Mit hoz létre

- Bucket: `evolvia-platform-iac-state`
- Régió: `eu-north-1`
- Versioning, public access block, AES256

## Előfeltétel

AWS CLI profile: `prod` (platform / SES account). Ne a lab/foundation `evolvia` profile legyen.

## Futtatás

```bash
AWS_PROFILE=prod ./aws-evolvia-platform-iac-state-bucket.sh
```

A scriptet az `infra/00-remote-state` könyvtárból kell futtatni.

## Kész, ha

`aws s3api head-bucket --bucket evolvia-platform-iac-state` sikerül ezen a profile-on.

## Következő

[2. Infra tofu](./02-infra-tofu.md)
