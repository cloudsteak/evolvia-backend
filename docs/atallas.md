# Átírás és átállás

K8s + Redis + Auth0 + cm-messenger (Brevo) → Lambda + API Gateway + DynamoDB + SES.

- Account: izolált platform / SES-prod (nem a lab/foundation account)
- Prod host: `backend.api.evolvia.hu` (`evolvia.hu` hosted zone, ebben az accountban)
- Infra: `infra/`, alkalmazáskód: `backend/`, `cleanup-trigger/`
- Layer terv: [docs/layers.md](./layers.md). Kisebbtől nagyobbig. 20–22, 34, 50, 52, 55, 60 kész. 22 alias catch-up: custom domain a 22-é, bind a 60-é.
- Layer adat: későbbi stack az előzőt `terraform_remote_state`-ből olvassa. Nincs másolt account ID / ARN változó.

Sorrend: **1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9**. A 8. (WordPress) a 7. (DNS) után, a 9. (K8s törlés) előtt.

| # | Lépés | Állapot | Dokumentum |
|---|--------|---------|------------|
| 1 | Remote state bucket | lefuttatva (`AWS_PROFILE=prod`) | [infra/00-remote-state](../infra/00-remote-state/README.md) |
| 2 | Infra tofu | 12–60 kész | [02-infra-tofu.md](./steps/02-infra-tofu.md) |
| 3 | Backend kódátírás | nincs | [03-kod.md](./steps/03-kod.md) |
| 4 | CI/CD | nincs | [04-cicd.md](./steps/04-cicd.md) |
| 5 | GitHub lab-ready kliens | nincs | [05-github-lab-ready.md](./steps/05-github-lab-ready.md) |
| 6 | Próba a next hoston | nincs | [06-proba.md](./steps/06-proba.md) |
| 7 | DNS átállás | nincs | [07-dns.md](./steps/07-dns.md) |
| 8 | WordPress lab-launcher | nincs | [08-wordpress.md](./steps/08-wordpress.md) |
| 9 | K8s és messenger törlése | nincs | [09-kivezetes.md](./steps/09-kivezetes.md) |
