# 8. WordPress lab-launcher

Még nincs implementálva. Repo: `wordpress-plugins/lab-launcher`.

Utolsó kliens-változás: a 7. (DNS) után, a 9. (K8s törlés) előtt.

| # | Fájl | Mit |
|---|------|-----|
| 8a | `includes/api-caller.php` | Nincs `oauth/token`. Header: `X-API-Key`. |
| 8b | `includes/settings.php` | Auth0 mezők helyett `backend_api_key`. `backend_url` → `https://backend.api.evolvia.hu`. |
| 8c | TTL (ma 5400s) | Admin default, REST payload, countdown, expired — ugyanaz az új érték. |

TTL érintett: `admin/lab-admin-page.php`, `lab-launcher.php`, `includes/shortcode.php`. A már mentett labok az optionben a régi TTL-t tartják, amíg újra nem mented őket.

Nem nyúlunk: `status_webhook_token`, shortcode böngésző-hívás.

A plugin 90s-ot vár; az API Gateway ~29s-nál vág. A 6. lépésben mért p95 dönti el, kell-e Function URL.

## Következő

[9. Kivezetés](./09-kivezetes.md)
