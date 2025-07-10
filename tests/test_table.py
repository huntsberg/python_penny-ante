import unittest

from .context import penny_ante
from penny_ante.table import Table
from penny_ante.space import Space


class TestTable(unittest.TestCase):
    # Require the table type or throw an exception
    def test_create_table_american(self):
        test_table = Table(table_type="AMERICAN")
        self.assertEqual(test_table.wheel.type, "AMERICAN")
        self.assertEqual(test_table.layout.type, "AMERICAN")

    def test_create_table_european(self):
        test_table = Table(table_type="EUROPEAN")
        self.assertEqual(test_table.wheel.type, "EUROPEAN")
        self.assertEqual(test_table.layout.type, "EUROPEAN")

    def test_spin_wheel(self):
        test_table = Table(table_type="EUROPEAN")
        test_table.spin_wheel()
        self.assertIsInstance(test_table.wheel.current_space, Space)


if __name__ == "__main__":
    unittest.main()
