import unittest

from .context import penny_ante
from penny_ante.bet import Bet, BetType
from penny_ante.table import Table
from penny_ante.space import Space


class TestBet(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.table = Table(table_type="AMERICAN")
        self.layout = self.table.layout
        
    def test_create_straight_up_bet(self):
        """Test creating a straight up bet on a single number."""
        bet = Bet.create_straight_up_bet("17", amount=5, layout=self.layout)
        
        self.assertEqual(bet.bet_type, BetType.STRAIGHT_UP)
        self.assertEqual(bet.spaces, {"17"})
        self.assertEqual(bet.amount, 5)
        
    def test_create_split_bet(self):
        """Test creating a split bet on two numbers."""
        bet = Bet.create_split_bet("17", "18", amount=10, layout=self.layout)
        
        self.assertEqual(bet.bet_type, BetType.SPLIT)
        self.assertEqual(bet.spaces, {"17", "18"})
        self.assertEqual(bet.amount, 10)
        
    def test_create_color_bet_red(self):
        """Test creating a red color bet."""
        bet = Bet.create_color_bet("red", amount=20, layout=self.layout)
        
        self.assertEqual(bet.bet_type, BetType.RED)
        self.assertEqual(bet.amount, 20)
        # Check that some red numbers are included
        self.assertIn("1", bet.spaces)
        self.assertIn("3", bet.spaces)
        self.assertNotIn("2", bet.spaces)  # 2 is black
        
    def test_create_color_bet_black(self):
        """Test creating a black color bet."""
        bet = Bet.create_color_bet("black", amount=15, layout=self.layout)
        
        self.assertEqual(bet.bet_type, BetType.BLACK)
        self.assertEqual(bet.amount, 15)
        # Check that some black numbers are included
        self.assertIn("2", bet.spaces)
        self.assertIn("4", bet.spaces)
        self.assertNotIn("1", bet.spaces)  # 1 is red
        
    def test_create_dozen_bet(self):
        """Test creating dozen bets."""
        bet1 = Bet.create_dozen_bet(1, amount=25, layout=self.layout)
        bet2 = Bet.create_dozen_bet(2, amount=30, layout=self.layout)
        bet3 = Bet.create_dozen_bet(3, amount=35, layout=self.layout)
        
        self.assertEqual(bet1.bet_type, BetType.FIRST_DOZEN)
        self.assertEqual(bet2.bet_type, BetType.SECOND_DOZEN)
        self.assertEqual(bet3.bet_type, BetType.THIRD_DOZEN)
        
        # Check number ranges
        self.assertIn("1", bet1.spaces)
        self.assertIn("12", bet1.spaces)
        self.assertNotIn("13", bet1.spaces)
        
        self.assertIn("13", bet2.spaces)
        self.assertIn("24", bet2.spaces)
        self.assertNotIn("12", bet2.spaces)
        self.assertNotIn("25", bet2.spaces)
        
        self.assertIn("25", bet3.spaces)
        self.assertIn("36", bet3.spaces)
        self.assertNotIn("24", bet3.spaces)
        
    def test_create_column_bet(self):
        """Test creating column bets."""
        bet1 = Bet.create_column_bet(1, amount=40, layout=self.layout)
        bet2 = Bet.create_column_bet(2, amount=45, layout=self.layout)
        bet3 = Bet.create_column_bet(3, amount=50, layout=self.layout)
        
        self.assertEqual(bet1.bet_type, BetType.FIRST_COLUMN)
        self.assertEqual(bet2.bet_type, BetType.SECOND_COLUMN)
        self.assertEqual(bet3.bet_type, BetType.THIRD_COLUMN)
        
        # Check column numbers
        self.assertIn("1", bet1.spaces)
        self.assertIn("4", bet1.spaces)
        self.assertIn("34", bet1.spaces)
        self.assertNotIn("2", bet1.spaces)
        
        self.assertIn("2", bet2.spaces)
        self.assertIn("5", bet2.spaces)
        self.assertIn("35", bet2.spaces)
        self.assertNotIn("1", bet2.spaces)
        
        self.assertIn("3", bet3.spaces)
        self.assertIn("6", bet3.spaces)
        self.assertIn("36", bet3.spaces)
        self.assertNotIn("1", bet3.spaces)
        
    def test_invalid_color_bet_raises_error(self):
        """Test that invalid color raises ValueError."""
        with self.assertRaises(ValueError):
            Bet.create_color_bet("green", amount=10, layout=self.layout)
            
    def test_invalid_dozen_bet_raises_error(self):
        """Test that invalid dozen raises ValueError."""
        with self.assertRaises(ValueError):
            Bet.create_dozen_bet(4, amount=10, layout=self.layout)
            
    def test_invalid_column_bet_raises_error(self):
        """Test that invalid column raises ValueError."""
        with self.assertRaises(ValueError):
            Bet.create_column_bet(4, amount=10, layout=self.layout)
            
    def test_straight_up_bet_validation(self):
        """Test validation of straight up bets."""
        # Valid bet
        bet = Bet(BetType.STRAIGHT_UP, "17", amount=5, layout=self.layout)
        self.assertEqual(bet.spaces, {"17"})
        
        # Invalid - too many spaces
        with self.assertRaises(ValueError):
            Bet(BetType.STRAIGHT_UP, ["17", "18"], amount=5, layout=self.layout)
            
    def test_split_bet_validation(self):
        """Test validation of split bets."""
        # Valid bet
        bet = Bet(BetType.SPLIT, ["17", "18"], amount=10, layout=self.layout)
        self.assertEqual(bet.spaces, {"17", "18"})
        
        # Invalid - wrong number of spaces
        with self.assertRaises(ValueError):
            Bet(BetType.SPLIT, ["17"], amount=10, layout=self.layout)
            
    def test_negative_amount_raises_error(self):
        """Test that negative bet amount raises ValueError."""
        with self.assertRaises(ValueError):
            Bet(BetType.STRAIGHT_UP, "17", amount=-5, layout=self.layout)
            
    def test_is_winning_bet_straight_up(self):
        """Test winning check for straight up bets."""
        bet = Bet.create_straight_up_bet("17", amount=5, layout=self.layout)
        
        # Create winning space
        winning_space = Space("17")
        winning_space.color = "BLACK"
        
        # Create losing space
        losing_space = Space("18")
        losing_space.color = "RED"
        
        self.assertTrue(bet.is_winning_bet(winning_space))
        self.assertFalse(bet.is_winning_bet(losing_space))
        
    def test_is_winning_bet_red(self):
        """Test winning check for red color bets."""
        bet = Bet.create_color_bet("red", amount=10, layout=self.layout)
        
        # Create red winning space
        red_space = Space("1")
        red_space.color = "RED"
        
        # Create black losing space
        black_space = Space("2")
        black_space.color = "BLACK"
        
        # Create green losing space (0)
        green_space = Space("0")
        green_space.color = "GREEN"
        
        self.assertTrue(bet.is_winning_bet(red_space))
        self.assertFalse(bet.is_winning_bet(black_space))
        self.assertFalse(bet.is_winning_bet(green_space))
        
    def test_is_winning_bet_odd_even(self):
        """Test winning check for odd/even bets."""
        # Create odd bet
        odd_bet = Bet(BetType.ODD, set(), amount=10, layout=self.layout)
        
        # Create even bet
        even_bet = Bet(BetType.EVEN, set(), amount=10, layout=self.layout)
        
        # Test odd numbers
        odd_space = Space("17")
        self.assertTrue(odd_bet.is_winning_bet(odd_space))
        self.assertFalse(even_bet.is_winning_bet(odd_space))
        
        # Test even numbers
        even_space = Space("18")
        self.assertFalse(odd_bet.is_winning_bet(even_space))
        self.assertTrue(even_bet.is_winning_bet(even_space))
        
        # Test zero (neither odd nor even for betting purposes)
        zero_space = Space("0")
        self.assertFalse(odd_bet.is_winning_bet(zero_space))
        self.assertFalse(even_bet.is_winning_bet(zero_space))
        
    def test_is_winning_bet_high_low(self):
        """Test winning check for high/low bets."""
        # Create high bet (19-36)
        high_bet = Bet(BetType.HIGH, set(), amount=10, layout=self.layout)
        
        # Create low bet (1-18)
        low_bet = Bet(BetType.LOW, set(), amount=10, layout=self.layout)
        
        # Test low numbers
        low_space = Space("18")
        self.assertFalse(high_bet.is_winning_bet(low_space))
        self.assertTrue(low_bet.is_winning_bet(low_space))
        
        # Test high numbers
        high_space = Space("19")
        self.assertTrue(high_bet.is_winning_bet(high_space))
        self.assertFalse(low_bet.is_winning_bet(high_space))
        
        # Test zero
        zero_space = Space("0")
        self.assertFalse(high_bet.is_winning_bet(zero_space))
        self.assertFalse(low_bet.is_winning_bet(zero_space))
        
    def test_calculate_payout_straight_up(self):
        """Test payout calculation for straight up bets."""
        bet = Bet.create_straight_up_bet("17", amount=5, layout=self.layout)
        
        # Winning space
        winning_space = Space("17")
        payout = bet.calculate_payout(winning_space)
        expected_payout = 5 + (5 * 35)  # original bet + winnings
        self.assertEqual(payout, expected_payout)
        
        # Losing space
        losing_space = Space("18")
        payout = bet.calculate_payout(losing_space)
        self.assertEqual(payout, 0)
        
    def test_calculate_payout_color_bet(self):
        """Test payout calculation for color bets."""
        bet = Bet.create_color_bet("red", amount=20, layout=self.layout)
        
        # Winning space (red)
        winning_space = Space("1")
        winning_space.color = "RED"
        payout = bet.calculate_payout(winning_space)
        expected_payout = 20 + (20 * 1)  # original bet + winnings
        self.assertEqual(payout, expected_payout)
        
        # Losing space (black)
        losing_space = Space("2")
        losing_space.color = "BLACK"
        payout = bet.calculate_payout(losing_space)
        self.assertEqual(payout, 0)
        
    def test_calculate_payout_dozen_bet(self):
        """Test payout calculation for dozen bets."""
        bet = Bet.create_dozen_bet(1, amount=15, layout=self.layout)
        
        # Winning space (in first dozen)
        winning_space = Space("7")
        payout = bet.calculate_payout(winning_space)
        expected_payout = 15 + (15 * 2)  # original bet + winnings
        self.assertEqual(payout, expected_payout)
        
        # Losing space (not in first dozen)
        losing_space = Space("25")
        payout = bet.calculate_payout(losing_space)
        self.assertEqual(payout, 0)
        
    def test_bet_string_representation(self):
        """Test string representation of bets."""
        bet = Bet.create_straight_up_bet("17", amount=5, layout=self.layout)
        str_repr = str(bet)
        self.assertIn("straight_up", str_repr)
        self.assertIn("17", str_repr)
        self.assertIn("5", str_repr)
        
    def test_bet_repr(self):
        """Test detailed representation of bets."""
        bet = Bet.create_split_bet("17", "18", amount=10, layout=self.layout)
        repr_str = repr(bet)
        self.assertIn("Bet", repr_str)
        self.assertIn("split", repr_str)
        self.assertIn("10", repr_str)
        
    def test_layout_positions_calculated(self):
        """Test that layout positions are calculated when layout is provided."""
        bet = Bet.create_straight_up_bet("17", amount=5, layout=self.layout)
        
        # Should have one layout position
        self.assertEqual(len(bet.layout_positions), 1)
        row, col = bet.layout_positions[0]
        
        # Verify the position matches the layout lookup
        expected_row, expected_col = self.layout.lookup["17"]
        self.assertEqual(row, expected_row)
        self.assertEqual(col, expected_col)
        
    def test_bet_without_layout(self):
        """Test creating bets without layout validation."""
        bet = Bet(BetType.STRAIGHT_UP, "17", amount=5)
        
        self.assertEqual(bet.bet_type, BetType.STRAIGHT_UP)
        self.assertEqual(bet.spaces, {"17"})
        self.assertEqual(bet.amount, 5)
        self.assertEqual(len(bet.layout_positions), 0)


if __name__ == "__main__":
    unittest.main() 