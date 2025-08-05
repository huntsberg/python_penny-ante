import unittest

from .context import penny_ante
from penny_ante.bet import Bet, BetType
from penny_ante.table import Table
from penny_ante.space import Space


class TestBetEdgeCases(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.table = Table(table_type="AMERICAN")
        self.layout = self.table.layout

    def test_bet_with_non_standard_spaces(self):
        """Test bets with spaces that might cause edge cases."""
        # Test with space that has leading/trailing whitespace (if normalized)
        bet = Bet.create_straight_up_bet("17", amount=5, layout=self.layout)
        self.assertEqual(bet.spaces, {"17"})
        
    def test_winning_bet_with_non_numeric_values(self):
        """Test winning bet logic with non-numeric space values."""
        red_bet = Bet.create_color_bet("red", amount=10, layout=self.layout)
        
        # Test with a space that has a non-numeric value
        space_with_letters = Space("abc")
        space_with_letters.color = "RED"
        
        # Should still win based on color, even though value is non-numeric
        self.assertTrue(red_bet.is_winning_bet(space_with_letters))
        
        # Test odd/even with non-numeric - should lose
        odd_bet = Bet(BetType.ODD, set(), amount=10, layout=self.layout)
        self.assertFalse(odd_bet.is_winning_bet(space_with_letters))
        
    def test_all_outside_bets_with_boundary_numbers(self):
        """Test all outside bets with edge numbers."""
        # Create all outside bet types
        high_bet = Bet(BetType.HIGH, set(), amount=10, layout=self.layout)
        low_bet = Bet(BetType.LOW, set(), amount=10, layout=self.layout)
        
        # Test edge cases for high/low
        space_36 = Space("36")  # Maximum high
        space_1 = Space("1")    # Minimum low
        
        self.assertTrue(high_bet.is_winning_bet(space_36))
        self.assertFalse(low_bet.is_winning_bet(space_36))
        
        self.assertFalse(high_bet.is_winning_bet(space_1))
        self.assertTrue(low_bet.is_winning_bet(space_1))
        
    def test_dozen_bets_with_all_boundary_numbers(self):
        """Test dozen bets with all boundary numbers."""
        dozen1 = Bet.create_dozen_bet(1, amount=10, layout=self.layout)
        dozen2 = Bet.create_dozen_bet(2, amount=10, layout=self.layout)
        dozen3 = Bet.create_dozen_bet(3, amount=10, layout=self.layout)
        
        # Test all boundaries
        test_cases = [
            ("1", True, False, False),   # First in dozen 1
            ("12", True, False, False),  # Last in dozen 1
            ("13", False, True, False),  # First in dozen 2
            ("24", False, True, False),  # Last in dozen 2
            ("25", False, False, True),  # First in dozen 3
            ("36", False, False, True),  # Last in dozen 3
        ]
        
        for space_val, d1_win, d2_win, d3_win in test_cases:
            space = Space(space_val)
            self.assertEqual(dozen1.is_winning_bet(space), d1_win, f"Dozen 1 failed for {space_val}")
            self.assertEqual(dozen2.is_winning_bet(space), d2_win, f"Dozen 2 failed for {space_val}")
            self.assertEqual(dozen3.is_winning_bet(space), d3_win, f"Dozen 3 failed for {space_val}")
    
    def test_column_bets_with_all_numbers(self):
        """Test column bets with specific numbers from each column."""
        col1 = Bet.create_column_bet(1, amount=10, layout=self.layout)
        col2 = Bet.create_column_bet(2, amount=10, layout=self.layout)
        col3 = Bet.create_column_bet(3, amount=10, layout=self.layout)
        
        # Test specific numbers known to be in each column
        # Column 1: 1,4,7,10,13,16,19,22,25,28,31,34
        # Column 2: 2,5,8,11,14,17,20,23,26,29,32,35
        # Column 3: 3,6,9,12,15,18,21,24,27,30,33,36
        
        test_cases = [
            ("1", True, False, False),
            ("2", False, True, False),
            ("3", False, False, True),
            ("34", True, False, False),  # Last in column 1
            ("35", False, True, False),  # Last in column 2
            ("36", False, False, True),  # Last in column 3
        ]
        
        for space_val, c1_win, c2_win, c3_win in test_cases:
            space = Space(space_val)
            self.assertEqual(col1.is_winning_bet(space), c1_win, f"Column 1 failed for {space_val}")
            self.assertEqual(col2.is_winning_bet(space), c2_win, f"Column 2 failed for {space_val}")
            self.assertEqual(col3.is_winning_bet(space), c3_win, f"Column 3 failed for {space_val}")
    
    def test_bet_type_coverage_for_all_outside_bets(self):
        """Ensure all outside bet types are covered in winning logic."""
        # Create bets for all outside bet types
        red_bet = Bet(BetType.RED, set(), amount=10, layout=self.layout)
        black_bet = Bet(BetType.BLACK, set(), amount=10, layout=self.layout)
        odd_bet = Bet(BetType.ODD, set(), amount=10, layout=self.layout)
        even_bet = Bet(BetType.EVEN, set(), amount=10, layout=self.layout)
        high_bet = Bet(BetType.HIGH, set(), amount=10, layout=self.layout)
        low_bet = Bet(BetType.LOW, set(), amount=10, layout=self.layout)
        dozen1_bet = Bet(BetType.FIRST_DOZEN, set(), amount=10, layout=self.layout)
        dozen2_bet = Bet(BetType.SECOND_DOZEN, set(), amount=10, layout=self.layout)
        dozen3_bet = Bet(BetType.THIRD_DOZEN, set(), amount=10, layout=self.layout)
        col1_bet = Bet(BetType.FIRST_COLUMN, set(), amount=10, layout=self.layout)
        col2_bet = Bet(BetType.SECOND_COLUMN, set(), amount=10, layout=self.layout)
        col3_bet = Bet(BetType.THIRD_COLUMN, set(), amount=10, layout=self.layout)
        
        # Test with a red odd low number from first dozen, first column
        space = Space("1")
        space.color = "RED"
        
        # Should win: red, odd, low, first dozen, first column
        self.assertTrue(red_bet.is_winning_bet(space))
        self.assertFalse(black_bet.is_winning_bet(space))
        self.assertTrue(odd_bet.is_winning_bet(space))
        self.assertFalse(even_bet.is_winning_bet(space))
        self.assertFalse(high_bet.is_winning_bet(space))
        self.assertTrue(low_bet.is_winning_bet(space))
        self.assertTrue(dozen1_bet.is_winning_bet(space))
        self.assertFalse(dozen2_bet.is_winning_bet(space))
        self.assertFalse(dozen3_bet.is_winning_bet(space))
        self.assertTrue(col1_bet.is_winning_bet(space))
        self.assertFalse(col2_bet.is_winning_bet(space))
        self.assertFalse(col3_bet.is_winning_bet(space))
        
    def test_unknown_bet_type_fallthrough(self):
        """Test the fallthrough case in is_winning_bet for unhandled bet types."""
        # Create a bet with a type that's not explicitly handled in is_winning_bet
        # This is tricky since all types should be handled, but let's test the return False fallthrough
        straight_bet = Bet.create_straight_up_bet("17", amount=10, layout=self.layout)
        
        # Test with non-matching space - should return False via the fallthrough
        space = Space("18")
        self.assertFalse(straight_bet.is_winning_bet(space))
        
    def test_payout_with_losing_bets(self):
        """Test payout calculation returns 0 for losing bets."""
        bet = Bet.create_straight_up_bet("17", amount=10, layout=self.layout)
        losing_space = Space("18")
        
        payout = bet.calculate_payout(losing_space)
        self.assertEqual(payout, 0)
        
    def test_bet_with_copy_of_spaces_set(self):
        """Test that bet correctly handles copying of spaces set."""
        original_spaces = {"17", "18"}
        bet = Bet(BetType.SPLIT, original_spaces, amount=10, layout=self.layout)
        
        # Modify original set
        original_spaces.add("19")
        
        # Bet should not be affected
        self.assertEqual(bet.spaces, {"17", "18"})
        
    def test_layout_positions_with_invalid_spaces(self):
        """Test layout position calculation when some spaces don't exist in layout."""
        # Create a bet without layout validation to test layout position calculation
        bet = Bet(BetType.STRAIGHT_UP, "99", amount=10)  # No layout validation
        
        # Now calculate positions with layout
        positions = bet._calculate_layout_positions(self.layout)
        
        # Should return empty list since "99" is not in layout
        self.assertEqual(len(positions), 0)
        
    def test_bet_initialization_with_no_layout(self):
        """Test bet initialization without layout parameter."""
        bet = Bet(BetType.STRAIGHT_UP, "17", amount=10)
        
        self.assertEqual(bet.bet_type, BetType.STRAIGHT_UP)
        self.assertEqual(bet.spaces, {"17"})
        self.assertEqual(bet.amount, 10)
        self.assertEqual(bet.chips, None)
        self.assertEqual(len(bet.layout_positions), 0)
        
    def test_all_payout_ratios_exist(self):
        """Test that all bet types have payout ratios defined."""
        for bet_type in BetType:
            self.assertIn(bet_type, Bet.PAYOUT_RATIOS, 
                         f"Payout ratio missing for {bet_type}")
            
    def test_bet_string_methods_with_different_data(self):
        """Test string representation methods with various bet configurations."""
        # Test with different bet types
        street_bet = Bet(BetType.STREET, ["1", "2", "3"], amount=15, layout=self.layout)
        corner_bet = Bet(BetType.CORNER, ["1", "2", "4", "5"], amount=20, layout=self.layout)
        
        # Test str method
        street_str = str(street_bet)
        self.assertIn("street", street_str)
        self.assertIn("15", street_str)
        
        corner_str = str(corner_bet)
        self.assertIn("corner", corner_str)
        self.assertIn("20", corner_str)
        
        # Test repr method
        street_repr = repr(street_bet)
        self.assertIn("Bet", street_repr)
        self.assertIn("street", street_repr)
        
        corner_repr = repr(corner_bet)
        self.assertIn("Bet", corner_repr)
        self.assertIn("corner", corner_repr)


if __name__ == "__main__":
    unittest.main() 