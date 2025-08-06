#!/usr/bin/env python3
"""
Ratio-Based Minimum Bets Demo - Demonstrates the flexible minimum bet system.

This script shows how minimum bet amounts are expressed as ratios of the table
minimum, making the system scalable and flexible for different table limits.
"""

from penny_ante import Game, Bet, BetType, BettingRules
import tempfile
import os


def create_high_minimum_config():
    """Create a configuration with high table minimum to show scaling."""
    config = """
# High Minimum Table Configuration
payout_ratios:
  straight_up: 35
  split: 17
  red: 1
  black: 1
  first_dozen: 2

minimum_bet_ratios:
  global: 1.0           # 100% of table minimum
  straight_up: 0.5      # 50% of table minimum (lower for high-risk)
  split: 0.75           # 75% of table minimum
  red: 2.0              # 200% of table minimum
  black: 2.0
  first_dozen: 3.0      # 300% of table minimum

maximum_bet_ratios:
  global: 1.0
  straight_up: 0.5
  red: 1.0

house_edge:
  straight_up: 5.26
  red: 5.26

table_limits:
  minimum_bet: 50       # High table minimum
  maximum_bet: 500000
  maximum_total_bet: 5000000
"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
    temp_file.write(config)
    temp_file.close()
    return temp_file.name


def main():
    """Demonstrate the ratio-based minimum bet system."""
    print("🎰 Penny Ante Ratio-Based Minimum Bets Demo 🎰\n")
    
    # === STANDARD CONFIGURATIONS ===
    print("=== STANDARD CONFIGURATIONS ===")
    
    # American table
    print("🇺🇸 AMERICAN TABLE")
    american_game = Game(table_type="AMERICAN")
    american_rules = american_game.betting_rules
    
    print(f"  Table minimum: ${american_rules.get_table_minimum()}")
    print("  Minimum bet calculations:")
    
    bet_types = [BetType.STRAIGHT_UP, BetType.SPLIT, BetType.RED, BetType.FIRST_DOZEN]
    for bet_type in bet_types:
        min_bet = american_rules.get_minimum_bet(bet_type)
        ratio = american_rules.get_minimum_bet_ratio(bet_type)
        print(f"    {bet_type.value:<12}: ${min_bet:<3} (ratio: {ratio})")
    print()
    
    # European table
    print("🇪🇺 EUROPEAN TABLE")
    european_game = Game(table_type="EUROPEAN")
    european_rules = european_game.betting_rules
    
    print(f"  Table minimum: ${european_rules.get_table_minimum()}")
    print("  Minimum bet calculations:")
    
    for bet_type in bet_types:
        min_bet = european_rules.get_minimum_bet(bet_type)
        ratio = european_rules.get_minimum_bet_ratio(bet_type)
        print(f"    {bet_type.value:<12}: ${min_bet:<3} (ratio: {ratio})")
    print()
    
    # === RATIO COMPARISON ===
    print("=== AMERICAN vs EUROPEAN MINIMUM BET RATIOS ===")
    print(f"{'Bet Type':<15} {'American Ratio':<15} {'European Ratio':<15} {'Difference'}")
    print("-" * 65)
    
    for bet_type in bet_types:
        american_ratio = american_rules.get_minimum_bet_ratio(bet_type)
        european_ratio = european_rules.get_minimum_bet_ratio(bet_type)
        diff = european_ratio - american_ratio
        print(f"{bet_type.value:<15} {american_ratio:<15} {european_ratio:<15} {diff:+.1f}")
    print()
    
    # === SCALING DEMONSTRATION ===
    print("=== SCALING DEMONSTRATION ===")
    print("How minimum bets scale with different table minimums:\n")
    
    table_minimums = [1, 5, 10, 25, 50]
    print(f"{'Table Min':<10} {'Straight Up':<12} {'Red':<8} {'Dozen':<8}")
    print("-" * 40)
    
    # American scaling
    print("American:")
    for table_min in table_minimums:
        straight_up = int(table_min * american_rules.get_minimum_bet_ratio(BetType.STRAIGHT_UP))
        red = int(table_min * american_rules.get_minimum_bet_ratio(BetType.RED))
        dozen = int(table_min * american_rules.get_minimum_bet_ratio(BetType.FIRST_DOZEN))
        print(f"${table_min:<9} ${straight_up:<11} ${red:<7} ${dozen:<7}")
    
    print("\nEuropean:")
    for table_min in table_minimums:
        straight_up = int(table_min * european_rules.get_minimum_bet_ratio(BetType.STRAIGHT_UP))
        red = int(table_min * european_rules.get_minimum_bet_ratio(BetType.RED))
        dozen = int(table_min * european_rules.get_minimum_bet_ratio(BetType.FIRST_DOZEN))
        print(f"${table_min:<9} ${straight_up:<11} ${red:<7} ${dozen:<7}")
    print()
    
    # === CUSTOM HIGH MINIMUM TABLE ===
    print("=== CUSTOM HIGH MINIMUM TABLE ===")
    
    high_min_config_path = create_high_minimum_config()
    try:
        print("💰 HIGH MINIMUM TABLE (custom config)")
        high_min_game = Game(
            table_type="AMERICAN", 
            betting_rules_config=high_min_config_path
        )
        high_min_rules = high_min_game.betting_rules
        
        print(f"  Table minimum: ${high_min_rules.get_table_minimum()}")
        print("  Minimum bet calculations:")
        
        for bet_type in bet_types:
            min_bet = high_min_rules.get_minimum_bet(bet_type)
            ratio = high_min_rules.get_minimum_bet_ratio(bet_type)
            print(f"    {bet_type.value:<12}: ${min_bet:<3} (ratio: {ratio})")
        print()
        
        # === BETTING VALIDATION ===
        print("=== BETTING VALIDATION EXAMPLES ===")
        
        print("Standard American table ($1 minimum):")
        test_amounts = [1, 5, 10]
        for amount in test_amounts:
            try:
                bet = Bet.create_color_bet("red", amount, betting_rules=american_rules)
                print(f"  ✓ ${amount} red bet: Accepted (min: ${american_rules.get_minimum_bet(BetType.RED)})")
            except ValueError as e:
                print(f"  ✗ ${amount} red bet: {e}")
        
        print("\nEuropean table ($2 minimum):")
        for amount in test_amounts:
            try:
                bet = Bet.create_color_bet("red", amount, betting_rules=european_rules)
                print(f"  ✓ ${amount} red bet: Accepted (min: ${european_rules.get_minimum_bet(BetType.RED)})")
            except ValueError as e:
                print(f"  ✗ ${amount} red bet: {e}")
        
        print("\nHigh minimum table ($50 minimum):")
        test_amounts_high = [25, 50, 100]
        for amount in test_amounts_high:
            try:
                bet = Bet.create_color_bet("red", amount, betting_rules=high_min_rules)
                print(f"  ✓ ${amount} red bet: Accepted (min: ${high_min_rules.get_minimum_bet(BetType.RED)})")
            except ValueError as e:
                print(f"  ✗ ${amount} red bet: {e}")
        print()
        
        # === RATIO BENEFITS ===
        print("=== BENEFITS OF RATIO-BASED MINIMUMS ===")
        
        print("1. Automatic Scaling:")
        print("   • Change table minimum → all bet minimums scale proportionally")
        print("   • No need to manually update each bet type")
        print("   • Maintains relative betting structure")
        print()
        
        print("2. Flexible Configuration:")
        print("   • Inside bets can have lower ratios (less risk for house)")
        print("   • Outside bets can have higher ratios (encourage larger bets)")
        print("   • Easy to adjust relative minimum relationships")
        print()
        
        print("3. Consistency Across Tables:")
        print("   • Same ratio structure across different table limits")
        print("   • Predictable scaling for players")
        print("   • Easier to maintain multiple table configurations")
        print()
        
        # === RATIO EXAMPLES ===
        print("=== COMMON RATIO PATTERNS ===")
        
        print("Conservative (favors house):")
        print("  • Inside bets: 1.0x table minimum (same as table)")
        print("  • Outside bets: 5.0x table minimum (higher barriers)")
        print()
        
        print("Aggressive (encourages betting):")
        print("  • Inside bets: 0.5x table minimum (lower barriers)")
        print("  • Outside bets: 2.0x table minimum (moderate barriers)")
        print()
        
        print("Balanced (current European setup):")
        print("  • Straight up: 0.5x (encourage high-risk bets)")
        print("  • Outside bets: 5.0x (maintain profitability)")
        print()
        
    finally:
        # Clean up
        os.unlink(high_min_config_path)
    
    print("🎰 Ratio-Based Minimum Bets Demo Complete! 🎰")
    print("\nKey Features Demonstrated:")
    print("  ✓ Ratio-based minimum bet calculations")
    print("  ✓ Automatic scaling with table minimums")
    print("  ✓ American vs European ratio differences")
    print("  ✓ Custom ratio configurations")
    print("  ✓ Betting validation with ratio-based minimums")
    print("  ✓ Flexible risk management through ratios")


if __name__ == "__main__":
    main() 