import unittest

from .context import penny_ante
from penny_ante.player import Player


class TestPlayer(unittest.TestCase):

    def test_create_player(self):
        test_player = Player(name="Bobby")
        self.assertEqual(test_player.name, "Bobby")

    def test_buy_chips_no_value(self):
        test_player = Player(name="Bobby")
        test_player.buy_chips(count=1)
        self.assertEqual(test_player.chips.cash_value(), 1)


if __name__ == "__main__":
    unittest.main()
