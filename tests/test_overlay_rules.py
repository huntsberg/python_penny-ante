"""
Test cases for overlay rules functionality in BettingRules.
"""

import unittest
import tempfile
import os
from src.penny_ante.betting_rules import BettingRules
from src.penny_ante.game import Game


class TestOverlayRules(unittest.TestCase):
    """Test overlay rules functionality."""
    
    def test_no_overlay_uses_defaults(self):
        """Test that no overlay results in default configuration."""
        rules = BettingRules(table_type="AMERICAN")
        
        # Should use default American values
        self.assertEqual(rules.table_limits['minimum_bet'], 1)
        self.assertEqual(rules.table_limits['maximum_bet'], 1000000)
        self.assertEqual(rules.payout_ratios['straight_up'], 35)
        self.assertFalse(rules.game_rules.get('en_prison', False))
    
    def test_table_limits_overlay(self):
        """Test overlaying only table limits."""
        overlay = {
            "table_limits": {
                "minimum_bet": 25,
                "maximum_bet": 5000000
            }
        }
        
        rules = BettingRules(table_type="AMERICAN", overlay_config=overlay)
        
        # Overlaid values should be used
        self.assertEqual(rules.table_limits['minimum_bet'], 25)
        self.assertEqual(rules.table_limits['maximum_bet'], 5000000)
        
        # Other values should remain default
        self.assertEqual(rules.payout_ratios['straight_up'], 35)
        self.assertEqual(rules.minimum_bet_ratios['red'], 5.0)
        self.assertFalse(rules.game_rules.get('en_prison', False))
    
    def test_payout_ratios_overlay(self):
        """Test overlaying only some payout ratios."""
        overlay = {
            "payout_ratios": {
                "straight_up": 40,
                "split": 20
            }
        }
        
        rules = BettingRules(table_type="AMERICAN", overlay_config=overlay)
        
        # Overlaid payouts should be used
        self.assertEqual(rules.payout_ratios['straight_up'], 40)
        self.assertEqual(rules.payout_ratios['split'], 20)
        
        # Non-overlaid payouts should remain default
        self.assertEqual(rules.payout_ratios['red'], 1)
        self.assertEqual(rules.payout_ratios['corner'], 8)
        
        # Other sections should remain default
        self.assertEqual(rules.table_limits['minimum_bet'], 1)
        self.assertFalse(rules.game_rules.get('en_prison', False))
    
    def test_game_rules_overlay(self):
        """Test overlaying game rules."""
        overlay = {
            "game_rules": {
                "surrender": True,
                "maximum_repeats": 5
            }
        }
        
        rules = BettingRules(table_type="AMERICAN", overlay_config=overlay)
        
        # Overlaid game rules should be used
        self.assertTrue(rules.game_rules.get('surrender', False))
        self.assertEqual(rules.game_rules.get('maximum_repeats', 10), 5)
        
        # Non-overlaid game rules should remain default
        self.assertFalse(rules.game_rules.get('en_prison', False))
        self.assertFalse(rules.game_rules.get('la_partage', False))
        
        # Other sections should remain default
        self.assertEqual(rules.payout_ratios['straight_up'], 35)
        self.assertEqual(rules.table_limits['minimum_bet'], 1)
    
    def test_comprehensive_overlay(self):
        """Test overlaying multiple sections simultaneously."""
        overlay = {
            "table_limits": {
                "minimum_bet": 100
            },
            "payout_ratios": {
                "straight_up": 42
            },
            "game_rules": {
                "surrender": True
            },
            "minimum_bet_ratios": {
                "red": 10.0
            }
        }
        
        rules = BettingRules(table_type="AMERICAN", overlay_config=overlay)
        
        # All overlaid values should be used
        self.assertEqual(rules.table_limits['minimum_bet'], 100)
        self.assertEqual(rules.payout_ratios['straight_up'], 42)
        self.assertTrue(rules.game_rules.get('surrender', False))
        self.assertEqual(rules.minimum_bet_ratios['red'], 10.0)
        
        # Non-overlaid values should remain default
        self.assertEqual(rules.table_limits['maximum_bet'], 1000000)
        self.assertEqual(rules.payout_ratios['split'], 17)
        self.assertFalse(rules.game_rules.get('en_prison', False))
        self.assertEqual(rules.minimum_bet_ratios['black'], 5.0)
    
    def test_european_base_with_overlay(self):
        """Test overlay on European base configuration."""
        overlay = {
            "table_limits": {
                "minimum_bet": 5
            },
            "game_rules": {
                "la_partage": False
            }
        }
        
        rules = BettingRules(table_type="EUROPEAN", overlay_config=overlay)
        
        # Overlaid values should be used
        self.assertEqual(rules.table_limits['minimum_bet'], 5)
        self.assertFalse(rules.game_rules.get('la_partage', True))
        
        # European defaults should be preserved where not overlaid
        self.assertEqual(rules.table_limits['maximum_bet'], 2000000)
        self.assertTrue(rules.game_rules.get('en_prison', False))
        self.assertEqual(rules.payout_ratios['straight_up'], 35)
    
    def test_game_class_integration(self):
        """Test that Game class properly uses overlay rules."""
        overlay = {
            "table_limits": {
                "minimum_bet": 50
            },
            "payout_ratios": {
                "straight_up": 38
            }
        }
        
        game = Game(table_type="AMERICAN", overlay_rules=overlay)
        
        # Overlay values should be applied
        self.assertEqual(game.betting_rules.table_limits['minimum_bet'], 50)
        self.assertEqual(game.betting_rules.payout_ratios['straight_up'], 38)
        
        # Default values should be preserved
        self.assertEqual(game.betting_rules.table_limits['maximum_bet'], 1000000)
        self.assertEqual(game.betting_rules.payout_ratios['red'], 1)
    
    def test_empty_overlay(self):
        """Test that empty overlay doesn't affect configuration."""
        overlay = {}
        
        rules = BettingRules(table_type="AMERICAN", overlay_config=overlay)
        rules_no_overlay = BettingRules(table_type="AMERICAN")
        
        # Should be identical to no overlay
        self.assertEqual(rules.table_limits, rules_no_overlay.table_limits)
        self.assertEqual(rules.payout_ratios, rules_no_overlay.payout_ratios)
        self.assertEqual(rules.game_rules, rules_no_overlay.game_rules)
    
    def test_overlay_validation_still_works(self):
        """Test that overlaid configuration still gets validated."""
        # This should still fail validation because required sections are missing
        # when only overlay is provided (no base config)
        overlay = {
            "table_limits": {
                "minimum_bet": 50
            }
        }
        
        # Should work because we have a base config that provides required sections
        rules = BettingRules(table_type="AMERICAN", overlay_config=overlay)
        self.assertEqual(rules.table_limits['minimum_bet'], 50)
    
    def test_overlay_with_custom_config_file(self):
        """Test overlay works with custom config files."""
        # Create a custom config file
        custom_config = """
payout_ratios:
  straight_up: 30
  red: 1

minimum_bet_ratios:
  global: 1.0
  straight_up: 1.0
  red: 5.0

maximum_bet_ratios:
  global: 1.0
  straight_up: 0.5
  red: 1.0

table_limits:
  minimum_bet: 10
  maximum_bet: 500000

game_rules:
  en_prison: false

special_rules:
  allow_call_bets: false
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(custom_config)
            custom_config_path = f.name
        
        try:
            overlay = {
                "table_limits": {
                    "minimum_bet": 20
                },
                "payout_ratios": {
                    "straight_up": 45
                }
            }
            
            rules = BettingRules(
                config_path=custom_config_path, 
                table_type="AMERICAN", 
                overlay_config=overlay
            )
            
            # Overlay values should override custom config
            self.assertEqual(rules.table_limits['minimum_bet'], 20)
            self.assertEqual(rules.payout_ratios['straight_up'], 45)
            
            # Non-overlaid values should come from custom config
            self.assertEqual(rules.table_limits['maximum_bet'], 500000)
            self.assertEqual(rules.payout_ratios['red'], 1)
            
        finally:
            os.unlink(custom_config_path)


if __name__ == '__main__':
    unittest.main()