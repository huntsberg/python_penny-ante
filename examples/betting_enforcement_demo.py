#!/usr/bin/env python3
"""
Betting Enforcement Demonstration

This script demonstrates the comprehensive betting limits and rules enforcement
system in the penny-ante roulette library.
"""

import sys
import os

# Add the src directory to the path so we can import penny_ante
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from penny_ante import Game, Bet, BetType


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")


def print_subsection(title: str) -> None:
    """Print a subsection header."""
    print(f"\n{'-'*40}")
    print(f"{title}")
    print(f"{'-'*40}")


def demonstrate_individual_bet_limits():
    """Demonstrate individual bet amount limits."""
    print_section("INDIVIDUAL BET LIMITS ENFORCEMENT")
    
    # Create a game with American rules
    game = Game(table_type="AMERICAN")
    
    # Show table limits
    info = game.betting_rules.get_table_info()
    print(f"Table Type: {info['table_type']}")
    print(f"Table Minimum: ${info['minimum_bet']:,}")
    print(f"Table Maximum: ${info['maximum_bet']:,}")
    print(f"Maximum Total Bets: ${info['maximum_total_bet']:,}")
    
    print_subsection("Valid Bets")
    
    try:
        # Valid straight up bet
        valid_bet = Bet.create_straight_up_bet("17", amount=1000, 
                                             layout=game.table.layout,
                                             betting_rules=game.betting_rules)
        print(f"✓ Valid straight up bet: ${valid_bet.amount:,} on number {list(valid_bet.spaces)[0]}")
        
        # Valid color bet
        valid_color_bet = Bet.create_color_bet("red", amount=5000,
                                             layout=game.table.layout,
                                             betting_rules=game.betting_rules)
        print(f"✓ Valid red bet: ${valid_color_bet.amount:,}")
        
    except ValueError as e:
        print(f"✗ Unexpected error: {e}")
    
    print_subsection("Invalid Bets - Amount Too Low")
    
    try:
        # Bet below minimum (table minimum is 1)
        invalid_low_bet = Bet.create_straight_up_bet("17", amount=0,
                                                   layout=game.table.layout,
                                                   betting_rules=game.betting_rules)
        print(f"✗ This should have failed: ${invalid_low_bet.amount}")
    except ValueError as e:
        print(f"✓ Correctly rejected low bet: {e}")
    
    print_subsection("Invalid Bets - Amount Too High")
    
    try:
        # Bet above maximum for straight up (50% of table max = $500,000)
        max_straight_up = game.betting_rules.get_maximum_bet(BetType.STRAIGHT_UP)
        invalid_high_bet = Bet.create_straight_up_bet("17", amount=max_straight_up + 1,
                                                    layout=game.table.layout,
                                                    betting_rules=game.betting_rules)
        print(f"✗ This should have failed: ${invalid_high_bet.amount:,}")
    except ValueError as e:
        print(f"✓ Correctly rejected high bet: {e}")


def demonstrate_total_bet_limits():
    """Demonstrate total bet limits across all players."""
    print_section("TOTAL BET LIMITS ENFORCEMENT")
    
    # Create a game with lower total limits for demonstration
    game = Game(table_type="AMERICAN")
    
    # Add players with chips
    game.add_player("Alice")
    game.add_player("Bob")
    
    alice = game.players["Alice"]
    alice.buy_chips(count=5000000, value=1)  # $5M in chips
    
    bob = game.players["Bob"]
    bob.buy_chips(count=5000000, value=1)  # $5M in chips
    
    print(f"Alice has ${alice.get_total_value():,} in chips")
    print(f"Bob has ${bob.get_total_value():,} in chips")
    print(f"Maximum total bets allowed: ${game.betting_rules.get_maximum_total_bet():,}")
    
    print_subsection("Placing Valid Bets")
    
    # Place several large bets (within individual limits)
    bet1 = Bet.create_color_bet("red", amount=800000,  # Within red bet limit
                              layout=game.table.layout,
                              betting_rules=game.betting_rules)
    game.place_bet(bet1, "Alice")
    print(f"✓ Alice placed red bet: ${bet1.amount:,}")
    
    bet2 = Bet.create_color_bet("black", amount=900000,  # Within black bet limit
                              layout=game.table.layout,
                              betting_rules=game.betting_rules)
    game.place_bet(bet2, "Bob")
    print(f"✓ Bob placed black bet: ${bet2.amount:,}")
    
    # Add more bets to approach the total limit
    bet3 = Bet.create_straight_up_bet("17", amount=400000,  # Within straight up limit
                                    layout=game.table.layout,
                                    betting_rules=game.betting_rules)
    game.place_bet(bet3, "Alice")
    print(f"✓ Alice placed straight up bet: ${bet3.amount:,}")
    
    # Show current total
    current_total = game.get_total_bet_amount()
    print(f"Current total bets: ${current_total:,}")
    
    print_subsection("Attempting to Exceed Total Limit")
    
    # Add more bets to approach the total limit systematically
    bet_amounts = [800000, 800000, 800000, 800000, 800000, 800000, 800000, 800000, 800000]  # 7.2M more
    
    for i, amount in enumerate(bet_amounts):
        try:
            bet = Bet.create_color_bet("red" if i % 2 == 0 else "black", amount=amount,
                                     layout=game.table.layout,
                                     betting_rules=game.betting_rules)
            game.place_bet(bet, "Alice" if i % 2 == 0 else "Bob")
            current_total = game.get_total_bet_amount()
            print(f"✓ Placed bet #{i+4}: ${amount:,} (Total: ${current_total:,})")
            
            # Stop when we get close to the limit
            if current_total >= 9500000:  # Stop at 9.5M to try one more
                break
                
        except ValueError as e:
            if "exceed maximum total bet limit" in str(e):
                print(f"✓ Correctly rejected bet that would exceed total limit: {e}")
                break
            else:
                print(f"✓ Bet rejected for individual limit: {e}")
                break


