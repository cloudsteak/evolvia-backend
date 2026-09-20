# 34-dynamodb

Átállás **2d**. Apply kész. Tábla: `evolvia-platform-labs`, PK `username`.

Nem ide: SQL (`30–33`), Redis (`37`), egyéb db (`38–39`). Nincs DynamoDB TTL: a lejárat app-logika + GitHub destroy.

Olvas: 12 (prefix). A 52-es Lambda olvassa a tábla nevét / ARN-t.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/dynamodb/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

Előfeltétel: apply-olt `12-oidc` és `22-dns`. A 30–33 SQL nincs, kihagyható.

## Apply

```bash
cd infra/aws/34-dynamodb
tofu init
tofu apply
```

## Outputs

- `labs_table_name`
- `labs_table_arn`

## Következő layer

`infra/aws/21-ses` (a 22 előtt; a 34 után a tiszta sorrendben a 50 jön).
