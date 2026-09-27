import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harborstay.inventory import has_room, reserve
from harborstay.store import Store


class HasRoomTests(unittest.TestCase):
    def test_returns_true_when_inventory_available(self):
        store = Store(rooms={"harbor-queen": 2})
        self.assertTrue(has_room(store, "harbor-queen"))

    def test_returns_false_when_inventory_is_zero(self):
        store = Store(rooms={"harbor-queen": 0})
        self.assertFalse(has_room(store, "harbor-queen"))

    def test_returns_false_for_unknown_room_type(self):
        store = Store(rooms={"harbor-queen": 2})
        self.assertFalse(has_room(store, "penthouse-suite"))

    def test_returns_true_when_exactly_one_room_left(self):
        store = Store(rooms={"cedar-loft": 1})
        self.assertTrue(has_room(store, "cedar-loft"))


class ReserveTests(unittest.TestCase):
    def test_returns_true_and_decrements_on_success(self):
        store = Store(rooms={"harbor-queen": 2})
        result = reserve(store, "harbor-queen")
        self.assertTrue(result)
        self.assertEqual(store.rooms["harbor-queen"], 1)

    def test_returns_false_when_inventory_is_zero(self):
        store = Store(rooms={"harbor-queen": 0})
        result = reserve(store, "harbor-queen")
        self.assertFalse(result)
        self.assertEqual(store.rooms["harbor-queen"], 0)  # not decremented below zero

    def test_returns_false_for_unknown_room_type(self):
        store = Store(rooms={"harbor-queen": 2})
        result = reserve(store, "penthouse-suite")
        self.assertFalse(result)
        self.assertNotIn("penthouse-suite", store.rooms)  # store not mutated

    def test_last_room_decrements_to_zero(self):
        store = Store(rooms={"cedar-loft": 1})
        result = reserve(store, "cedar-loft")
        self.assertTrue(result)
        self.assertEqual(store.rooms["cedar-loft"], 0)

    def test_sequential_reserves_exhaust_inventory(self):
        store = Store(rooms={"harbor-queen": 2})
        self.assertTrue(reserve(store, "harbor-queen"))
        self.assertTrue(reserve(store, "harbor-queen"))
        self.assertFalse(reserve(store, "harbor-queen"))
        self.assertEqual(store.rooms["harbor-queen"], 0)

    def test_reserve_does_not_affect_other_room_types(self):
        store = Store(rooms={"harbor-queen": 2, "cedar-loft": 1})
        reserve(store, "harbor-queen")
        self.assertEqual(store.rooms["cedar-loft"], 1)


if __name__ == "__main__":
    unittest.main()
