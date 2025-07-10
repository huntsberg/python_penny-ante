import unittest

from .context import penny_ante
from penny_ante.space import Space


class TestSpace(unittest.TestCase):
    # Require the wheel type or throw an exception
    def test_throw_exception_if_all_values_are_not_set(self):
        with self.assertRaises(Exception):
            result = Space()

    def test_throw_exception_if_location_is_not_set(self):
        with self.assertRaises(Exception):
            result = Space(value="0", color="GREEN")

    def test_throw_exception_if_value_is_not_set(self):
        with self.assertRaises(Exception):
            result = Space(location=0, color="GREEN")

    def test_throw_exception_if_color_is_not_set(self):
        with self.assertRaises(Exception):
            result = Space(location=0, value="00")

    def test_instantiation_location(self):
        test_space = Space(location=0, value="00", color="GREEN")
        self.assertEqual(test_space.location, 0)

    def test_instantiation_value(self):
        test_space = Space(location=0, value="00", color="GREEN")
        self.assertEqual(test_space.value, "00")

    def test_instantiation_color(self):
        test_space = Space(location=0, value="00", color="GREEN")
        self.assertEqual(test_space.color, "GREEN")


if __name__ == "__main__":
    unittest.main()
