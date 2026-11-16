# 21-ses

Átállás **2e**. Apply kész. A DNS rekordok a 22-ben vannak, az identity verified.

Az első apply pending identitynél visszatér. A [22-dns](../22-dns/README.md) írja a rekordokat és megvárja a verified státuszt. Most verified. 21 után 22, utána a 22-re nincs visszalépés.

Bejövő mail: az **apex `evolvia.hu` MX marad cPanel** (`0 evolvia.hu`). SES MX/SPF csak `bounce.evolvia.hu`.

Nem ide: Route53, SQS, Lambda IAM.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/ses/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

Előfeltétel: `20-certificates`. Apply kész. A Route53 rekord a 22-ben van.

## Apply

```bash
cd infra/aws/21-ses
tofu init
tofu apply
```

Új SES DNS érték után egyszer `22-dns` apply. Utána a 22-re nincs visszalépés.

## Outputs

- `mail_domain`
- `mail_identity_arn`
- `from_address`
- `mail_from_domain`
- `ses_dns_records` — a 22-es olvassa
