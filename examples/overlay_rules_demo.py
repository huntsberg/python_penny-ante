#!/usr/bin/env python3
"""
Overlay Rules Demo - Demonstrates how to create custom rules that overlay on defaults.

This demo shows how users can create partial configurations that inherit
missing values from the default rules, allowing for easy customization
without having to specify every single setting.
"""

from penny_ante.game import Game
from penny_ante.betting_rules import BettingRules


def main():
    """Demonstrate the overlay rules functionality."""
    print("🎰 Penny Ante Overlay Rules Demo 🎰\n")
    
    # === BASELINE: STANDARD AMERICAN GAME ===
    print("=== BASELINE: STANDARD AMERICAN GAME ===")
    standard_game = Game(table_type="AMERICAN")
    
    print("Standard American table configuration:")
    print(f"  • Table minimum: ${standard_game.betting_rules.table_limits['minimum_bet']}")
    print(f"  • Table maximum: ${standard_game.betting_rules.table_limits['maximum_bet']:,}")
    print(f"  • Straight up payout: {standard_game.betting_rules.payout_ratios['straight_up']}:1")
    print(f"  • Red minimum ratio: {standard_game.betting_rules.minimum_bet_ratios['red']}")
    print(f"  • En prison rule: {standard_game.betting_rules.game_rules.get('en_prison', False)}")
    print(f"  • Surrender rule: {standard_game.betting_rules.game_rules.get('surrender', False)}")
    print()
    
    # === EXAMPLE 1: HIGHER TABLE LIMITS ONLY ===
    print("=== EXAMPLE 1: HIGHER TABLE LIMITS ONLY ===")
    high_limits_overlay = {
        "table_limits": {
            "minimum_bet": 25,
            "maximum_bet": 5000000
        }
    }
    
    high_limits_game = Game(
        table_type="AMERICAN", 
        overlay_rules=high_limits_overlay
    )
    
    print("High limits overlay (only table limits changed):")
    print(f"  • Table minimum: ${high_limits_game.betting_rules.table_limits['minimum_bet']} (was $1)")
    print(f"  • Table maximum: ${high_limits_game.betting_rules.table_limits['maximum_bet']:,} (was $1,000,000)")
    print(f"  • Straight up payout: {high_limits_game.betting_rules.payout_ratios['straight_up']}:1 (unchanged)")
    print(f"  • Red minimum ratio: {high_limits_game.betting_rules.minimum_bet_ratios['red']} (unchanged)")
    print(f"  • En prison rule: {high_limits_game.betting_rules.game_rules.get('en_prison', False)} (unchanged)")
    print()
    
    # === EXAMPLE 2: CUSTOM PAYOUTS ONLY ===
    print("=== EXAMPLE 2: CUSTOM PAYOUTS ONLY ===")
    custom_payouts_overlay = {
        "payout_ratios": {
            "straight_up": 40,  # Higher than standard 35:1
            "split": 20,        # Higher than standard 17:1
            "first_dozen": 3    # Higher than standard 2:1
        }
    }
    
    custom_payouts_game = Game(
        table_type="AMERICAN", 
        overlay_rules=custom_payouts_overlay
    )
    
    print("Custom payouts overlay (only some payouts changed):")
    print(f"  • Straight up payout: {custom_payouts_game.betting_rules.payout_ratios['straight_up']}:1 (was 35:1)")
    print(f"  • Split payout: {custom_payouts_game.betting_rules.payout_ratios['split']}:1 (was 17:1)")
    print(f"  • First dozen payout: {custom_payouts_game.betting_rules.payout_ratios['first_dozen']}:1 (was 2:1)")
    print(f"  • Red payout: {custom_payouts_game.betting_rules.payout_ratios['red']}:1 (unchanged)")
    print(f"  • Table minimum: ${custom_payouts_game.betting_rules.table_limits['minimum_bet']} (unchanged)")
    print(f"  • Table maximum: ${custom_payouts_game.betting_rules.table_limits['maximum_bet']:,} (unchanged)")
    print()
    
    # === EXAMPLE 3: SPECIAL RULES ONLY ===
    print("=== EXAMPLE 3: SPECIAL RULES ONLY ===")
    special_rules_overlay = {
        "game_rules": {
            "surrender": True,      # Enable surrender (normally false for American)
            "maximum_repeats": 5    # Stricter monitoring
        },
        "special_rules": {
            "allow_call_bets": True,      # Enable call bets
            "progressive_betting": False  # Disable progressive betting
        }
    }
    
    special_rules_game = Game(
        table_type="AMERICAN", 
        overlay_rules=special_rules_overlay
    )
    
    print("Special rules overlay (only rules changed):")
    print(f"  • En prison rule: {special_rules_game.betting_rules.game_rules.get('en_prison', False)} (unchanged)")
    print(f"  • Surrender rule: {special_rules_game.betting_rules.game_rules.get('surrender', False)} (was False)")
    print(f"  • Maximum repeats: {special_rules_game.betting_rules.game_rules.get('maximum_repeats', 10)} (was 10)")
    print(f"  • Call bets allowed: {special_rules_game.betting_rules.special_rules.get('allow_call_bets', False)} (was False)")
    print(f"  • Progressive betting: {special_rules_game.betting_rules.special_rules.get('progressive_betting', True)} (was True)")
    print(f"  • All payouts unchanged: {special_rules_game.betting_rules.payout_ratios['straight_up']}:1")
    print(f"  • All limits unchanged: ${special_rules_game.betting_rules.table_limits['minimum_bet']} - ${special_rules_game.betting_rules.table_limits['maximum_bet']:,}")
    print()
    
    # === EXAMPLE 4: COMPREHENSIVE OVERLAY ===
    print("=== EXAMPLE 4: COMPREHENSIVE OVERLAY ===")
    comprehensive_overlay = {
        "table_limits": {
            "minimum_bet": 100,
            "maximum_bet": 10000000
        },
        "payout_ratios": {
            "straight_up": 42
        },
        "minimum_bet_ratios": {
            "red": 10.0,    # Higher minimum for outside bets
            "black": 10.0
        },
        "game_rules": {
            "surrender": True,
            "maximum_repeats": 3
        }
    }
    
    comprehensive_game = Game(
        table_type="AMERICAN", 
        overlay_rules=comprehensive_overlay
    )
    
    print("Comprehensive overlay (multiple sections changed):")
    print(f"  • Table minimum: ${comprehensive_game.betting_rules.table_limits['minimum_bet']} (was $1)")
    print(f"  • Table maximum: ${comprehensive_game.betting_rules.table_limits['maximum_bet']:,} (was $1,000,000)")
    print(f"  • Straight up payout: {comprehensive_game.betting_rules.payout_ratios['straight_up']}:1 (was 35:1)")
    print(f"  • Split payout: {comprehensive_game.betting_rules.payout_ratios['split']}:1 (unchanged)")
    print(f"  • Red minimum ratio: {comprehensive_game.betting_rules.minimum_bet_ratios['red']} (was 5.0)")
    print(f"  • Odd minimum ratio: {comprehensive_game.betting_rules.minimum_bet_ratios['odd']} (unchanged)")
    print(f"  • Surrender rule: {comprehensive_game.betting_rules.game_rules.get('surrender', False)} (was False)")
    print(f"  • En prison rule: {comprehensive_game.betting_rules.game_rules.get('en_prison', False)} (unchanged)")
    print()
    
    # === EXAMPLE 5: EUROPEAN BASE WITH OVERLAY ===
    print("=== EXAMPLE 5: EUROPEAN BASE WITH OVERLAY ===")
    european_overlay = {
        "table_limits": {
            "minimum_bet": 5
        },
        "game_rules": {
            "la_partage": False  # Disable la partage
        }
    }
    
    european_game = Game(
        table_type="EUROPEAN", 
        overlay_rules=european_overlay
    )
    
    print("European base with overlay:")
    print(f"  • Table minimum: ${european_game.betting_rules.table_limits['minimum_bet']} (was $2)")
    print(f"  • Table maximum: ${european_game.betting_rules.table_limits['maximum_bet']:,} (unchanged)")
    print(f"  • En prison rule: {european_game.betting_rules.game_rules.get('en_prison', False)} (unchanged)")
    print(f"  • La partage rule: {european_game.betting_rules.game_rules.get('la_partage', True)} (was True)")
    print(f"  • All payouts unchanged: {european_game.betting_rules.payout_ratios['straight_up']}:1")
    print()
    
    # === DEMONSTRATION: BETTING WITH OVERLAY RULES ===
    print("=== DEMONSTRATION: BETTING WITH OVERLAY RULES ===")
    
    # Test with high limits game
    print("Testing with high limits overlay:")
    min_bet = high_limits_game.betting_rules.get_minimum_bet("straight_up")
    max_bet = high_limits_game.betting_rules.get_maximum_bet("straight_up")
    print(f"  • Straight up bet range: ${min_bet} - ${max_bet:,}")
    
    # Test with custom payouts game  
    print("Testing with custom payouts overlay:")
    payout_ratio = custom_payouts_game.betting_rules.get_payout_ratio("straight_up")
    print(f"  • Straight up payout ratio: {payout_ratio}:1")
    
    print()
    
    # === COMPARISON TABLE ===
    print("=== OVERLAY COMPARISON TABLE ===")
    print(f"{'Setting':<20} {'Standard':<12} {'High Limits':<12} {'Custom Payouts':<15} {'Special Rules':<13}")
    print("-" * 80)
    print(f"{'Min Bet':<20} ${standard_game.betting_rules.table_limits['minimum_bet']:<11} ${high_limits_game.betting_rules.table_limits['minimum_bet']:<11} ${custom_payouts_game.betting_rules.table_limits['minimum_bet']:<14} ${special_rules_game.betting_rules.table_limits['minimum_bet']:<12}")
    print(f"{'Max Bet':<20} ${standard_game.betting_rules.table_limits['maximum_bet']:<11,} ${high_limits_game.betting_rules.table_limits['maximum_bet']:<11,} ${custom_payouts_game.betting_rules.table_limits['maximum_bet']:<14,} ${special_rules_game.betting_rules.table_limits['maximum_bet']:<12,}")
    print(f"{'Straight Up':<20} {standard_game.betting_rules.payout_ratios['straight_up']}:1{'':<8} {high_limits_game.betting_rules.payout_ratios['straight_up']}:1{'':<8} {custom_payouts_game.betting_rules.payout_ratios['straight_up']}:1{'':<11} {special_rules_game.betting_rules.payout_ratios['straight_up']}:1{'':<9}")
    print(f"{'Surrender':<20} {standard_game.betting_rules.game_rules.get('surrender', False)!s:<11} {high_limits_game.betting_rules.game_rules.get('surrender', False)!s:<11} {custom_payouts_game.betting_rules.game_rules.get('surrender', False)!s:<14} {special_rules_game.betting_rules.game_rules.get('surrender', False)!s:<12}")
    
    print("\n🎰 Overlay Rules Demo Complete! 🎰")
    print("\nKey Features Demonstrated:")
    print("  ✓ Partial configuration overlays")
    print("  ✓ Inheritance from default values")
    print("  ✓ Section-specific customization")
    print("  ✓ Multiple overlay combinations")
    print("  ✓ European and American base configurations")
    print("  ✓ Seamless integration with existing API")
    
    print("\nBenefits:")
    print("  ✓ Reduced configuration complexity")
    print("  ✓ Easy customization of specific settings")
    print("  ✓ Automatic inheritance of sensible defaults")
    print("  ✓ No need to specify complete configurations")
    print("  ✓ Type-safe integration with Game class")


if __name__ == "__main__":
    main()