"""Show the planted double-charge on a retried confirmation."""

from harborstay.billing import confirm_reservation, create_hold
from harborstay.store import Store


def main():
    store = Store()
    reservation = create_hold(
        store,
        guest_name="Dana Shah",
        room_type="harbor-queen",
        amount_cents=18400,
        card_token="tok_demo_dana",
    )
    key = "dana-retry-9f3"
    first = confirm_reservation(store, reservation["reservationId"], key)
    charges_after_first = len(store.charges)
    second = confirm_reservation(store, reservation["reservationId"], key)
    charges_after_retry = len(store.charges)
    print(f"reservation: {reservation['reservationId']}")
    print(f"first confirmation: {first['confirmationCode']} charges={charges_after_first}")
    print(f"retry confirmation: {second['confirmationCode']} charges={charges_after_retry}")
    print("expected charges after one retry with the same Idempotency-Key: 1")


if __name__ == "__main__":
    main()
