#!/usr/bin/env python3
"""
Calculated House Edge Demo - Demonstrates automatic house edge calculation.

This script shows how house edge is now calculated mathematically based on
payout ratios and table type (American vs European), eliminating the need
for manual configuration and ensuring mathematical accuracy.
"""

from penny_ante import Game, Bet, BetType, BettingRules
import tempfile
import os


def create_custom_payout_config():
    """Create a configuration with custom payout ratios to show house edge calculation."""
    config = """
# Custom Payout Configuration - To demonstrate house edge calculation
payout_ratios:
  straight_up: 30        # Lower than standard 35:1
  split: 15             # Lower than standard 17:1 
  street: 10            # Lower than standard 11:1
  red: 1                # Standard 1:1
  black: 1
  first_dozen: 2        # Standard 2:1

minimum_bet_ratios:
  global: 1.0
  straight_up: 1.0
  red: 5.0

maximum_bet_ratios:
  global: 1.0
  straight_up: 0.5
  red: 1.0

table_limits:
  minimum_bet: 1
  maximum_bet: 100000
  maximum_total_bet: 1000000
"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
    temp_file.write(config)
    temp_file.close()
    return temp_file.name


def calculate_house_edge_manually(winning_outcomes: int, total_pockets: int, payout_ratio: int) -> float:
    """
    Manual calculation for verification.
    
    Formula: House Edge = (1 - (Win Probability × (Payout + 1))) × 100
    """
    win_probability = winning_outcomes / total_pockets
    house_edge = (1 - (win_probability * (payout_ratio + 1))) * 100
    return round(house_edge, 2)


def main():
    """Demonstrate the calculated house edge system."""
    print("🎰 Penny Ante Calculated House Edge Demo 🎰\n")
    
    # === STANDARD CONFIGURATIONS ===
    print("=== STANDARD HOUSE EDGE CALCULATIONS ===")
    
    # American table
    print("🇺🇸 AMERICAN TABLE (38 pockets)")
    american_game = Game(table_type="AMERICAN")
    american_rules = american_game.betting_rules
    
    print("  Calculated House Edges:")
    bet_types = [BetType.STRAIGHT_UP, BetType.SPLIT, BetType.RED, BetType.FIRST_DOZEN]
    
    for bet_type in bet_types:
        payout = american_rules.get_payout_ratio(bet_type)
        house_edge = american_rules.get_house_edge(bet_type)
        print(f"    {bet_type.value:<12}: {payout}:1 payout → {house_edge:.2f}% house edge")
    print()
    
    # European table
    print("🇪🇺 EUROPEAN TABLE (37 pockets)")
    european_game = Game(table_type="EUROPEAN")
    european_rules = european_game.betting_rules
    
    print("  Calculated House Edges:")
    for bet_type in bet_types:
        payout = european_rules.get_payout_ratio(bet_type)
        house_edge = european_rules.get_house_edge(bet_type)
        print(f"    {bet_type.value:<12}: {payout}:1 payout → {house_edge:.2f}% house edge")
    print()
    
    # === MANUAL VERIFICATION ===
    print("=== MANUAL CALCULATION VERIFICATION ===")
    
    print("Straight Up Bet Verification:")
    # Straight up: 1 winning outcome, payout 35:1
    american_manual = calculate_house_edge_manually(1, 38, 35)
    european_manual = calculate_house_edge_manually(1, 37, 35)
    american_calculated = american_rules.get_house_edge(BetType.STRAIGHT_UP)
    european_calculated = european_rules.get_house_edge(BetType.STRAIGHT_UP)
    
    print(f"  American: Manual {american_manual:.2f}% vs Calculated {american_calculated:.2f}%")
    print(f"  European: Manual {european_manual:.2f}% vs Calculated {european_calculated:.2f}%")
    print()
    
    print("Red Bet Verification:")
    # Red: 18 winning outcomes, payout 1:1
    american_manual = calculate_house_edge_manually(18, 38, 1)
    european_manual = calculate_house_edge_manually(18, 37, 1)
    american_calculated = american_rules.get_house_edge(BetType.RED)
    european_calculated = european_rules.get_house_edge(BetType.RED)
    
    print(f"  American: Manual {american_manual:.2f}% vs Calculated {american_calculated:.2f}%")
    print(f"  European: Manual {european_manual:.2f}% vs Calculated {european_calculated:.2f}%")
    print()
    
    # === MATHEMATICAL FORMULA EXPLANATION ===
    print("=== MATHEMATICAL FORMULA ===")
    print("House Edge = (1 - (Win Probability × (Payout + 1))) × 100")
    print()
    print("Example: American Straight Up")
    print("  • Winning outcomes: 1 (single number)")
    print("  • Total pockets: 38 (0, 00, 1-36)")
    print("  • Win probability: 1/38 = 0.02632")
    print("  • Payout: 35:1")
    print("  • Calculation: (1 - (1/38 × (35 + 1))) × 100")
    print("  • Calculation: (1 - (1/38 × 36)) × 100")
    print("  • Calculation: (1 - 36/38) × 100")
    print("  • Calculation: (2/38) × 100 = 5.26%")
    print()
    
    # === CUSTOM PAYOUT RATIOS ===
    print("=== CUSTOM PAYOUT RATIOS DEMONSTRATION ===")
    
    custom_config_path = create_custom_payout_config()
    try:
        print("💰 CUSTOM PAYOUT TABLE")
        custom_game = Game(
            table_type="AMERICAN", 
            betting_rules_config=custom_config_path
        )
        custom_rules = custom_game.betting_rules
        
        print("  Standard vs Custom Payouts and House Edges:")
        print(f"{'Bet Type':<12} {'Std Payout':<10} {'Std Edge':<8} {'Custom Payout':<13} {'Custom Edge':<11} {'Difference'}")
        print("-" * 75)
        
        for bet_type in [BetType.STRAIGHT_UP, BetType.SPLIT, BetType.RED]:
            std_payout = american_rules.get_payout_ratio(bet_type)
            std_edge = american_rules.get_house_edge(bet_type)
            custom_payout = custom_rules.get_payout_ratio(bet_type)
            custom_edge = custom_rules.get_house_edge(bet_type)
            edge_diff = custom_edge - std_edge
            
            print(f"{bet_type.value:<12} {std_payout}:1{'':<6} {std_edge:.2f}%{'':<3} {custom_payout}:1{'':<9} {custom_edge:.2f}%{'':<6} {edge_diff:+.2f}%")
        print()
        
        print("Impact of Lower Payouts:")
        print("  • Lower payouts = Higher house edge")
        print("  • Straight up: 35:1 → 30:1 increases edge by ~10.5%")
        print("  • Split: 17:1 → 15:1 increases edge by ~5.3%")
        print("  • Outside bets unchanged: Same house edge")
        print()
        
    finally:
        # Clean up
        os.unlink(custom_config_path)
    
    # === HOUSE EDGE BY BET TYPE ===
    print("=== HOUSE EDGE BY BET TYPE ===")
    
    print("American Table House Edges:")
    all_bet_types = [
        BetType.STRAIGHT_UP, BetType.SPLIT, BetType.STREET, BetType.CORNER,
        BetType.RED, BetType.FIRST_DOZEN, BetType.FIRST_COLUMN
    ]
    
    for bet_type in all_bet_types:
        try:
            payout = american_rules.get_payout_ratio(bet_type)
            house_edge = american_rules.get_house_edge(bet_type)
            print(f"  {bet_type.value:<12}: {house_edge:.2f}% (payout {payout}:1)")
        except ValueError:
            print(f"  {bet_type.value:<12}: Not configured")
    print()
    
    # === ADVANTAGES OF CALCULATED HOUSE EDGE ===
    print("=== ADVANTAGES OF CALCULATED HOUSE EDGE ===")
    
    print("1. Mathematical Accuracy:")
    print("   • Always correct based on actual payout ratios")
    print("   • No possibility of configuration errors")
    print("   • Automatic updates when payouts change")
    print()
    
    print("2. Simplified Configuration:")
    print("   • No need to manually specify house edge values")
    print("   • Fewer configuration sections to maintain")
    print("   • Reduced chance of inconsistencies")
    print()
    
    print("3. Transparency:")
    print("   • Clear relationship between payouts and house edge")
    print("   • Easy to verify calculations")
    print("   • Educational value for understanding the math")
    print()
    
    print("4. Flexibility:")
    print("   • Custom payout ratios automatically get correct house edge")
    print("   • Easy to test different payout scenarios")
    print("   • Supports any mathematically valid payout structure")
    print()
    
    # === COMPARISON WITH REAL GAME VALUES ===
    print("=== COMPARISON WITH REAL GAME VALUES ===")
    print()
    print("Standard Game House Edges (calculated):")
    real_edges = [
        ("Straight Up", american_rules.get_house_edge(BetType.STRAIGHT_UP), "5.26%"),
        ("Split", american_rules.get_house_edge(BetType.SPLIT), "5.26%"),
        ("Red/Black", american_rules.get_house_edge(BetType.RED), "5.26%"),
        ("Dozen", american_rules.get_house_edge(BetType.FIRST_DOZEN), "5.26%"),
    ]
    
    print(f"{'Bet Type':<12} {'Calculated':<11} {'Real Game':<12} {'Match'}")
    print("-" * 45)
    for bet_name, calculated, real in real_edges:
        match = "✓" if abs(calculated - float(real.strip('%'))) < 0.01 else "✗"
        print(f"{bet_name:<12} {calculated:.2f}%{'':<6} {real:<12} {match}")
    print()
    
    print("European vs American Difference:")
    european_straight = european_rules.get_house_edge(BetType.STRAIGHT_UP)
    american_straight = american_rules.get_house_edge(BetType.STRAIGHT_UP)
    difference = american_straight - european_straight
    print(f"  • American: {american_straight:.2f}%")
    print(f"  • European: {european_straight:.2f}%")
    print(f"  • Difference: {difference:.2f}% (due to extra 00 pocket)")
    
    print("\n🎰 Calculated House Edge Demo Complete! 🎰")
    print("\nKey Features Demonstrated:")
    print("  ✓ Automatic house edge calculation from payout ratios")
    print("  ✓ Mathematical accuracy and verification")
    print("  ✓ American vs European differences")
    print("  ✓ Custom payout ratio impact")
    print("  ✓ Simplified configuration (no manual house edge)")
    print("  ✓ Real game value verification")


if __name__ == "__main__":
    main() 