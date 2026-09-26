# Demo seed (Double Charge Club — do not feed to agents as sole source)

## Planted bug

`confirm_reservation` in `harborstay/billing.py` calls `charge_card` **before** checking `store.idempotency`. Retries with the same key return the cached confirmation but append another charge.

## Fix direction

Check idempotency (or return early if already confirmed) **before** charging. Add test `test_confirm_retry_same_idempotency_key_single_charge`.

## Fixtures

- Ticket: `fixtures/tickets/SUP-1187.md`
- Alert: `fixtures/alerts/ALT-2041.json`
- Advisory: `fixtures/advisories/HARBOR-2026-014.json`

## Demo commands

```bash
python -m unittest discover -s tests
python -m harborstay.demo
```
