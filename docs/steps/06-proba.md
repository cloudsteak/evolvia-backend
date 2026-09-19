# 6. Próba a next hoston

Még nincs implementálva.

Host: `backend-next.api.evolvia.hu`. A régi prod (`evolvia.api.cloud-mentor.hu`) még K8s. A WordPress prod plugint itt ne cseréld.

## Ellenőrzés

- Authorizer: rossz kulcs 401, jó kulcs 200 a `GET /`-re
- `start-lab`: DynamoDB item + GitHub apply
- `lab-ready`: SES levél, ugyanaz a HTML
- `verify-lab`: proxy; API Gateway ~29s limit mérése
- Cleanup: manuális invoke

## Következő

[7. DNS](./07-dns.md)
