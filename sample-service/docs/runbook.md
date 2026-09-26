# Harbor Stay on-call runbook (OUTDATED)

> **Warning:** This runbook predates the Python monolith. Do not use paths below for code changes.

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
