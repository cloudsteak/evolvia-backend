# 5. GitHub lab-ready kliens

A forge `lab-ready-callback` Auth0 helyett `X-API-Key`. A reusable WF `@main`-t hív — merge kell, különben a régi callback fut.

GitHub (evolvia-forge):

| | Mit |
|--|-----|
| Variable `BACKEND_HOST` | `backend.api.evolvia.hu` (nincs `https://`) |
| Secret `BACKEND_API_KEY` | SSM `/prod/evolvia/api-keys/github` |

Auth0 secret/var a callbackhoz nem kell.

## Következő

[6. Próba](./06-proba.md)
