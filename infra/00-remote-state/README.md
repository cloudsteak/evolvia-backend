# 00-remote-state

Átállás **1. lépése**. CLI script, nem OpenTofu — a state bucketnek a első `tofu init` előtt kell léteznie.

Részletek: [docs/steps/01-remote-state.md](../../docs/steps/01-remote-state.md).

```bash
AWS_PROFILE=prod ./aws-evolvia-platform-iac-state-bucket.sh
```

Következő layer: [12-oidc](../aws/12-oidc/README.md). Apply sorrend: lásd [infra/README.md](../README.md).
