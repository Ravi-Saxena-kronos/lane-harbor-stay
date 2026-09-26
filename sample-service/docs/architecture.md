# Harbor Stay architecture

Small Python service (stdlib HTTP in `harborstay/__main__.py`).

## Modules

| Module | Responsibility |
|--------|----------------|
| `harborstay/api.py` | HTTP mapping, status codes |
| `harborstay/billing.py` | Holds, card charges, confirmation, idempotency ledger |
| `harborstay/inventory.py` | Room availability |
| `harborstay/store.py` | In-memory state for demos and tests |
| `harborstay/errors.py` | Domain exceptions |

## Main flow

1. `POST /reservations` creates a **held** reservation (`create_hold`).
2. `POST /reservations/{id}/confirm` with header `Idempotency-Key` confirms and charges (`confirm_reservation`).

Contract reference: `openapi.yaml` (may not match runtime — check release gate).

## Tests

```bash
python -m unittest discover -s tests
```
