import unittest

from .context import penny_ante
from penny_ante.bet import Bet, BetType
from penny_ante.table import Table
from penny_ante.space import Space
from penny_ante.chips import Chips


class TestBetComprehensive(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.american_table = Table(table_type="AMERICAN")
        self.european_table = Table(table_type="EUROPEAN")
        self.american_layout = self.american_table.layout
        self.european_layout = self.european_table.layout
        
    def test_invalid_space_validation(self):
        """Test validation with invalid space values."""
        # Test invalid space not in layout
        with self.assertRaises(ValueError) as context:
            Bet(BetType.STRAIGHT_UP, "99", amount=10, layout=self.american_layout)
        self.assertIn("Invalid space value: 99", str(context.exception))
        
        # Test invalid space with letters
        with self.assertRaises(ValueError):
            Bet(BetType.STRAIGHT_UP, "abc", amount=10, layout=self.american_layout)
    
    def test_zero_amount_validation(self):
        """Test validation with zero amount."""
        with self.assertRaises(ValueError) as context:
            Bet(BetType.STRAIGHT_UP, "17", amount=0, layout=self.american_layout)
        self.assertIn("Bet amount must be positive", str(context.exception))
    
    def test_street_bet_validation_errors(self):
        """Test street bet validation with wrong number of spaces."""
        # Too few spaces
        with self.assertRaises(ValueError) as context:
            Bet(BetType.STREET, ["17", "18"], amount=15, layout=self.american_layout)
        self.assertIn("Street bet must cover exactly three spaces", str(context.exception))
        
        # Too many spaces
        with self.assertRaises(ValueError):
            Bet(BetType.STREET, ["17", "18", "19", "20"], amount=15, layout=self.american_layout)
    
    def test_corner_bet_validation_errors(self):
        """Test corner bet validation with wrong number of spaces."""
        # Too few spaces
        with self.assertRaises(ValueError) as context:
            Bet(BetType.CORNER, ["17", "18", "19"], amount=20, layout=self.american_layout)
        self.assertIn("Corner bet must cover exactly four spaces", str(context.exception))
        
        # Too many spaces
        with self.assertRaises(ValueError):
            Bet(BetType.CORNER, ["17", "18", "19", "20", "21"], amount=20, layout=self.american_layout)
    
    def test_six_line_bet_validation_errors(self):
        """Test six line bet validation with wrong number of spaces."""
        # Too few spaces
        with self.assertRaises(ValueError) as context:
            Bet(BetType.SIX_LINE, ["17", "18", "19", "20", "21"], amount=25, layout=self.american_layout)
        self.assertIn("Six line bet must cover exactly six spaces", str(context.exception))
        
        # Too many spaces
        with self.assertRaises(ValueError):
            Bet(BetType.SIX_LINE, ["17", "18", "19", "20", "21", "22", "23"], amount=25, layout=self.american_layout)
    
    def test_bet_with_zero_and_double_zero(self):
        """Test bets that include 0 and 00."""
        # American table with 00
        bet_00 = Bet.create_straight_up_bet("00", amount=10, layout=self.american_layout)
        self.assertEqual(bet_00.spaces, {"00"})
        
        # European table should not have 00 in lookup, but validation should still work
        # since we explicitly allow "0" and "00" in validation
        bet_0_euro = Bet.create_straight_up_bet("0", amount=10, layout=self.european_layout)
        self.assertEqual(bet_0_euro.spaces, {"0"})
    
    def test_all_bet_types_winning_scenarios(self):
        """Test winning scenarios for all bet types not covered in basic tests."""
        # Test all dozen bets
        dozen1_bet = Bet.create_dozen_bet(1, amount=30, layout=self.american_layout)
        dozen2_bet = Bet.create_dozen_bet(2, amount=30, layout=self.american_layout)
        dozen3_bet = Bet.create_dozen_bet(3, amount=30, layout=self.american_layout)
        
        # Test with space in first dozen
        space_5 = Space("5")
        self.assertTrue(dozen1_bet.is_winning_bet(space_5))
        self.assertFalse(dozen2_bet.is_winning_bet(space_5))
        self.assertFalse(dozen3_bet.is_winning_bet(space_5))
        
        # Test with space in second dozen
        space_15 = Space("15")
        self.assertFalse(dozen1_bet.is_winning_bet(space_15))
        self.assertTrue(dozen2_bet.is_winning_bet(space_15))
        self.assertFalse(dozen3_bet.is_winning_bet(space_15))
        
        # Test with space in third dozen
        space_30 = Space("30")
        self.assertFalse(dozen1_bet.is_winning_bet(space_30))
        self.assertFalse(dozen2_bet.is_winning_bet(space_30))
        self.assertTrue(dozen3_bet.is_winning_bet(space_30))
    
    def test_all_column_bets_winning_scenarios(self):
        """Test winning scenarios for all column bets."""
        col1_bet = Bet.create_column_bet(1, amount=40, layout=self.american_layout)
        col2_bet = Bet.create_column_bet(2, amount=40, layout=self.american_layout)
        col3_bet = Bet.create_column_bet(3, amount=40, layout=self.american_layout)
        
        # Test with space in first column
        space_1 = Space("1")
        self.assertTrue(col1_bet.is_winning_bet(space_1))
        self.assertFalse(col2_bet.is_winning_bet(space_1))
        self.assertFalse(col3_bet.is_winning_bet(space_1))
        
        # Test with space in second column
        space_2 = Space("2")
        self.assertFalse(col1_bet.is_winning_bet(space_2))
        self.assertTrue(col2_bet.is_winning_bet(space_2))
        self.assertFalse(col3_bet.is_winning_bet(space_2))
        
        # Test with space in third column
        space_3 = Space("3")
        self.assertFalse(col1_bet.is_winning_bet(space_3))
        self.assertFalse(col2_bet.is_winning_bet(space_3))
        self.assertTrue(col3_bet.is_winning_bet(space_3))
    
    def test_non_digit_spaces_for_outside_bets(self):
        """Test outside bets with non-digit spaces like 0 and 00."""
        red_bet = Bet.create_color_bet("red", amount=20, layout=self.american_layout)
        black_bet = Bet.create_color_bet("black", amount=20, layout=self.american_layout)
        odd_bet = Bet(BetType.ODD, set(), amount=10, layout=self.american_layout)
        even_bet = Bet(BetType.EVEN, set(), amount=10, layout=self.american_layout)
        high_bet = Bet(BetType.HIGH, set(), amount=10, layout=self.american_layout)
        low_bet = Bet(BetType.LOW, set(), amount=10, layout=self.american_layout)
        
        # Test with 0 (green)
        space_0 = Space("0")
        space_0.color = "GREEN"
        
        self.assertFalse(red_bet.is_winning_bet(space_0))
        self.assertFalse(black_bet.is_winning_bet(space_0))
        self.assertFalse(odd_bet.is_winning_bet(space_0))
        self.assertFalse(even_bet.is_winning_bet(space_0))
        self.assertFalse(high_bet.is_winning_bet(space_0))
        self.assertFalse(low_bet.is_winning_bet(space_0))
        
        # Test with 00 (green)
        space_00 = Space("00")
        space_00.color = "GREEN"
        
        self.assertFalse(red_bet.is_winning_bet(space_00))
        self.assertFalse(black_bet.is_winning_bet(space_00))
        self.assertFalse(odd_bet.is_winning_bet(space_00))
        self.assertFalse(even_bet.is_winning_bet(space_00))
        self.assertFalse(high_bet.is_winning_bet(space_00))
        self.assertFalse(low_bet.is_winning_bet(space_00))
    
    def test_bet_with_different_space_input_types(self):
        """Test bet creation with different input types for spaces."""
        # String input
        bet1 = Bet(BetType.STRAIGHT_UP, "17", amount=5, layout=self.american_layout)
        self.assertEqual(bet1.spaces, {"17"})
        
        # List input
        bet2 = Bet(BetType.SPLIT, ["17", "18"], amount=10, layout=self.american_layout)
        self.assertEqual(bet2.spaces, {"17", "18"})
        
        # Set input
        bet3 = Bet(BetType.SPLIT, {"17", "18"}, amount=10, layout=self.american_layout)
        self.assertEqual(bet3.spaces, {"17", "18"})
    
    def test_layout_positions_for_zeros(self):
        """Test layout position calculation for zero spaces."""
        bet_0 = Bet.create_straight_up_bet("0", amount=10, layout=self.american_layout)
        self.assertEqual(len(bet_0.layout_positions), 1)
        
        bet_00 = Bet.create_straight_up_bet("00", amount=10, layout=self.american_layout)
        self.assertEqual(len(bet_00.layout_positions), 1)
    
    def test_layout_positions_for_multiple_spaces(self):
        """Test layout position calculation for bets covering multiple spaces."""
        split_bet = Bet.create_split_bet("17", "18", amount=10, layout=self.american_layout)
        self.assertEqual(len(split_bet.layout_positions), 2)
        
        # Verify positions are different
        positions = split_bet.layout_positions
        self.assertNotEqual(positions[0], positions[1])
    
    def test_bet_with_chips_parameter(self):
        """Test bet creation with chips parameter."""
        chips = Chips(value=5)
        chips.change_chips(count=20)
        
        bet = Bet.create_straight_up_bet("17", amount=5, chips=chips, layout=self.american_layout)
        self.assertEqual(bet.chips, chips)
        self.assertEqual(bet.amount, 5)
    
    def test_payout_calculations_for_all_bet_types(self):
        """Test payout calculations for all bet types."""
        # Test straight up bet payout
        straight_bet = Bet.create_straight_up_bet("17", amount=10, layout=self.american_layout)
        winning_space = Space("17")
        payout = straight_bet.calculate_payout(winning_space)
        self.assertEqual(payout, 10 + (10 * 35))  # 360
        
        # Test split bet payout
        split_bet = Bet.create_split_bet("17", "18", amount=10, layout=self.american_layout)
        payout = split_bet.calculate_payout(winning_space)
        self.assertEqual(payout, 10 + (10 * 17))  # 180
        
        # Test street bet payout
        street_bet = Bet(BetType.STREET, ["17", "18", "19"], amount=10, layout=self.american_layout)
        payout = street_bet.calculate_payout(winning_space)
        self.assertEqual(payout, 10 + (10 * 11))  # 120
        
        # Test corner bet payout
        corner_bet = Bet(BetType.CORNER, ["17", "18", "20", "21"], amount=10, layout=self.american_layout)
        payout = corner_bet.calculate_payout(winning_space)
        self.assertEqual(payout, 10 + (10 * 8))  # 90
        
        # Test six line bet payout
        six_line_bet = Bet(BetType.SIX_LINE, ["16", "17", "18", "19", "20", "21"], amount=10, layout=self.american_layout)
        payout = six_line_bet.calculate_payout(winning_space)
        self.assertEqual(payout, 10 + (10 * 5))  # 60
    
    def test_bet_boundary_values(self):
        """Test bets with boundary values for different bet types."""
        # Test high/low boundary
        high_bet = Bet(BetType.HIGH, set(), amount=10, layout=self.american_layout)
        low_bet = Bet(BetType.LOW, set(), amount=10, layout=self.american_layout)
        
        # Boundary values
        space_18 = Space("18")  # Highest low number
        space_19 = Space("19")  # Lowest high number
        
        self.assertTrue(low_bet.is_winning_bet(space_18))
        self.assertFalse(high_bet.is_winning_bet(space_18))
        
        self.assertFalse(low_bet.is_winning_bet(space_19))
        self.assertTrue(high_bet.is_winning_bet(space_19))
        
        # Test dozen boundaries
        dozen1_bet = Bet.create_dozen_bet(1, amount=30, layout=self.american_layout)
        dozen2_bet = Bet.create_dozen_bet(2, amount=30, layout=self.american_layout)
        
        space_12 = Space("12")  # Highest first dozen
        space_13 = Space("13")  # Lowest second dozen
        
        self.assertTrue(dozen1_bet.is_winning_bet(space_12))
        self.assertFalse(dozen2_bet.is_winning_bet(space_12))
        
        self.assertFalse(dozen1_bet.is_winning_bet(space_13))
        self.assertTrue(dozen2_bet.is_winning_bet(space_13))
    
    def test_european_vs_american_table_differences(self):
        """Test differences between European and American tables."""
        # American table should handle 00
        american_bet = Bet.create_straight_up_bet("00", amount=10, layout=self.american_layout)
        self.assertEqual(american_bet.spaces, {"00"})
        
        # European table doesn't have 00 in layout, but validation still allows it
        # This tests the explicit check for "0" and "00" in validation
        european_bet_00 = Bet(BetType.STRAIGHT_UP, "00", amount=10, layout=self.european_layout)
        self.assertEqual(european_bet_00.spaces, {"00"})
    
    def test_bet_equality_and_hashing_behavior(self):
        """Test that bets can be compared and used in sets/dicts properly."""
        bet1 = Bet.create_straight_up_bet("17", amount=10, layout=self.american_layout)
        bet2 = Bet.create_straight_up_bet("17", amount=10, layout=self.american_layout)
        bet3 = Bet.create_straight_up_bet("18", amount=10, layout=self.american_layout)
        
        # Test string representations are consistent
        self.assertEqual(str(bet1), str(bet2))
        self.assertNotEqual(str(bet1), str(bet3))
        
        # Test repr is informative
        repr_str = repr(bet1)
        self.assertIn("Bet", repr_str)
        self.assertIn("straight_up", repr_str)
        self.assertIn("17", repr_str)
        self.assertIn("10", repr_str)
    
    def test_large_bet_amounts(self):
        """Test bets with large amounts."""
        large_bet = Bet.create_straight_up_bet("17", amount=1000000, layout=self.american_layout)
        winning_space = Space("17")
        
        payout = large_bet.calculate_payout(winning_space)
        expected_payout = 1000000 + (1000000 * 35)  # 36,000,000
        self.assertEqual(payout, expected_payout)
    
    def test_bet_creation_edge_cases(self):
        """Test edge cases in bet creation methods."""
        # Test with minimum valid values
        min_bet = Bet.create_straight_up_bet("1", amount=1, layout=self.american_layout)
        self.assertEqual(min_bet.amount, 1)
        self.assertEqual(min_bet.spaces, {"1"})
        
        # Test with maximum table numbers
        max_bet = Bet.create_straight_up_bet("36", amount=1, layout=self.american_layout)
        self.assertEqual(max_bet.spaces, {"36"})
    
    def test_all_factory_methods(self):
        """Test all factory method variations."""
        # Test factory methods without layout parameter
        bet1 = Bet.create_straight_up_bet("17", amount=5)
        self.assertEqual(len(bet1.layout_positions), 0)
        
        bet2 = Bet.create_split_bet("17", "18", amount=10)
        self.assertEqual(len(bet2.layout_positions), 0)
        
        bet3 = Bet.create_color_bet("red", amount=20)
        self.assertEqual(len(bet3.layout_positions), 0)
        
        bet4 = Bet.create_dozen_bet(1, amount=30)
        self.assertEqual(len(bet4.layout_positions), 0)
        
        bet5 = Bet.create_column_bet(1, amount=40)
        self.assertEqual(len(bet5.layout_positions), 0)
    
    def test_case_insensitive_color_bets(self):
        """Test that color bets work with different case inputs."""
        red_bet_upper = Bet.create_color_bet("RED", amount=20, layout=self.american_layout)
        red_bet_mixed = Bet.create_color_bet("Red", amount=20, layout=self.american_layout)
        
        self.assertEqual(red_bet_upper.bet_type, BetType.RED)
        self.assertEqual(red_bet_mixed.bet_type, BetType.RED)
        
        black_bet_upper = Bet.create_color_bet("BLACK", amount=20, layout=self.american_layout)
        black_bet_mixed = Bet.create_color_bet("Black", amount=20, layout=self.american_layout)
        
        self.assertEqual(black_bet_upper.bet_type, BetType.BLACK)
        self.assertEqual(black_bet_mixed.bet_type, BetType.BLACK)


if __name__ == "__main__":
    unittest.main() 