import unittest

from .context import penny_ante
from penny_ante.game import Game

class TestGame(unittest.TestCase):
    # Require the table type or throw an exception
    def test_throw_exception_if_table_type_is_not_set(self):
        with self.assertRaises(Exception):
            test_game = result = Game()

    def test_set_table_type_american(self):
        test_game = Game(table_type = 'AMERICAN')
        result = test_game.wheel.type
        self.assertEqual(result, 'AMERICAN')

    def test_set_table_type_european(self):
        test_game = Game(table_type = 'EUROPEAN')
        result = test_game.wheel.type
        self.assertEqual(result, 'EUROPEAN')

    def test_spin_wheel(self):
        test_game = Game(table_type = 'AMERICAN')
        test_game.spin_wheel()
        first_result = test_game.current_space.value
        test_game.spin_wheel()
        second_result = test_game.current_space.value
        self.assertNotEqual(first_result, second_result)

if __name__ == '__main__':
    unittest.main()