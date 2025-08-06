#!/usr/bin/env python3
"""
Separate Configuration Demo - Demonstrates table-specific betting rules.

This script shows how the betting rules system automatically selects the
appropriate configuration file (American or European) based on table type,
and how to use custom configuration files with the Game class.
"""

from penny_ante import Game, Bet, BetType, BettingRules
import tempfile
import os


def create_high_stakes_american_config():
    """Create a custom high-stakes American configuration."""
    config = """
# High Stakes American Roulette Configuration
payout_ratios:
  straight_up: 40        # Higher payout than standard
  split: 20
  street: 13
  corner: 10
  six_line: 6
  red: 1
  black: 1
  odd: 1
  even: 1
  high: 1
  low: 1
  first_dozen: 3         # Higher dozen payout
  second_dozen: 3
  third_dozen: 3
  first_column: 3
  second_column: 3
  third_column: 3

minimum_bets:
  global: 100            # High minimum
  straight_up: 50
  red: 500               # Very high outside bet minimum
  black: 500
  odd: 500
  even: 500
  high: 500
  low: 500

minimum_bet_ratios:
  global: 1.0
  straight_up: 5.0       # Higher minimum for inside bets
  split: 5.0
  street: 5.0
  corner: 5.0
  six_line: 5.0
  red: 10.0              # Higher minimum for outside bets
  black: 10.0
  odd: 10.0
  even: 10.0
  high: 10.0
  low: 10.0
  first_dozen: 10.0
  second_dozen: 10.0
  third_dozen: 10.0
  first_column: 10.0
  second_column: 10.0
  third_column: 10.0

maximum_bet_ratios:
  global: 1.0
  straight_up: 0.25      # Conservative for high payouts
  split: 0.4
  street: 0.6
  red: 1.0

table_limits:
  minimum_bet: 100
  maximum_bet: 10000000  # 10 million max
  maximum_total_bet: 100000000

game_rules:
  en_prison: false
  la_partage: false
  surrender: true        # Offer surrender on high stakes
  maximum_repeats: 5     # Strict monitoring

special_rules:
  allow_call_bets: true
  allow_neighbor_bets: true
  progressive_betting: true
  maximum_parlay: 3      # Limited parlay on high stakes
"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
    temp_file.write(config)
    temp_file.close()
    return temp_file.name


def main():
    """Demonstrate the separate configuration system."""
    print("🎰 Penny Ante Separate Configuration Demo 🎰\n")
    
    # === AUTOMATIC CONFIGURATION SELECTION ===
    print("=== AUTOMATIC CONFIGURATION SELECTION ===")
    print("Creating games with automatic config selection based on table type...\n")
    
    # American table - automatically uses american_rules.yaml
    print("🇺🇸 AMERICAN TABLE (automatic config)")
    american_game = Game(table_type="AMERICAN")
    print(f"  Config file: {american_game.betting_rules.config_path}")
    print(f"  Table minimum: ${american_game.betting_rules.get_table_minimum()}")
    print(f"  Table maximum: ${american_game.betting_rules.get_table_maximum():,}")
    print(f"  Straight up max ratio: {american_game.betting_rules.get_maximum_bet_ratio(BetType.STRAIGHT_UP)}")
    print(f"  House edge: {american_game.betting_rules.get_house_edge(BetType.RED):.2f}%")
    print()
    
    # European table - automatically uses european_rules.yaml
    print("🇪🇺 EUROPEAN TABLE (automatic config)")
    european_game = Game(table_type="EUROPEAN")
    print(f"  Config file: {european_game.betting_rules.config_path}")
    print(f"  Table minimum: ${european_game.betting_rules.get_table_minimum()}")
    print(f"  Table maximum: ${european_game.betting_rules.get_table_maximum():,}")
    print(f"  Straight up max ratio: {european_game.betting_rules.get_maximum_bet_ratio(BetType.STRAIGHT_UP)}")
    print(f"  House edge: {european_game.betting_rules.get_house_edge(BetType.RED):.2f}%")
    print()
    
    # === CONFIGURATION COMPARISON ===
    print("=== AMERICAN vs EUROPEAN CONFIGURATION DIFFERENCES ===")
    print(f"{'Attribute':<20} {'American':<15} {'European':<15} {'Difference'}")
    print("-" * 65)
    
    comparisons = [
        ("Table Minimum", american_game.betting_rules.get_table_minimum(), 
         european_game.betting_rules.get_table_minimum()),
        ("Table Maximum", american_game.betting_rules.get_table_maximum(), 
         european_game.betting_rules.get_table_maximum()),
        ("Straight Up Max %", american_game.betting_rules.get_maximum_bet_ratio(BetType.STRAIGHT_UP), 
         european_game.betting_rules.get_maximum_bet_ratio(BetType.STRAIGHT_UP)),
        ("House Edge %", american_game.betting_rules.get_house_edge(BetType.RED), 
         european_game.betting_rules.get_house_edge(BetType.RED)),
        ("Red Min Bet", american_game.betting_rules.get_minimum_bet(BetType.RED), 
         european_game.betting_rules.get_minimum_bet(BetType.RED)),
    ]
    
    for attr, american_val, european_val in comparisons:
        if attr == "House Edge %":
            diff = f"{american_val - european_val:+.2f}%"
            print(f"{attr:<20} {american_val:.2f}%{'':<8} {european_val:.2f}%{'':<8} {diff}")
        elif attr == "Straight Up Max %":
            diff = f"{american_val - european_val:+.1f}"
            print(f"{attr:<20} {american_val}{'':<14} {european_val}{'':<14} {diff}")
        elif "Maximum" in attr:
            diff = f"${european_val - american_val:+,}"
            print(f"{attr:<20} ${american_val:,}{'':<7} ${european_val:,}{'':<7} {diff}")
        else:
            diff = f"{european_val - american_val:+d}"
            print(f"{attr:<20} {american_val}{'':<14} {european_val}{'':<14} {diff}")
    print()
    
    # === CUSTOM CONFIGURATION WITH GAME ===
    print("=== CUSTOM CONFIGURATION WITH GAME ===")
    
    high_stakes_config_path = create_high_stakes_american_config()
    try:
        print("💰 HIGH STAKES AMERICAN TABLE (custom config)")
        high_stakes_game = Game(
            table_type="AMERICAN", 
            betting_rules_config=high_stakes_config_path
        )
        
        print(f"  Config file: {high_stakes_game.betting_rules.config_path}")
        print(f"  Table minimum: ${high_stakes_game.betting_rules.get_table_minimum()}")
        print(f"  Table maximum: ${high_stakes_game.betting_rules.get_table_maximum():,}")
        print(f"  Straight up payout: {high_stakes_game.betting_rules.get_payout_ratio(BetType.STRAIGHT_UP)}:1")
        print(f"  Red minimum bet: ${high_stakes_game.betting_rules.get_minimum_bet(BetType.RED)}")
        print(f"  House edge: {high_stakes_game.betting_rules.get_house_edge(BetType.RED):.1f}%")
        print()
        
        # === BETTING WITH DIFFERENT CONFIGURATIONS ===
        print("=== BETTING WITH DIFFERENT CONFIGURATIONS ===")
        
        print("Standard American table bets:")
        try:
            american_bet = Bet.create_straight_up_bet(
                "17", amount=1000, betting_rules=american_game.betting_rules
            )
            print(f"  ✓ $1,000 straight up bet: Payout {american_bet.get_effective_payout_ratio()}:1")
        except ValueError as e:
            print(f"  ✗ $1,000 straight up bet: {e}")
        
        try:
            american_red_bet = Bet.create_color_bet(
                "red", amount=100, betting_rules=american_game.betting_rules
            )
            print(f"  ✓ $100 red bet: Payout {american_red_bet.get_effective_payout_ratio()}:1")
        except ValueError as e:
            print(f"  ✗ $100 red bet: {e}")
        
        print("\nEuropean table bets:")
        try:
            european_bet = Bet.create_straight_up_bet(
                "17", amount=1000, betting_rules=european_game.betting_rules
            )
            print(f"  ✓ $1,000 straight up bet: Payout {european_bet.get_effective_payout_ratio()}:1")
        except ValueError as e:
            print(f"  ✗ $1,000 straight up bet: {e}")
        
        try:
            european_red_bet = Bet.create_color_bet(
                "red", amount=50, betting_rules=european_game.betting_rules
            )
            print(f"  ✓ $50 red bet: Payout {european_red_bet.get_effective_payout_ratio()}:1")
        except ValueError as e:
            print(f"  ✗ $50 red bet: {e}")
        
        print("\nHigh stakes table bets:")
        try:
            high_stakes_bet = Bet.create_straight_up_bet(
                "17", amount=100000, betting_rules=high_stakes_game.betting_rules
            )
            print(f"  ✓ $100,000 straight up bet: Payout {high_stakes_bet.get_effective_payout_ratio()}:1")
        except ValueError as e:
            print(f"  ✗ $100,000 straight up bet: {e}")
        
        try:
            high_stakes_red_bet = Bet.create_color_bet(
                "red", amount=100000, betting_rules=high_stakes_game.betting_rules
            )
            print(f"  ✓ $100,000 red bet: Payout {high_stakes_red_bet.get_effective_payout_ratio()}:1")
        except ValueError as e:
            print(f"  ✗ $100,000 red bet: {e}")
        
        # Test minimum bet validation
        try:
            low_bet = Bet.create_color_bet(
                "red", amount=50, betting_rules=high_stakes_game.betting_rules
            )
            print(f"  ✓ $50 red bet on high stakes table: Accepted")
        except ValueError as e:
            print(f"  ✗ $50 red bet on high stakes table: {e}")
        
        print()
        
        # === CONFIGURATION DETAILS ===
        print("=== CONFIGURATION DETAILS ===")
        
        print("American configuration features:")
        american_info = american_game.betting_rules.get_table_info()
        print(f"  • House edge: {american_info.get('house_edge_default', 'N/A')}%")
        print(f"  • En prison rule: {american_game.betting_rules.game_rules.get('en_prison', False)}")
        print(f"  • La partage rule: {american_game.betting_rules.game_rules.get('la_partage', False)}")
        print(f"  • Call bets allowed: {american_game.betting_rules.special_rules.get('allow_call_bets', False)}")
        
        print("\nEuropean configuration features:")
        european_info = european_game.betting_rules.get_table_info()
        print(f"  • House edge: {european_info.get('house_edge_default', 'N/A')}%")
        print(f"  • En prison rule: {european_game.betting_rules.game_rules.get('en_prison', False)}")
        print(f"  • La partage rule: {european_game.betting_rules.game_rules.get('la_partage', False)}")
        print(f"  • Call bets allowed: {european_game.betting_rules.special_rules.get('allow_call_bets', False)}")
        
        print("\nHigh stakes configuration features:")
        high_stakes_info = high_stakes_game.betting_rules.get_table_info()
        print(f"  • House edge: {high_stakes_info.get('house_edge_default', 'N/A')}%")
        print(f"  • Surrender rule: {high_stakes_game.betting_rules.game_rules.get('surrender', False)}")
        print(f"  • Maximum parlay: {high_stakes_game.betting_rules.special_rules.get('maximum_parlay', 'N/A')}")
        print(f"  • Call bets allowed: {high_stakes_game.betting_rules.special_rules.get('allow_call_bets', False)}")
        
    finally:
        # Clean up
        os.unlink(high_stakes_config_path)
    
    print("\n🎰 Separate Configuration Demo Complete! 🎰")
    print("\nKey Features Demonstrated:")
    print("  ✓ Automatic config selection based on table type")
    print("  ✓ American vs European rule differences")
    print("  ✓ Custom configuration files with Game class")
    print("  ✓ Table-specific betting validation")
    print("  ✓ Game rules and special betting features")
    print("  ✓ Ratio-based maximum bet calculations")
    
    print("\nConfiguration Files:")
    print("  📁 config/american_rules.yaml - American table defaults")
    print("  📁 config/european_rules.yaml - European table defaults")
    print("  📁 Custom configs can be provided to Game constructor")


if __name__ == "__main__":
    main() 