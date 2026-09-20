# 21-ses

Átállás **2e**. Apply kész. Identity pending, DNS a 22-esben.

Az apply **visszatér** pendingnél. A [22-dns](../22-dns/README.md) írja a rekordokat és megvárja a verified státuszt. 21 után 22, utána nincs vissza a 22-re.

Bejövő mail: az **apex `evolvia.hu` MX marad cPanel** (`0 evolvia.hu`). SES MX/SPF csak `bounce.evolvia.hu`.

Nem ide: Route53, SQS, Lambda IAM.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/ses/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

Előfeltétel a tiszta sorrendben: `20-certificates`. Most: 20 és 22 ACM már kész, a 21 kimaradt.

## Apply

```bash
cd infra/aws/21-ses
tofu init
tofu apply
```

Utána **egyszer** `22-dns` apply (SES DNS). Utána 22 tilos.

## Outputs

- `mail_domain`
- `mail_identity_arn`
- `from_address`
- `mail_from_domain`
- `ses_dns_records` — a 22-es olvassa
