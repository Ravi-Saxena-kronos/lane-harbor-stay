from __future__ import annotations

import re
import subprocess
from pathlib import Path

BUG_MARKER = "BUG: charge runs before idempotency"

CONFIRM_FIXED = '''def confirm_reservation(store, reservation_id, idempotency_key):
    if not idempotency_key:
        raise ValidationError("Idempotency-Key is required")

    reservation = store.reservations.get(reservation_id)
    if reservation is None:
        raise ReservationNotFound(reservation_id)
    if reservation["status"] == "cancelled":
        raise Conflict("Reservation is cancelled")

    prior = store.idempotency.get(idempotency_key)
    if prior is not None:
        return prior

    if reservation["status"] == "confirmed" and reservation["confirmation"] is not None:
        return reservation["confirmation"]

    if not has_room(store, reservation["roomType"]):
        raise SoldOut(reservation["roomType"])

    charge_card(store, reservation)

    if not reserve(store, reservation["roomType"]):
        raise SoldOut(reservation["roomType"])

    confirmation = {
        "reservationId": reservation_id,
        "status": "confirmed",
        "confirmationCode": f"CNF-{reservation_id[-4:]}",
        "chargedCents": reservation["amountCents"],
    }
    reservation["status"] = "confirmed"
    reservation["confirmation"] = confirmation
    store.idempotency[idempotency_key] = confirmation
    return confirmation
'''

IDEMPOTENCY_TEST = '''
    def test_confirm_retry_same_idempotency_key_single_charge(self):
        store = Store()
        reservation = create_hold(store, "Dana Shah", "harbor-queen", 18400, "tok_dana")
        key = "dana-retry-9f3"
        first = confirm_reservation(store, reservation["reservationId"], key)
        second = confirm_reservation(store, reservation["reservationId"], key)
        self.assertEqual(first["confirmationCode"], second["confirmationCode"])
        self.assertEqual(len(store.charges), 1)
'''


def billing_has_bug(billing_path: Path) -> bool:
    if not billing_path.is_file():
        return False
    return BUG_MARKER in billing_path.read_text(encoding="utf-8")


def apply_billing_fix(billing_path: Path) -> bool:
    """Return True if file was modified."""
    text = billing_path.read_text(encoding="utf-8")
    if BUG_MARKER not in text:
        return False

    pattern = r"def confirm_reservation\(store, reservation_id, idempotency_key\):[\s\S]*$"
    if not re.search(pattern, text):
        raise RuntimeError("Could not locate confirm_reservation in billing.py")

    new_text = re.sub(pattern, CONFIRM_FIXED.strip() + "\n", text, count=1)
    billing_path.write_text(new_text, encoding="utf-8")
    return True


def apply_regression_test(test_path: Path) -> bool:
    """Return True if test was added."""
    text = test_path.read_text(encoding="utf-8")
    if "test_confirm_retry_same_idempotency_key_single_charge" in text:
        return False

    anchor = "\n\nif __name__ == \"__main__\":"
    if anchor not in text:
        raise RuntimeError("Could not insert idempotency test in test_reservations.py")

    text = text.replace(anchor, IDEMPOTENCY_TEST + anchor)
    test_path.write_text(text, encoding="utf-8")
    return True


def run_tests(repo_root: Path, test_command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        test_command,
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
