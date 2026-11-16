# 7. DNS átállás

Az új host a [22-dns](../../infra/aws/22-dns/README.md)-ben apply kész: `backend.api.evolvia.hu`. Custom domain és A/AAAA alias a 22-ben. A [60-backend](../../infra/aws/60-backend/README.md) csak bind (`api_mapping`).

A régi `evolvia.api.cloud-mentor.hu` a hívók átállásáig marad. A hívóváltás az 5. (GitHub) és a 8. (WordPress).

| # | Mikor | Akció |
|---|--------|--------|
| 7a | kész | ACM és alias: 22. Bind: 60. |
| 7b | flip előtt | Új lab a régi hoston ne induljon. A lab állapot DynamoDB. |
| 7c | flip | Az 5. lépés az új URL + `X-API-Key`. |
| 7d | flip után | Smoke a `backend.api.evolvia.hu`-n. `start-lab` a 8. után. |

Rollback: a hívó URL-je vissza a régi hostra. A 22 aliasát nem bontjuk.

## Következő

[8. WordPress](./08-wordpress.md)
