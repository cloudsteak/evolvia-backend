# 20-certificates

Átállás **2b**. Apply kész. A cert a 22-es után **ISSUED**.

A 12-es kimenetére nincs szükség. A 22-es olvassa: `lab_backend_api_cert_arn`, `lab_backend_api_domain`, `acm_validation_records`.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/certificates/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

Előfeltétel: apply-olt `12-oidc`.

## Apply

```bash
cd infra/aws/20-certificates
tofu init
tofu apply
```

Az apply **visszatér a promptra**, amint a cert request létrejött. Státusz: `PENDING_VALIDATION`. Itt nincs waiter — a 22-es apply addig nem sikerül, amíg `ISSUED` nem lesz.

## Outputs

- `lab_backend_api_cert_arn`
- `lab_backend_api_domain`
- `acm_validation_records` — a 22-es remote state-ből olvassa, doksiba nem másoljuk

## Következő layer

`infra/aws/22-dns`
