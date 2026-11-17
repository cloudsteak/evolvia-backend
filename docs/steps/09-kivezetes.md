# 9. K8s és messenger törlése

Nyitott. Csak ha a 8. lépés éles és 24–72 órája stabil.

| # | Hol | Mit |
|---|-----|-----|
| 9a | cm-companion | `evolvia-backend-prod`: sync ki, majd törlés (core, cleanup, redis, ingress) |
| 9b | cm-companion | `cm-messenger` törlése, ha nincs más hívó |
| 9c | cluster Parameter Store | `/prod/app/evolvia-backend-core/*` és cleanup credentials |
| 9d | evolvia-backend | `docker-build-lab-*.yml`, `backend/Dockerfile`, `cleanup-trigger/Dockerfile`. A `Dockerfile.lambda` marad |
| 9e | Auth0 | M2M app / API, ha más rendszer nem használja |

Rollback a 9. előtt: a hívó URL-je vissza a régi hostra. Az új accounton indult labokra utána még egyszer futtasd a cleanup Lambdát.
