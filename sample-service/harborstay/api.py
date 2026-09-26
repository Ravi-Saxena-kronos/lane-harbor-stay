import json

from harborstay.billing import confirm_reservation, create_hold
from harborstay.errors import Conflict, HarborError, ReservationNotFound, SoldOut, ValidationError


def health():
    return 200, {"service": "harbor-stay", "status": "ok", "version": "1.4.0"}


def post_reservation(store, body):
    try:
        reservation = create_hold(
            store,
            guest_name=body.get("guestName", ""),
            room_type=body.get("roomType", ""),
            amount_cents=int(body.get("amountCents") or 0),
            card_token=body.get("cardToken", ""),
        )
    except (ValidationError, ValueError) as exc:
        return 400, {"error": str(exc)}
    return 201, reservation


def post_confirm(store, reservation_id, idempotency_key):
    try:
        confirmation = confirm_reservation(store, reservation_id, idempotency_key)
    except ValidationError as exc:
        return 400, {"error": str(exc)}
    except ReservationNotFound as exc:
        return 404, {"error": str(exc)}
    except SoldOut as exc:
        return 409, {"error": f"Sold out: {exc}"}
    except Conflict as exc:
        return 409, {"error": str(exc)}
    except HarborError as exc:
        return 400, {"error": str(exc)}
    return 201, confirmation


def get_reservation(store, reservation_id):
    reservation = store.reservations.get(reservation_id)
    if reservation is None:
        return 404, {"error": reservation_id}
    public = {key: value for key, value in reservation.items() if key != "cardToken"}
    return 200, public


def encode(payload):
    return json.dumps(payload).encode("utf-8")
