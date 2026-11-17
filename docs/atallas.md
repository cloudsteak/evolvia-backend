# Átírás és átállás

K8s + Redis + Auth0 + cm-messenger (Brevo) → Lambda + API Gateway + DynamoDB + SES.

- Account: izolált platform / SES-prod (nem a lab/foundation account)
- Prod host: `backend.api.evolvia.hu` (`evolvia.hu` hosted zone, ebben az accountban)
- Infra: `infra/`. Alkalmazáskód: `backend/`, `cleanup-trigger/`, `authorizer/`
- Layer terv: [docs/layers.md](./layers.md). Kisebbtől nagyobbig. 12–60 apply kész. Minden Lambda a 52-ben.
- Layer adat: későbbi stack az előzőt `terraform_remote_state`-ből olvassa. Nincs másolt account ID / ARN változó.

Sorrend: **1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9**. Az 5. és a 8. a hívók (forge, WordPress). A 9. a régi K8s és a GHCR workflow.

| # | Lépés | Állapot | Dokumentum |
|---|--------|---------|------------|
| 1 | Remote state bucket | kész | [infra/00-remote-state](../infra/00-remote-state/README.md) |
| 2 | Infra tofu | 12–60 apply kész | [02-infra-tofu.md](./steps/02-infra-tofu.md) |
| 3 | Backend kód | kész. Kulcs-scope később | [03-kod.md](./steps/03-kod.md) |
| 4 | CI/CD | kész. A GHCR workflow a 9-ig még fut | [04-cicd.md](./steps/04-cicd.md) |
| 5 | GitHub lab-ready kliens | a forge repóban | [05-github-lab-ready.md](./steps/05-github-lab-ready.md) |
| 6 | Próba | checklist, prod host | [06-proba.md](./steps/06-proba.md) |
| 7 | DNS | új host a 22-ben kész. Hívóváltás az 5. és a 8. | [07-dns.md](./steps/07-dns.md) |
| 8 | WordPress lab-launcher | a plugin repóban | [08-wordpress.md](./steps/08-wordpress.md) |
| 9 | K8s és messenger törlése | nyitott | [09-kivezetes.md](./steps/09-kivezetes.md) |
