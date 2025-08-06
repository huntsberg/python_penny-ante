import unittest
import tempfile
import os
from pathlib import Path

from .context import penny_ante
from penny_ante.betting_rules import BettingRules
from penny_ante.bet import BetType


class TestBettingRules(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary config file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_rules.yaml")
        
        # Test configuration with ratio-based maximum bets
        self.test_config = """
payout_ratios:
  straight_up: 35
  split: 17
  red: 1
  first_dozen: 2

minimum_bet_ratios:
  global: 5.0
  straight_up: 0.2
  red: 10.0

maximum_bet_ratios:
  global: 1.0
  straight_up: 0.5
  split: 0.75
  red: 1.0

# Note: house_edge now calculated automatically

table_limits:
  minimum_bet: 5
  maximum_bet: 100000
  maximum_total_bet: 1000000
"""
        
        with open(self.config_path, 'w') as f:
            f.write(self.test_config)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    def test_load_configuration_from_file(self):
        """Test loading configuration from YAML file."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        self.assertEqual(rules.table_type, "AMERICAN")
        self.assertEqual(rules.get_payout_ratio(BetType.STRAIGHT_UP), 35)
        self.assertEqual(rules.get_payout_ratio(BetType.RED), 1)
    
    def test_default_configuration_loading(self):
        """Test loading the default configuration file."""
        # This should load the actual config/betting_rules.yaml
        rules = BettingRules(table_type="AMERICAN")
        
        self.assertEqual(rules.table_type, "AMERICAN")
        self.assertIsInstance(rules.get_payout_ratio(BetType.STRAIGHT_UP), int)
        self.assertIsInstance(rules.get_table_minimum(), int)
    
    def test_ratio_based_maximum_bets(self):
        """Test that maximum bets are calculated correctly from ratios."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        table_max = rules.get_table_maximum()  # 100000 from config
        
        # Test specific ratios
        straight_up_max = rules.get_maximum_bet(BetType.STRAIGHT_UP)
        self.assertEqual(straight_up_max, int(table_max * 0.5))  # 50000
        
        split_max = rules.get_maximum_bet(BetType.SPLIT)
        self.assertEqual(split_max, int(table_max * 0.75))  # 75000
        
        red_max = rules.get_maximum_bet(BetType.RED)
        self.assertEqual(red_max, int(table_max * 1.0))  # 100000
    
    def test_get_maximum_bet_ratio(self):
        """Test getting maximum bet ratios."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        self.assertEqual(rules.get_maximum_bet_ratio(BetType.STRAIGHT_UP), 0.5)
        self.assertEqual(rules.get_maximum_bet_ratio(BetType.SPLIT), 0.75)
        self.assertEqual(rules.get_maximum_bet_ratio(BetType.RED), 1.0)
        
        # Test fallback to global ratio
        self.assertEqual(rules.get_maximum_bet_ratio(BetType.EVEN), 1.0)  # Uses global
    
    def test_minimum_bet_rules(self):
        """Test minimum bet calculations with ratios."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        # Table minimum is 5, straight_up ratio is 0.2, so 5 * 0.2 = 1
        self.assertEqual(rules.get_minimum_bet(BetType.STRAIGHT_UP), 1)
        # Table minimum is 5, red ratio is 10.0, so 5 * 10.0 = 50
        self.assertEqual(rules.get_minimum_bet(BetType.RED), 50)
        
        # Test fallback to global minimum ratio (5.0), so 5 * 5.0 = 25
        self.assertEqual(rules.get_minimum_bet(BetType.EVEN), 25)  # Uses global
    
    def test_minimum_bet_ratios(self):
        """Test minimum bet ratio retrieval."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        self.assertEqual(rules.get_minimum_bet_ratio(BetType.STRAIGHT_UP), 0.2)
        self.assertEqual(rules.get_minimum_bet_ratio(BetType.RED), 10.0)
        
        # Test fallback to global ratio
        self.assertEqual(rules.get_minimum_bet_ratio(BetType.EVEN), 5.0)  # Uses global
    
    def test_payout_ratio_retrieval(self):
        """Test payout ratio retrieval."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        self.assertEqual(rules.get_payout_ratio(BetType.STRAIGHT_UP), 35)
        self.assertEqual(rules.get_payout_ratio(BetType.SPLIT), 17)
        self.assertEqual(rules.get_payout_ratio(BetType.RED), 1)
        
        # Test error for missing payout ratio
        with self.assertRaises(ValueError):
            rules.get_payout_ratio(BetType.EVEN)  # Not in test config
    
    def test_house_edge_calculation(self):
        """Test calculated house edge."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        # House edge should be calculated based on payout ratios and table type
        # American table has 38 pockets, so house edge for all standard bets should be 5.26%
        self.assertAlmostEqual(rules.get_house_edge(BetType.STRAIGHT_UP), 5.26, places=2)
        self.assertAlmostEqual(rules.get_house_edge(BetType.RED), 5.26, places=2)
        
        # Test European table (37 pockets)
        rules_european = BettingRules(config_path=self.config_path, table_type="EUROPEAN")
        self.assertAlmostEqual(rules_european.get_house_edge(BetType.STRAIGHT_UP), 2.70, places=2)
        self.assertAlmostEqual(rules_european.get_house_edge(BetType.RED), 2.70, places=2)
    
    def test_bet_amount_validation(self):
        """Test bet amount validation with ratio-based minimums."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        # Valid amounts
        self.assertTrue(rules.validate_bet_amount(BetType.STRAIGHT_UP, 50))  # Between 1 and 50000
        self.assertTrue(rules.validate_bet_amount(BetType.RED, 100))  # Between 50 and 100000
        
        # Invalid amounts - too low (red minimum is now 50, not 10)
        self.assertFalse(rules.validate_bet_amount(BetType.RED, 25))  # Below minimum of 50
        
        # Invalid amounts - too high
        self.assertFalse(rules.validate_bet_amount(BetType.STRAIGHT_UP, 60000))  # Above max of 50000
    
    def test_table_limits(self):
        """Test table limit retrieval."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        self.assertEqual(rules.get_table_minimum(), 5)
        self.assertEqual(rules.get_table_maximum(), 100000)
        self.assertEqual(rules.get_maximum_total_bet(), 1000000)
    
    def test_bet_allowance_check(self):
        """Test checking if bet types are allowed."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        # These are in the payout ratios, so should be allowed
        self.assertTrue(rules.is_bet_allowed(BetType.STRAIGHT_UP))
        self.assertTrue(rules.is_bet_allowed(BetType.RED))
        
        # This is not in the payout ratios, so should not be allowed
        self.assertFalse(rules.is_bet_allowed(BetType.EVEN))
    
    def test_table_info_retrieval(self):
        """Test comprehensive table information retrieval."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        info = rules.get_table_info()
        
        self.assertEqual(info['table_type'], 'AMERICAN')
        self.assertEqual(info['minimum_bet'], 5)
        self.assertEqual(info['maximum_bet'], 100000)
        self.assertEqual(info['maximum_total_bet'], 1000000)
        self.assertIn('payout_ratios', info)
        self.assertIn('house_edge_calculated', info)
        self.assertIn('total_pockets', info)
    
    def test_configuration_validation_errors(self):
        """Test configuration validation with missing sections."""
        # Create invalid config
        invalid_config = """
payout_ratios:
  straight_up: 35
# Missing required sections
"""
        invalid_path = os.path.join(self.temp_dir, "invalid.yaml")
        with open(invalid_path, 'w') as f:
            f.write(invalid_config)
        
        with self.assertRaises(ValueError):
            BettingRules(config_path=invalid_path, table_type="AMERICAN")
        
        os.remove(invalid_path)
    
    def test_missing_required_sections(self):
        """Test error when required configuration sections are missing."""
        config_without_required = """
payout_ratios:
  straight_up: 35
minimum_bet_ratios:
  global: 1.0
# Missing maximum_bet_ratios and table_limits
"""
        missing_sections_path = os.path.join(self.temp_dir, "missing_sections.yaml")
        with open(missing_sections_path, 'w') as f:
            f.write(config_without_required)
        
        with self.assertRaises(ValueError):
            BettingRules(config_path=missing_sections_path, table_type="AMERICAN")
        
        os.remove(missing_sections_path)
    
    def test_file_not_found_error(self):
        """Test error when configuration file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            BettingRules(config_path="nonexistent.yaml", table_type="AMERICAN")
    
    def test_create_default_config(self):
        """Test creating a default configuration file."""
        default_path = os.path.join(self.temp_dir, "default.yaml")
        
        BettingRules.create_default_config(default_path)
        
        self.assertTrue(os.path.exists(default_path))
        
        # Test that the created config can be loaded
        rules = BettingRules(config_path=default_path, table_type="AMERICAN")
        self.assertEqual(rules.get_payout_ratio(BetType.STRAIGHT_UP), 35)
        
        os.remove(default_path)
    
    def test_string_representations(self):
        """Test string representation methods."""
        rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        
        str_repr = str(rules)
        self.assertIn("BettingRules", str_repr)
        self.assertIn("AMERICAN", str_repr)
        self.assertIn("5", str_repr)  # minimum bet
        self.assertIn("100000", str_repr)  # maximum bet
        
        repr_str = repr(rules)
        self.assertIn("BettingRules", repr_str)
        self.assertIn(self.config_path, repr_str)
        self.assertIn("AMERICAN", repr_str)
    
    def test_different_table_types(self):
        """Test configuration with different table types."""
        american_rules = BettingRules(config_path=self.config_path, table_type="AMERICAN")
        european_rules = BettingRules(config_path=self.config_path, table_type="EUROPEAN")
        
        # Both should have same table limits from config
        self.assertEqual(american_rules.get_table_minimum(), european_rules.get_table_minimum())
        self.assertEqual(american_rules.get_table_maximum(), european_rules.get_table_maximum())
        
        # But different calculated house edges
        self.assertAlmostEqual(american_rules.get_house_edge(BetType.RED), 5.26, places=2)
        self.assertAlmostEqual(european_rules.get_house_edge(BetType.RED), 2.70, places=2)
    
    def test_edge_case_ratios(self):
        """Test edge cases for bet ratios."""
        # Create config with extreme ratios
        extreme_config = """
payout_ratios:
  straight_up: 35
  red: 1

minimum_bet_ratios:
  global: 1.0

maximum_bet_ratios:
  global: 1.0
  straight_up: 0.1  # Very low ratio
  red: 2.0          # Ratio above 1.0

table_limits:
  minimum_bet: 1
  maximum_bet: 1000
  maximum_total_bet: 10000
"""
        extreme_path = os.path.join(self.temp_dir, "extreme.yaml")
        with open(extreme_path, 'w') as f:
            f.write(extreme_config)
        
        rules = BettingRules(config_path=extreme_path, table_type="AMERICAN")
        
        # Test very low ratio
        straight_up_max = rules.get_maximum_bet(BetType.STRAIGHT_UP)
        self.assertEqual(straight_up_max, 100)  # 1000 * 0.1
        
        # Test ratio above 1.0
        red_max = rules.get_maximum_bet(BetType.RED)
        self.assertEqual(red_max, 2000)  # 1000 * 2.0
        
        os.remove(extreme_path)


if __name__ == "__main__":
    unittest.main() 