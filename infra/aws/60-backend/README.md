# 60-backend

HTTP API. Integráció: 52 `backend:live`. Stage: `live`. **Authorizer:** 52 `authorizer:live`, `X-API-Key` → SSM. `GET /health` nyitva, a többi route CUSTOM. **Bind:** `api_mapping` → 22 `backend.api.evolvia.hu`. **Nincs Route53, nincs custom domain resource** (az a 22).

Hívók: `https://evolvia.hu` (WP shortcode) és `https://github.com` (Actions). CORS; header: `Content-Type`, `X-API-Key`, `Authorization`.

Scope később: wordpress/github ne érje el a `lab-status/all` / cleanup / delete-t — [03-kod](../../../docs/steps/03-kod.md).

Olvas: 12, 22, 52.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/backend/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

## Apply (22 után)

A 22-ben már legyen a custom domain + alias. A 60 csak bindel.

```bash
cd infra/aws/60-backend
tofu apply
```

Ha a domain még ebben a state-ben van: előbb `tofu destroy` (vagy a 60 egész), aztán 22 apply (létrehozza a domain-t), aztán 60 apply (API + mapping).

## Név

- API: `local.api_name`
- domain: `local.domain` (22)
- stage: `live`
- throttle: `local.throttle_rate` / `local.throttle_burst` (20 rps / 50 burst)
- routes: `local.routes`

## Outputs

- `api_endpoint` (záró `/`)
- `custom_domain_name`
