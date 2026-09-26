# Harbor Stay on-call runbook

## Current system (Python monolith)

The confirmation flow now lives entirely in the Python monolith.

- **Entry point:** `harborstay/billing.py` → `confirm_reservation()`
- **Idempotency:** callers must pass the `Idempotency-Key` request header; the billing module records each key in its ledger before attempting a charge.
- **Duplicate charge investigation:** if a duplicate charge is reported, check that `Idempotency-Key` is being persisted in the ledger *before* `charge_card` is called. A missing or late write means a retry can reach `charge_card` a second time.

---

## Legacy billing-worker (LEGACY — pre-migration)

> **Warning:** The steps below describe the old Node.js billing-worker stack. They no longer reflect the running system. Do not use these paths for code changes or incident response.

## Symptom: duplicate charges on confirm

1. Check `services/billing-worker/confirm.js` for idempotency handling.
2. Restart deployment `billing-worker` in namespace `payments`.
3. If still failing, flip feature flag `CONFIRM_V2=true` in LaunchDarkly.

## Symptom: confirm timeouts

- Scale `billing-worker` replicas to 4.
- Purge Redis idempotency keys matching `confirm:*` (legacy).

## Escalation

Page **Payments Platform** if error rate on confirm > 2% for 10 minutes.

---

**Note for engineers:** Confirmation logic now lives in `harborstay/billing.py` in this repository. Update this runbook when you have time.
