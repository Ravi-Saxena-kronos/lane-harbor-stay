class HarborError(Exception):
    """Base error for the reservation service."""


class ValidationError(HarborError):
    pass


class ReservationNotFound(HarborError):
    pass


class Conflict(HarborError):
    pass


class SoldOut(HarborError):
    pass
