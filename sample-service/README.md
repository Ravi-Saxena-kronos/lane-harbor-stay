# Harbor Stay (sample service)

Fictional inn reservation API for the **Lane** hackathon demo (Double Charge Club).

This repo is intentionally imperfect: a billing idempotency bug, OpenAPI drift, a stale runbook, and a dependency advisory fixture.

## Quick start

```bash
cd sample-service
python -m unittest discover -s tests -v
python -m harborstay.demo
python -m harborstay   # HTTP on http://127.0.0.1:8080
```

## Layout

| Path | Role |
|------|------|
| `harborstay/billing.py` | Holds, charges, confirms reservations |
| `harborstay/api.py` | HTTP handlers |
| `openapi.yaml` | Published contract (may drift from code) |
| `docs/architecture.md` | Accurate module map |
| `docs/runbook.md` | **Stale** on-call notes |
| `fixtures/` | Sample alert, ticket, advisory inputs for Lane |

## Demo story

Guest **Dana Shah** — confirm retried with the same `Idempotency-Key` after a timeout; card charged twice. See `fixtures/tickets/SUP-1187.md` and `fixtures/alerts/ALT-2041.json`.

License: MIT (see repository root).
