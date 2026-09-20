# 7. DNS átállás

Még nincs implementálva. Új prod host: `backend.api.evolvia.hu` (hosted zone ebben az accountban). A régi `evolvia.api.cloud-mentor.hu` K8s-en marad, amíg a WordPress `backend_url` át nem vált.

| # | Mikor | Akció |
|---|--------|--------|
| 7a | 20-certificates + 22-dns apply | ACM validáció: `22-dns`. API alias: `60-backend` (zone a 22-ből). |
| 7b | −1 óra | Új lab tiltása. Drain vagy Redis → DynamoDB import. |
| 7c | flip | Nem a régi hostot vágjuk. A 5. lépés (GitHub) az új URL-re + X-API-Key. |
| 7d | +30 perc | Smoke a `backend.api.evolvia.hu`-n. `start-lab` a 8. után. |

A 8. lépés: WordPress `backend_url` + API kulcs. A régi `evolvia.api.cloud-mentor.hu` K8s-en marad rollbacknek, amíg a 9. ki nem vezeti.

Rollback: plugin `backend_url` vissza a régi hostra.

## Következő

[8. WordPress](./08-wordpress.md)
