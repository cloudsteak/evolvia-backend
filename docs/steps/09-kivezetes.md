# 9. K8s és messenger törlése

Még nincs implementálva. Csak ha a 8. lépés éles és 24–72 órája stabil.

| # | Hol | Mit |
|---|-----|-----|
| 9a | cm-companion | `evolvia-backend-prod`: sync ki, majd törlés (core, cleanup, redis, ingress) |
| 9b | cm-companion | `cm-messenger` törlése, ha nincs más hívó |
| 9c | cluster Parameter Store | `/prod/app/evolvia-backend-core/*` és cleanup credentials |
| 9d | evolvia-backend | `docker-build-*.yml`, Dockerfile-ok |
| 9e | Auth0 | M2M app / API, ha más nem használja |

Rollback a 9. előtt: DNS CNAME a K8s-re + plugin Auth0 / régi verzió. Az új accounton indult labokra utána még egyszer futtasd a cleanup Lambdát.
