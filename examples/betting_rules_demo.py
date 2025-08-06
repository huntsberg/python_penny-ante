#!/usr/bin/env python3
"""
Betting Rules Demo - Demonstrates the configurable betting rules system.

This script shows how to use YAML configuration files to customize betting rules,
including payout ratios, minimum/maximum bets, and table limits.
"""

from penny_ante import Game, Bet, BetType, BettingRules
import tempfile
import os


def create_custom_config():
    """Create a custom configuration file with different rules."""
    custom_config = """
# Custom Game Configuration - High Roller Table
payout_ratios:
  straight_up: 40        # Higher payout than standard 35:1
  split: 20             # Higher than standard 17:1
  street: 13            # Higher than standard 11:1
  corner: 10            # Higher than standard 8:1
  red: 1
  black: 1
  odd: 1
  even: 1
  high: 1
  low: 1
  first_dozen: 3        # Higher than standard 2:1
  second_dozen: 3
  third_dozen: 3

minimum_bet_ratios:
  global: 1.0           # Default ratio
  straight_up: 0.5      # Lower ratio for high-risk bets
  split: 0.5
  street: 1.0
  corner: 1.0
  red: 2.0              # Higher ratio for outside bets
  black: 2.0
  odd: 2.0
  even: 2.0
  high: 2.0
  low: 2.0
  first_dozen: 2.0
  second_dozen: 2.0
  third_dozen: 2.0
  first_column: 2.0
  second_column: 2.0
  third_column: 2.0

maximum_bet_ratios:
  global: 1.0           # 100% of table maximum
  straight_up: 0.3      # Only 30% for highest payout bets
  split: 0.5            # 50% for split bets
  street: 0.7           # 70% for street bets
  corner: 0.8           # 80% for corner bets
  six_line: 0.9         # 90% for six line bets
  red: 1.0              # Full amount for outside bets
  black: 1.0
  odd: 1.0
  even: 1.0
  high: 1.0
  low: 1.0
  first_dozen: 0.9      # 90% for dozen bets
  second_dozen: 0.9
  third_dozen: 0.9
  first_column: 0.9
  second_column: 0.9
  third_column: 0.9

table_limits:
  minimum_bet: 100
  maximum_bet: 5000000     # 5 million maximum
  maximum_total_bet: 50000000  # 50 million total per spin
"""
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
    temp_file.write(custom_config)
    temp_file.close()
    
    return temp_file.name


