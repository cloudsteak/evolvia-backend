# 6. Próba

Host: `https://backend.api.evolvia.hu`. Külön next hostname nincs a tofu-ban. A WordPress `backend_url` cseréje a 8. lépés.

## Ellenőrzés

- Authorizer: rossz kulcs 401, jó kulcs 200 a `GET /`-re
- `start-lab`: DynamoDB item + GitHub apply
- `lab-ready`: SES levél, feladó `Cloud Mentor <noreply@evolvia.hu>`
- `verify-lab`: proxy. A backend Lambda timeout 60 s; az API Gateway integrációs limitje ~29 s
- Cleanup: a `cleanup:live` invoke, vagy megvárni a 30 perces schedulert

## Következő

[7. DNS](./07-dns.md)
