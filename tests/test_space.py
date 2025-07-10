import unittest

from .context import penny_ante
from penny_ante.space import Space


class TestSpace(unittest.TestCase):
    def test_throw_exception_if_value_is_not_set(self):
        with self.assertRaises(Exception):
            result = Space(None)  # type: ignore

    def test_instantiation_value(self):
        test_space = Space(value="00")
        self.assertEqual(test_space.value, "00")


if __name__ == "__main__":
    unittest.main()
