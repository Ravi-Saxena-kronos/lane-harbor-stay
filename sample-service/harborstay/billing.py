from harborstay.errors import Conflict, ReservationNotFound, SoldOut, ValidationError
from harborstay.inventory import has_room, reserve


def create_hold(store, guest_name, room_type, amount_cents, card_token):
    if not guest_name or not room_type or amount_cents <= 0 or not card_token:
        raise ValidationError("guestName, roomType, amountCents, and cardToken are required")
    if room_type not in store.rooms:
        raise ValidationError(f"Unknown room type: {room_type}")

    reservation_id = store.new_id()
    store.reservations[reservation_id] = {
        "reservationId": reservation_id,
        "guestName": guest_name,
        "roomType": room_type,
        "amountCents": amount_cents,
        "cardToken": card_token,
        "status": "held",
        "confirmation": None,
    }
    return store.reservations[reservation_id]


def charge_card(store, reservation):
    receipt = {
        "reservationId": reservation["reservationId"],
        "amountCents": reservation["amountCents"],
        "cardToken": reservation["cardToken"],
    }
    store.charges.append(receipt)
    return receipt


def confirm_reservation(store, reservation_id, idempotency_key):
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
