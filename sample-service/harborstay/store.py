class Store:
    """In-memory reservations, charges, and room counts."""

    def __init__(self, rooms=None):
        self.reservations = {}
        self.idempotency = {}
        self.charges = []
        self.rooms = dict(rooms or {"harbor-queen": 2, "cedar-loft": 1})
        self._next_id = 1000

    def new_id(self):
        self._next_id += 1
        return f"HS-{self._next_id}"
