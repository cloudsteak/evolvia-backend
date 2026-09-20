# 12-oidc

Átállás **2a**. Apply kész. Következő: 20-certificates (kész).

GitHub Actions OIDC provider + deploy role az `evolvia-backend` repóra (`main` és `pull_request`). ECR push joga a 50-ben, Lambda update a 52-ben, tofu plan/apply a 12 `{role}-tofu` policyban.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/oidc/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

Előfeltétel: [1. remote state](../../../docs/steps/01-remote-state.md).

## Apply

```bash
cd infra/aws/12-oidc
tofu init
tofu apply
```

## Outputs

- `github_actions_role_arns`
- `oidc_provider_arn`
- `prefix` — későbbi layerek remote state-ből olvassák

A 12-es apply után a `prefix` output új. Ha a state-ben még nincs, egy újabb `tofu apply` (0 resource).

## Következő layer

`infra/aws/20-certificates`
