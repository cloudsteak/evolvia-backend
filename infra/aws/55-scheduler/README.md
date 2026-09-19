# 55-scheduler

EventBridge Scheduler → 52 `cleanup:live`. `rate(15 minutes)`. Group: `{prefix}` (`evolvia`), nem `default`. Olvas: 12, 52. Nincs Route53.

`local.schedules` map — most egy kulcs: `cleanup`.

A group a schedule identity része: a `default` → `evolvia` váltás **cseréli** a schedule-t. Apply **60 előtt**.

## State

| | |
|---|---|
| Bucket | `evolvia-platform-iac-state` |
| Key | `aws/scheduler/state.tfstate` |
| Region | `eu-north-1` |
| Profile | `prod` |

## Apply (52 után)

```bash
cd infra/aws/55-scheduler
tofu init
tofu apply
```

## Név

- group: `{prefix}`
- schedule: `{prefix}-cleanup`
- role: `{prefix}-scheduler-{key}`
- policy: `{role}-lambda`

## Outputs

- `schedules`

## Következő layer

`60-backend` (apply kész).
