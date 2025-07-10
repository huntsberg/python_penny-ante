import unittest

from .context import penny_ante
from penny_ante.player import Player


class TestChips(unittest.TestCase):

    def test_create_player(self):
        test_player = Player(name="Bobby")
        self.assertEqual(test_player.name, "Bobby")


if __name__ == "__main__":
    unittest.main()