def main():
    """Demonstrate the configurable betting rules system."""
    print("🎰 Penny Ante Configurable Betting Rules Demo 🎰\n")
    
    # === STANDARD CONFIGURATION ===
    print("=== STANDARD GAME CONFIGURATION ===")
    
    # Load default configuration
    standard_rules = BettingRules(table_type="AMERICAN")
    
    print(f"Table type: {standard_rules.table_type}")
    print(f"Table minimum: ${standard_rules.get_table_minimum()}")
    print(f"Table maximum: ${standard_rules.get_table_maximum():,}")
    print()
    
    print("Standard Payout Ratios:")
    for bet_type in [BetType.STRAIGHT_UP, BetType.SPLIT, BetType.RED, BetType.FIRST_DOZEN]:
        payout = standard_rules.get_payout_ratio(bet_type)
        print(f"  {bet_type.value}: {payout}:1")
    print()
    
    print("Standard Maximum Bets (using ratios):")
    for bet_type in [BetType.STRAIGHT_UP, BetType.SPLIT, BetType.RED]:
        max_bet = standard_rules.get_maximum_bet(bet_type)
        ratio = standard_rules.get_maximum_bet_ratio(bet_type)
        print(f"  {bet_type.value}: ${max_bet:,} (ratio: {ratio})")
    print()
    
    # === CUSTOM HIGH ROLLER CONFIGURATION ===
    print("=== CUSTOM HIGH ROLLER CONFIGURATION ===")
    
    # Create and load custom configuration
    custom_config_path = create_custom_config()
    try:
        high_roller_rules = BettingRules(config_path=custom_config_path, table_type="AMERICAN")
        
        print(f"Table type: {high_roller_rules.table_type}")
        print(f"Table minimum: ${high_roller_rules.get_table_minimum()}")
        print(f"Table maximum: ${high_roller_rules.get_table_maximum():,}")
        print()
        
        print("High Roller Payout Ratios:")
        for bet_type in [BetType.STRAIGHT_UP, BetType.SPLIT, BetType.RED, BetType.FIRST_DOZEN]:
            payout = high_roller_rules.get_payout_ratio(bet_type)
            print(f"  {bet_type.value}: {payout}:1")
        print()
        
        print("High Roller Maximum Bets (using ratios):")
        for bet_type in [BetType.STRAIGHT_UP, BetType.SPLIT, BetType.RED]:
            max_bet = high_roller_rules.get_maximum_bet(bet_type)
            ratio = high_roller_rules.get_maximum_bet_ratio(bet_type)
            print(f"  {bet_type.value}: ${max_bet:,} (ratio: {ratio})")
        print()
        
        print("High Roller Minimum Bets:")
        for bet_type in [BetType.STRAIGHT_UP, BetType.RED]:
            min_bet = high_roller_rules.get_minimum_bet(bet_type)
            print(f"  {bet_type.value}: ${min_bet}")
        print()
        
        # === COMPARISON ===
        print("=== CONFIGURATION COMPARISON ===")
        print(f"{'Bet Type':<15} {'Standard Max':<15} {'High Roller Max':<18} {'Standard Payout':<16} {'High Roller Payout'}")
        print("-" * 80)
        
        for bet_type in [BetType.STRAIGHT_UP, BetType.SPLIT, BetType.RED, BetType.FIRST_DOZEN]:
            std_max = standard_rules.get_maximum_bet(bet_type)
            hr_max = high_roller_rules.get_maximum_bet(bet_type)
            std_payout = standard_rules.get_payout_ratio(bet_type)
            hr_payout = high_roller_rules.get_payout_ratio(bet_type)
            
            print(f"{bet_type.value:<15} ${std_max:<14,} ${hr_max:<17,} {std_payout}:1{'':<12} {hr_payout}:1")
        print()
        
        # === BETTING WITH RULES ===
        print("=== BETTING WITH CONFIGURABLE RULES ===")
        
        # Create bets using high roller rules
        print("Creating bets with high roller rules...")
        
        # High roller straight up bet
        straight_bet = Bet.create_straight_up_bet(
            "17", 
            amount=100000,  # $100K bet
            betting_rules=high_roller_rules
        )
        
        # High roller red bet
        red_bet = Bet.create_color_bet(
            "red", 
            amount=500000,  # $500K bet
            betting_rules=high_roller_rules
        )
        
        print(f"Straight up bet: {straight_bet}")
        print(f"  Effective payout ratio: {straight_bet.get_effective_payout_ratio()}:1")
        print(f"  House edge: {straight_bet.get_house_edge():.2f}%")
        print()
        
        print(f"Red bet: {red_bet}")
        print(f"  Effective payout ratio: {red_bet.get_effective_payout_ratio()}:1")
        print(f"  House edge: {red_bet.get_house_edge():.2f}%")
        print()
        
        # === BET VALIDATION ===
        print("=== BET VALIDATION EXAMPLES ===")
        
        print("Testing bet validation with high roller rules...")
        
        # Valid bets
        try:
            valid_bet = Bet.create_straight_up_bet(
                "17", 
                amount=50000,  # Within limits
                betting_rules=high_roller_rules
            )
            print(f"✓ Valid bet: ${valid_bet.amount:,} straight up bet")
        except ValueError as e:
            print(f"✗ Validation error: {e}")
        
        # Invalid bet - too low
        try:
            invalid_low_bet = Bet.create_color_bet(
                "red", 
                amount=50,  # Below minimum of 200
                betting_rules=high_roller_rules
            )
            print(f"✓ Low bet accepted: ${invalid_low_bet.amount}")
        except ValueError as e:
            print(f"✗ Low bet rejected: {e}")
        
        # Invalid bet - too high
        try:
            invalid_high_bet = Bet.create_straight_up_bet(
                "17", 
                amount=2000000,  # Above 30% limit (1.5M)
                betting_rules=high_roller_rules
            )
            print(f"✓ High bet accepted: ${invalid_high_bet.amount:,}")
        except ValueError as e:
            print(f"✗ High bet rejected: {e}")
        
        print()
        
        # === PAYOUT SIMULATION ===
        print("=== PAYOUT SIMULATION ===")
        
        # Simulate a winning straight up bet
        print("Simulating a winning $100K straight up bet on 17...")
        
        # Create a winning space
        from penny_ante.space import Space
        winning_space = Space("17")
        
        if straight_bet.is_winning_bet(winning_space):
            payout = straight_bet.calculate_payout(winning_space)
            profit = payout - straight_bet.amount
            print(f"🎉 Winner! Payout: ${payout:,} (Profit: ${profit:,})")
        else:
            print("😞 Not a winner")
        
        print()
        
        # === TABLE INFORMATION ===
        print("=== TABLE INFORMATION ===")
        
        table_info = high_roller_rules.get_table_info()
        print("High Roller Table Info:")
        for key, value in table_info.items():
            if key == 'payout_ratios':
                print(f"  {key}: {len(value)} bet types configured")
            elif isinstance(value, (int, float)) and value > 1000:
                print(f"  {key}: ${value:,}")
            else:
                print(f"  {key}: {value}")
        
    finally:
        # Clean up temporary file
        os.unlink(custom_config_path)
    
    print("\n🎰 Betting Rules Demo Complete! 🎰")
    print("\nKey Features Demonstrated:")
    print("  ✓ YAML-based configuration")
    print("  ✓ Ratio-based maximum bets")
    print("  ✓ Configurable payout ratios")
    print("  ✓ Flexible minimum/maximum limits")
    print("  ✓ Bet validation with custom rules")
    print("  ✓ House edge customization")
    print("  ✓ Table type specific configurations")


if __name__ == "__main__":
    main() 