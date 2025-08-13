import unittest
import tempfile
import os

from .context import penny_ante
from penny_ante.game import Game
from penny_ante.bet import Bet, BetType
from penny_ante.player import Player
from penny_ante.chips import Chips
from penny_ante.betting_rules import BettingRules


class TestBetEnforcement(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.game = Game(table_type="AMERICAN")
        self.game.add_player("Alice")
        self.game.add_player("Bob")

        # Give players some chips
        alice = self.game.players["Alice"]
        alice.buy_chips(count=1000, value=1)

        bob = self.game.players["Bob"]
        bob.buy_chips(count=500, value=1)

        # Create a temporary config for testing limits
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_limits.yaml")

        # Test configuration with strict limits
        self.test_config = """
payout_ratios:
  straight_up: 35
  split: 17
  red: 1
  black: 1
  first_dozen: 2

minimum_bet_ratios:
  global: 1.0
  straight_up: 1.0
  red: 5.0

maximum_bet_ratios:
  global: 1.0
  straight_up: 0.1  # Very restrictive
  red: 0.5

table_limits:
  minimum_bet: 10
  maximum_bet: 1000
  maximum_total_bet: 2000  # Low limit for testing

game_rules:
  en_prison: false
  la_partage: false
  surrender: false
  maximum_repeats: 10

special_rules:
  allow_call_bets: false
  allow_neighbor_bets: false
  progressive_betting: true
  maximum_parlay: 5
"""

        with open(self.config_path, "w") as f:
            f.write(self.test_config)

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)

    def test_individual_bet_amount_limits(self):
        """Test that individual bet amounts are enforced."""
        # Create game with strict limits
        strict_game = Game(table_type="AMERICAN", betting_rules_config=self.config_path)

        # Test minimum bet enforcement
        with self.assertRaises(ValueError) as context:
            bet = Bet.create_straight_up_bet(
                "17",
                amount=5,
                layout=strict_game.table.layout,
                betting_rules=strict_game.betting_rules,
            )
        self.assertIn("outside allowed range", str(context.exception))

        # Test maximum bet enforcement
        with self.assertRaises(ValueError) as context:
            bet = Bet.create_straight_up_bet(
                "17",
                amount=500,  # Max is 100 (1000 * 0.1)
                layout=strict_game.table.layout,
                betting_rules=strict_game.betting_rules,
            )
        self.assertIn("outside allowed range", str(context.exception))

        # Test valid bet
        bet = Bet.create_straight_up_bet(
            "17",
            amount=50,
            layout=strict_game.table.layout,
            betting_rules=strict_game.betting_rules,
        )
        self.assertEqual(bet.amount, 50)

    def test_total_bet_limit_enforcement(self):
        """Test that total bet limits across all bets are enforced."""
        strict_game = Game(table_type="AMERICAN", betting_rules_config=self.config_path)
        strict_game.add_player("Charlie")
        charlie = strict_game.players["Charlie"]
        charlie.buy_chips(count=5000, value=1)

        # Place bets that individually are valid but exceed total limit
        bet1 = Bet.create_color_bet(
            "red",
            amount=500,
            layout=strict_game.table.layout,
            betting_rules=strict_game.betting_rules,
        )
        bet2 = Bet.create_color_bet(
            "black",
            amount=500,
            layout=strict_game.table.layout,
            betting_rules=strict_game.betting_rules,
        )
        bet3 = Bet.create_straight_up_bet(
            "17",
            amount=50,
            layout=strict_game.table.layout,
            betting_rules=strict_game.betting_rules,
        )

        # First two bets should be accepted
        strict_game.place_bet(bet1, "Charlie")
        strict_game.place_bet(bet2, "Charlie")

        # Third bet should exceed total limit (500 + 500 + 1000 = 2000, but we want to exceed 2000)
        bet4 = Bet.create_dozen_bet(
            1,
            amount=1000,
            layout=strict_game.table.layout,
            betting_rules=strict_game.betting_rules,
        )
        strict_game.place_bet(bet4, "Charlie")  # This should work (total = 2000)

        # Now try to add one more bet that would exceed the limit
        bet5 = Bet.create_straight_up_bet(
            "23",
            amount=50,
            layout=strict_game.table.layout,
            betting_rules=strict_game.betting_rules,
        )

        with self.assertRaises(ValueError) as context:
            strict_game.place_bet(bet5, "Charlie")
        self.assertIn("exceed maximum total bet limit", str(context.exception))

    def test_player_chip_balance_enforcement(self):
        """Test that player chip balances are enforced."""
        # Alice has 1000 chips, try to bet more than she has
        large_bet = Bet.create_color_bet(
            "red",
            amount=1500,
            layout=self.game.table.layout,
            betting_rules=self.game.betting_rules,
        )

        with self.assertRaises(Exception) as context:
            self.game.place_bet(large_bet, "Alice")
        self.assertIn("insufficient chips", str(context.exception))

        # Valid bet should work
        valid_bet = Bet.create_color_bet(
            "red",
            amount=100,
            layout=self.game.table.layout,
            betting_rules=self.game.betting_rules,
        )
        result = self.game.place_bet(valid_bet, "Alice")
        self.assertTrue(result)

        # Check that chips were deducted
        self.assertEqual(self.game.players["Alice"].get_chip_balance(), 900)

    def test_betting_phase_management(self):
        """Test that betting phases are properly managed."""
        # Betting should be open initially
        self.assertTrue(self.game.betting_open)

        # Place a bet
        bet = Bet.create_color_bet(
            "red",
            amount=50,
            layout=self.game.table.layout,
            betting_rules=self.game.betting_rules,
        )
        self.game.place_bet(bet, "Alice")

        # Close betting
        validation_result = self.game.close_betting()
        self.assertFalse(self.game.betting_open)
        self.assertTrue(validation_result["valid"])

        # Try to place bet when betting is closed
        another_bet = Bet.create_color_bet(
            "black",
            amount=50,
            layout=self.game.table.layout,
            betting_rules=self.game.betting_rules,
        )
        with self.assertRaises(ValueError) as context:
            self.game.place_bet(another_bet, "Alice")
        self.assertIn("Betting is closed", str(context.exception))

        # Open betting for new round
        self.game.open_betting()
        self.assertTrue(self.game.betting_open)
        self.assertEqual(len(self.game.active_bets), 0)  # Bets should be cleared

    def test_multiple_bet_validation(self):
        """Test validation of multiple bets together."""
        bets = [
            Bet.create_straight_up_bet(
                "17",
                amount=100,
                layout=self.game.table.layout,
                betting_rules=self.game.betting_rules,
            ),
            Bet.create_color_bet(
                "red",
                amount=200,
                layout=self.game.table.layout,
                betting_rules=self.game.betting_rules,
            ),
            Bet.create_dozen_bet(
                1,
                amount=150,
                layout=self.game.table.layout,
                betting_rules=self.game.betting_rules,
            ),
        ]

        validation_result = self.game.betting_rules.validate_multiple_bets(bets)

        self.assertTrue(validation_result["valid"])
        self.assertEqual(validation_result["total_amount"], 450)
        self.assertEqual(validation_result["bet_count"], 3)
        self.assertIn("straight_up", validation_result["bet_type_counts"])
        self.assertIn("red", validation_result["bet_type_counts"])
        self.assertIn("first_dozen", validation_result["bet_type_counts"])

    def test_bet_type_allowance(self):
        """Test that only allowed bet types can be placed."""
        # Create config that only allows certain bet types
        limited_config = """
payout_ratios:
  straight_up: 35
  red: 1
  # Note: black is not included, so it should not be allowed

minimum_bet_ratios:
  global: 1.0

maximum_bet_ratios:
  global: 1.0

table_limits:
  minimum_bet: 1
  maximum_bet: 1000
  maximum_total_bet: 10000
"""

        limited_path = os.path.join(self.temp_dir, "limited.yaml")
        with open(limited_path, "w") as f:
            f.write(limited_config)

        limited_game = Game(table_type="AMERICAN", betting_rules_config=limited_path)

        # Allowed bet should work
        allowed_bet = Bet.create_straight_up_bet(
            "17",
            amount=50,
            layout=limited_game.table.layout,
            betting_rules=limited_game.betting_rules,
        )
        self.assertEqual(allowed_bet.amount, 50)

        # Disallowed bet should fail
        with self.assertRaises(ValueError) as context:
            disallowed_bet = Bet.create_color_bet(
                "black",
                amount=50,
                layout=limited_game.table.layout,
                betting_rules=limited_game.betting_rules,
            )
        self.assertIn("not allowed on this table", str(context.exception))

        os.remove(limited_path)

    def test_special_rules_enforcement(self):
        """Test that special rules are enforced."""
        # Test with call bets disabled
        validation_result = self.game.betting_rules.validate_multiple_bets([])
        self.assertTrue(validation_result["valid"])

        # Test special rule queries
        self.assertFalse(
            self.game.betting_rules.is_special_rule_enabled("allow_call_bets")
        )
        self.assertTrue(
            self.game.betting_rules.is_special_rule_enabled("progressive_betting")
        )

        # Test game rule queries
        self.assertFalse(self.game.betting_rules.get_game_rule("en_prison"))
        self.assertEqual(self.game.betting_rules.get_game_rule("maximum_repeats"), 10)

    def test_bet_summary_and_tracking(self):
        """Test bet summary and tracking functionality."""
        # Place several bets
        bet1 = Bet.create_straight_up_bet(
            "17",
            amount=100,
            layout=self.game.table.layout,
            betting_rules=self.game.betting_rules,
        )
        bet2 = Bet.create_color_bet(
            "red",
            amount=200,
            layout=self.game.table.layout,
            betting_rules=self.game.betting_rules,
        )
        bet3 = Bet.create_straight_up_bet(
            "23",
            amount=150,
            layout=self.game.table.layout,
            betting_rules=self.game.betting_rules,
        )

        self.game.place_bet(bet1, "Alice")
        self.game.place_bet(bet2, "Bob")
        self.game.place_bet(bet3, "Alice")

        # Get bet summary
        summary = self.game.get_bet_summary()

        self.assertEqual(summary["total_bets"], 3)
        self.assertEqual(summary["total_amount"], 450)
        self.assertEqual(summary["bet_types"]["straight_up"]["count"], 2)
        self.assertEqual(summary["bet_types"]["straight_up"]["total_amount"], 250)
        self.assertEqual(summary["bet_types"]["red"]["count"], 1)
        self.assertEqual(summary["bet_types"]["red"]["total_amount"], 200)
        self.assertTrue(summary["betting_open"])

        # Test total bet amount getter
        self.assertEqual(self.game.get_total_bet_amount(), 450)

    def test_player_balance_methods(self):
        """Test player balance checking methods."""
        alice = self.game.players["Alice"]

        # Test balance methods
        self.assertEqual(alice.get_chip_balance(), 1000)
        self.assertEqual(alice.get_chip_value(), 1)
        self.assertEqual(alice.get_total_value(), 1000)

        # Test affordability checks
        self.assertTrue(alice.can_afford_bet(500))
        self.assertTrue(alice.can_afford_bet(1000))
        self.assertFalse(alice.can_afford_bet(1001))

        # Test with player who has no chips
        charlie = Player("Charlie")
        self.assertEqual(charlie.get_chip_balance(), 0)
        self.assertEqual(charlie.get_chip_value(), 0)
        self.assertEqual(charlie.get_total_value(), 0)
        self.assertFalse(charlie.can_afford_bet(1))

    def test_comprehensive_table_info(self):
        """Test comprehensive table information retrieval."""
        info = self.game.betting_rules.get_table_info()

        self.assertEqual(info["table_type"], "AMERICAN")
        self.assertIn("minimum_bet", info)
        self.assertIn("maximum_bet", info)
        self.assertIn("maximum_total_bet", info)
        self.assertIn("payout_ratios", info)
        self.assertIn("house_edge_calculated", info)
        self.assertIn("total_pockets", info)
        self.assertIn("game_rules", info)
        self.assertIn("special_rules", info)

        # Verify American table has 38 pockets
        self.assertEqual(info["total_pockets"], 38)

    def test_error_handling_edge_cases(self):
        """Test error handling for edge cases."""
        # Test placing bet for non-existent player
        bet = Bet.create_color_bet(
            "red",
            amount=50,
            layout=self.game.table.layout,
            betting_rules=self.game.betting_rules,
        )

        # Should work without error (player_name is optional)
        result = self.game.place_bet(bet, "NonExistentPlayer")
        self.assertTrue(result)

        # Test validation with empty bet list
        validation_result = self.game.betting_rules.validate_multiple_bets([])
        self.assertTrue(validation_result["valid"])
        self.assertEqual(validation_result["bet_count"], 0)
        self.assertEqual(validation_result["total_amount"], 0)


if __name__ == "__main__":
    unittest.main()
