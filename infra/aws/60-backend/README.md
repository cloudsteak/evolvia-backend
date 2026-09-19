# 60-backend

HTTP API. Integráció: 52 `backend:live`. Stage: `live`. Route-ok: `local.routes` (köztük `GET /health` → Lambda `{"status":"ok"}`). **Bind:** `api_mapping` → 22 `backend.api.evolvia.hu`. **Nincs Route53, nincs custom domain resource** (az a 22). **Nincs Lambda authorizer.**

Hívók: `https://evolvia.hu` (WP shortcode) és `https://github.com` (Actions). CORS; header: `Content-Type`, `X-API-Key`, `Authorization`.

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
- routes: `local.routes`

## Outputs

- `api_endpoint` (záró `/`)
- `custom_domain_name`
