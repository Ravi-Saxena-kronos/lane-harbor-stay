import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harborstay.api import post_confirm, post_reservation
from harborstay.billing import confirm_reservation, create_hold
from harborstay.errors import SoldOut
from harborstay.store import Store


class ReservationTests(unittest.TestCase):
    def test_create_and_confirm_once(self):
        store = Store()
        reservation = create_hold(store, "Mina Cole", "cedar-loft", 22000, "tok_mina")
        confirmation = confirm_reservation(store, reservation["reservationId"], "mina-once")
        self.assertEqual(confirmation["status"], "confirmed")
        self.assertEqual(len(store.charges), 1)
        self.assertEqual(store.rooms["cedar-loft"], 0)

    def test_confirm_unknown_reservation(self):
        status, body = post_confirm(Store(), "HS-missing", "key-1")
        self.assertEqual(status, 404)
        self.assertIn("error", body)

    def test_confirm_requires_idempotency_key(self):
        store = Store()
        status, reservation = post_reservation(
            store,
            {
                "guestName": "Jules Park",
                "roomType": "harbor-queen",
                "amountCents": 10000,
                "cardToken": "tok_jules",
            },
        )
        self.assertEqual(status, 201)
        status, body = post_confirm(store, reservation["reservationId"], "")
        self.assertEqual(status, 400)
        self.assertIn("Idempotency-Key", body["error"])

    def test_sold_out_does_not_charge(self):
        store = Store(rooms={"harbor-queen": 0})
        reservation = create_hold(store, "Ari Nguyen", "harbor-queen", 15000, "tok_ari")
        with self.assertRaises(SoldOut):
            confirm_reservation(store, reservation["reservationId"], "ari-1")
        self.assertEqual(store.charges, [])

    def test_confirm_retry_same_idempotency_key_single_charge(self):
        store = Store()
        reservation = create_hold(store, "Dana Shah", "harbor-queen", 18400, "tok_dana")
        key = "dana-retry-9f3"
        first = confirm_reservation(store, reservation["reservationId"], key)
        second = confirm_reservation(store, reservation["reservationId"], key)
        self.assertEqual(first["confirmationCode"], second["confirmationCode"])
        self.assertEqual(len(store.charges), 1)


if __name__ == "__main__":
    unittest.main()
