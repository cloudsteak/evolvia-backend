# 22-dns

**Egyedüli** `aws_route53_record` layer. ACM ISSUED, SES verified. Custom domain + alias: `backend.api.evolvia.hu`. **Olvas: 20, 21. Nem olvas 60-at.**

Apex `evolvia.hu` MX (cPanel) nem tofu. SES MX csak `bounce.evolvia.hu`.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/dns/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

## Apply

Önálló. 60 nem kell, 60 destroy után is ez a parancs:

```bash
cd infra/aws/22-dns
tofu apply
```

Létrehozza: custom domain (20 cert + név) + A/AAAA alias. Nincs import, nincs 60-as state.

Ha a `backend.api.evolvia.hu` domain még AWS-ben van (a 60 hozta létre), a create ütközik. Akkor előbb a 60-ból ki kell venni a domain-t (destroy a 60-nak, vagy csak annak a resource-nak). Utána a 22 apply **létrehozza**, nem importálja.

## Név

- domain / alias: `local.lab_backend_api_domain` (20)
- alias típus: `local.lab_backend_api_alias_types`

## Outputs

- `hosted_zone_id` / `hosted_zone_name`
- `lab_backend_api_cert_arn` (validált)
- `lab_backend_api_domain`
- `lab_backend_api_target`
