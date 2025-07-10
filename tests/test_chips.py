import unittest

from .context import penny_ante
from penny_ante.chips import Chips


class TestChips(unittest.TestCase):
    # Require the table type or throw an exception
    def test_create_chips_count(self):
        test_chips = Chips()
        self.assertEqual(test_chips.count, 0)

    def test_create_chips_value(self):
        test_chips = Chips()
        self.assertEqual(test_chips.value, None)

    def test_create_chips_set_value(self):
        test_chips = Chips(value=1)
        self.assertEqual(test_chips.value, 1)

    def test_buy_chips_instantiate_value(self):
        test_chips = Chips(value=5)
        test_chips.change_chips(count=10)
        self.assertEqual(test_chips.cash_value(), 50)

    def test_buy_chips_set_value_at_add(self):
        test_chips = Chips()
        test_chips.change_chips(value=50, count=10)
        self.assertEqual(test_chips.cash_value(), 500)

    def test_buy_chips_change_value(self):
        test_chips = Chips(value=5)
        with self.assertRaises(Exception):
            test_chips.change_chips(value=10, count=1)

    def test_buy_chips_no_value_set(self):
        test_chips = Chips()
        with self.assertRaises(Exception):
            test_chips.change_chips(count=1)

    def test_add_chips(self):
        test_chips = Chips()
        test_chips.change_chips(value=50, count=10)
        test_chips.change_chips(count=10)
        self.assertEqual(test_chips.count, 20)

    def test_remove_chips(self):
        test_chips = Chips()
        test_chips.change_chips(value=50, count=10)
        test_chips.change_chips(count=-5)
        self.assertEqual(test_chips.count, 5)

    def test_remove_too_many_chips(self):
        test_chips = Chips()
        test_chips.change_chips(value=50, count=10)
        with self.assertRaises(Exception):
            test_chips.change_chips(count=-15)

    def test_cash_value_new(self):
        test_chips = Chips()
        self.assertEqual(test_chips.cash_value(), None)

    def test_cash_value_some_chips(self):
        test_chips = Chips()
        self.assertEqual(test_chips.cash_value(), None)


if __name__ == "__main__":
    unittest.main()