def demonstrate_player_chip_validation():
    """Demonstrate player chip balance validation."""
    print_section("PLAYER CHIP BALANCE VALIDATION")
    
    game = Game(table_type="AMERICAN")
    game.add_player("Charlie")
    
    charlie = game.players["Charlie"]
    charlie.buy_chips(count=1000, value=1)  # Only $1000 in chips
    
    print(f"Charlie has ${charlie.get_total_value():,} in chips")
    
    print_subsection("Valid Bet Within Balance")
    
    try:
        valid_bet = Bet.create_color_bet("red", amount=500,
                                       layout=game.table.layout,
                                       betting_rules=game.betting_rules)
        game.place_bet(valid_bet, "Charlie")
        print(f"✓ Charlie placed bet: ${valid_bet.amount:,}")
        print(f"Charlie's remaining balance: ${charlie.get_chip_balance():,} chips")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    print_subsection("Invalid Bet Exceeding Balance")
    
    try:
        # Try to bet more than Charlie has
        invalid_bet = Bet.create_color_bet("black", amount=600,  # Charlie only has 500 left
                                         layout=game.table.layout,
                                         betting_rules=game.betting_rules)
        game.place_bet(invalid_bet, "Charlie")
        print(f"✗ This should have failed: ${invalid_bet.amount:,}")
    except Exception as e:
        print(f"✓ Correctly rejected bet exceeding balance: {e}")


def demonstrate_betting_phases():
    """Demonstrate betting phase management."""
    print_section("BETTING PHASE MANAGEMENT")
    
    game = Game(table_type="AMERICAN")
    game.add_player("Diana")
    
    diana = game.players["Diana"]
    diana.buy_chips(count=5000, value=1)
    
    print(f"Initial betting status: {'OPEN' if game.betting_open else 'CLOSED'}")
    
    print_subsection("Placing Bets During Open Phase")
    
    bet1 = Bet.create_straight_up_bet("17", amount=100,
                                    layout=game.table.layout,
                                    betting_rules=game.betting_rules)
    game.place_bet(bet1, "Diana")
    print(f"✓ Placed bet during open phase: ${bet1.amount:,}")
    
    bet2 = Bet.create_color_bet("red", amount=200,
                              layout=game.table.layout,
                              betting_rules=game.betting_rules)
    game.place_bet(bet2, "Diana")
    print(f"✓ Placed another bet: ${bet2.amount:,}")
    
    # Show bet summary
    summary = game.get_bet_summary()
    print(f"Total active bets: {summary['total_bets']}")
    print(f"Total amount: ${summary['total_amount']:,}")
    
    print_subsection("Closing Betting Phase")
    
    validation_result = game.close_betting()
    print(f"Betting closed. Valid: {validation_result['valid']}")
    print(f"Betting status: {'OPEN' if game.betting_open else 'CLOSED'}")
    
    print_subsection("Attempting to Bet During Closed Phase")
    
    try:
        bet3 = Bet.create_color_bet("black", amount=150,
                                  layout=game.table.layout,
                                  betting_rules=game.betting_rules)
        game.place_bet(bet3, "Diana")
        print(f"✗ This should have failed: ${bet3.amount:,}")
    except ValueError as e:
        print(f"✓ Correctly rejected bet during closed phase: {e}")
    
    print_subsection("Spinning Wheel and Opening New Round")
    
    # Spin the wheel (this automatically validates and closes betting if needed)
    game.spin_wheel()
    winning_space = game.current_space
    print(f"Wheel spun! Ball landed on: {winning_space.value} ({winning_space.color})")
    
    # Open betting for new round
    game.open_betting()
    print(f"New round started. Betting status: {'OPEN' if game.betting_open else 'CLOSED'}")
    print(f"Active bets cleared: {len(game.active_bets)} bets remaining")


