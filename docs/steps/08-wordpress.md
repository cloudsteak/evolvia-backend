# 8. WordPress lab-launcher

Repo: `wordpress-plugins/lab-launcher`. A plugin kód nincs ebben a repóban.

A hívás a 7. (DNS) után, a 9. (K8s törlés) előtt.

| # | Fájl | Mit |
|---|------|-----|
| 8a | `includes/api-caller.php` | Header: `X-API-Key`. Nincs token végpont. |
| 8b | `includes/settings.php` | `backend_api_key` = SSM `/prod/evolvia/api-keys/wordpress`. `backend_url` → `https://backend.api.evolvia.hu`. |
| 8c | TTL (ma 5400s) | Admin default, REST payload, countdown, expired — ugyanaz az új érték. |

TTL érintett: `admin/lab-admin-page.php`, `lab-launcher.php`, `includes/shortcode.php`. A már mentett labok az optionben a régi TTL-t tartják, amíg újra nem mented őket.

Nem nyúlunk: `status_webhook_token`, shortcode böngésző-hívás.

A plugin 90 s-ot vár. A backend Lambda timeout 60 s, az API Gateway integrációs limitje ~29 s. A 6. lépésben mért idő dönti el, kell-e Function URL.

## Következő

[9. Kivezetés](./09-kivezetes.md)
