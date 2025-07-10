import unittest

from .context import penny_ante
from penny_ante.game import Game
from penny_ante.space import Space


class TestGame(unittest.TestCase):
    # Require the table type or throw an exception
    def test_throw_exception_if_table_type_is_not_set(self):
        with self.assertRaises(Exception):
            test_game = Game(None)

    def test_set_table_type_american(self):
        test_game = Game(table_type="AMERICAN")
        self.assertEqual(test_game.table.wheel.type, "AMERICAN")

    def test_set_table_type_european(self):
        test_game = Game(table_type="EUROPEAN")
        self.assertEqual(test_game.table.wheel.type, "EUROPEAN")

    def test_spin_wheel(self):
        test_game = Game(table_type="AMERICAN")
        test_game.spin_wheel()
        self.assertIsInstance(test_game.table.wheel.current_space, Space)

    def test_add_single_player(self):
        test_game = Game(table_type="AMERICAN")
        test_game.add_player(player_name="Billy")
        self.assertEqual(len(test_game.players), 1)
        self.assertEqual(test_game.players["Billy"].name, "Billy")

    def test_add_multiple_players(self):
        test_game = Game(table_type="AMERICAN")
        test_game.add_player(player_name="Billy")
        test_game.add_player(player_name="Bobby")
        self.assertEqual(len(test_game.players), 2)

    def test_only_one_player_per_name(self):
        test_game = Game(table_type="AMERICAN")
        test_game.add_player(player_name="Billy")
        with self.assertRaises(Exception):
            test_game.add_player(player_name="Billy")


if __name__ == "__main__":
    unittest.main()
