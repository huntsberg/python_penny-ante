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


if __name__ == "__main__":
    unittest.main()
