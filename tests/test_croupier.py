import unittest

from .context import penny_ante
from penny_ante.croupier import Croupier
from penny_ante.table import Table
from penny_ante.space import Space


class TestCroupier(unittest.TestCase):
    # Require the table type or throw an exception

    def test_spin_wheel(self):
        test_croupier = Croupier(table=Table(table_type="AMERICAN"))
        test_croupier.spin_wheel()
        self.assertIsInstance(test_croupier.table.wheel.current_space, Space)


if __name__ == "__main__":
    unittest.main()