def demonstrate_special_rules():
    """Demonstrate special rules enforcement."""
    print_section("SPECIAL RULES ENFORCEMENT")
    
    game = Game(table_type="AMERICAN")
    
    # Show special rules
    print("Special Rules Configuration:")
    info = game.betting_rules.get_table_info()
    for rule, value in info['special_rules'].items():
        print(f"  {rule}: {value}")
    
    print("\nGame Rules Configuration:")
    for rule, value in info['game_rules'].items():
        print(f"  {rule}: {value}")
    
    print_subsection("Rule Queries")
    
    print(f"Call bets allowed: {game.betting_rules.is_special_rule_enabled('allow_call_bets')}")
    print(f"Neighbor bets allowed: {game.betting_rules.is_special_rule_enabled('allow_neighbor_bets')}")
    print(f"Progressive betting allowed: {game.betting_rules.is_special_rule_enabled('progressive_betting')}")
    print(f"Maximum parlay: {game.betting_rules.get_game_rule('maximum_parlay')}")
    print(f"En prison rule: {game.betting_rules.get_game_rule('en_prison')}")


def demonstrate_comprehensive_validation():
    """Demonstrate comprehensive bet validation."""
    print_section("COMPREHENSIVE BET VALIDATION")
    
    game = Game(table_type="AMERICAN")
    
    # Create a mix of bets
    bets = [
        Bet.create_straight_up_bet("17", amount=1000, layout=game.table.layout,
                                 betting_rules=game.betting_rules),
        Bet.create_color_bet("red", amount=5000, layout=game.table.layout,
                           betting_rules=game.betting_rules),
        Bet.create_dozen_bet(1, amount=2000, layout=game.table.layout,
                           betting_rules=game.betting_rules),
        Bet.create_column_bet(2, amount=1500, layout=game.table.layout,
                            betting_rules=game.betting_rules)
    ]
    
    print("Validating multiple bets together...")
    validation_result = game.betting_rules.validate_multiple_bets(bets)
    
    print(f"Validation result: {'VALID' if validation_result['valid'] else 'INVALID'}")
    print(f"Total bets: {validation_result['bet_count']}")
    print(f"Total amount: ${validation_result['total_amount']:,}")
    
    print("\nBet type breakdown:")
    for bet_type, stats in validation_result['bet_type_counts'].items():
        print(f"  {bet_type}: {stats} bets")
    
    if validation_result['errors']:
        print("\nErrors:")
        for error in validation_result['errors']:
            print(f"  ✗ {error}")
    
    if validation_result['warnings']:
        print("\nWarnings:")
        for warning in validation_result['warnings']:
            print(f"  ⚠ {warning}")


def main():
    """Run all demonstrations."""
    print("PENNY ANTE ROULETTE - BETTING ENFORCEMENT DEMONSTRATION")
    print("=" * 60)
    print("This demo shows how betting limits and rules are enforced")
    
    try:
        demonstrate_individual_bet_limits()
        demonstrate_total_bet_limits()
        demonstrate_player_chip_validation()
        demonstrate_betting_phases()
        demonstrate_special_rules()
        demonstrate_comprehensive_validation()
        
        print_section("DEMONSTRATION COMPLETE")
        print("All betting enforcement features have been demonstrated!")
        print("The system successfully enforces:")
        print("  ✓ Individual bet amount limits (min/max per bet type)")
        print("  ✓ Total bet limits across all players")
        print("  ✓ Player chip balance validation")
        print("  ✓ Betting phase management (open/closed)")
        print("  ✓ Special rules and game rules")
        print("  ✓ Comprehensive multi-bet validation")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
