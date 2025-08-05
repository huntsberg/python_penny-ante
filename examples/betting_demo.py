#!/usr/bin/env python3
"""
Betting Demo - Demonstrates the penny_ante betting system.

This script shows how to create and use various types of roulette bets,
including inside bets (straight up, split, etc.) and outside bets 
(red/black, dozens, columns, etc.).
"""

from penny_ante import Game, Bet, BetType, Chips


def main():
    """Demonstrate the betting system with various bet types."""
    print("🎲 Penny Ante Betting System Demo 🎲\n")

    # Create a new American roulette game
    print("Creating an American roulette table...")
    game = Game(table_type="AMERICAN")
    layout = game.table.layout

    # Add a player with chips
    game.add_player("Alice")
    alice = game.players["Alice"]
    alice.buy_chips(count=100, value=5)  # $500 in $5 chips
    print(f"Alice starts with {alice.chips.count} chips worth ${alice.chips.cash_value()}\n")  # type: ignore

    # Demonstrate inside bets
    print("=== INSIDE BETS ===")

    # 1. Straight up bet (single number)
    print("1. Straight Up Bet (Single Number)")
    straight_bet = Bet.create_straight_up_bet("17", amount=5, chips=alice.chips, layout=layout)
    print(f"   Bet: {straight_bet}")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.STRAIGHT_UP]}:1")
    print()

    # 2. Split bet (two adjacent numbers)
    print("2. Split Bet (Two Adjacent Numbers)")
    split_bet = Bet.create_split_bet("17", "18", amount=10, chips=alice.chips, layout=layout)
    print(f"   Bet: {split_bet}")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.SPLIT]}:1")
    print()

    # 3. Manual inside bets (street, corner, six line)
    print("3. Street Bet (Three Numbers in a Row)")
    street_bet = Bet(BetType.STREET, ["13", "14", "15"], amount=15, chips=alice.chips, layout=layout)
    print(f"   Bet: {street_bet}")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.STREET]}:1")
    print()

    print("4. Corner Bet (Four Numbers in a Square)")
    corner_bet = Bet(BetType.CORNER, ["13", "14", "16", "17"], amount=20, chips=alice.chips, layout=layout)
    print(f"   Bet: {corner_bet}")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.CORNER]}:1")
    print()

    print("5. Six Line Bet (Two Adjacent Rows)")
    six_line_bet = Bet(BetType.SIX_LINE, ["13", "14", "15", "16", "17", "18"], amount=25, chips=alice.chips, layout=layout)
    print(f"   Bet: {six_line_bet}")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.SIX_LINE]}:1")
    print()

    # Demonstrate outside bets
    print("=== OUTSIDE BETS ===")

    # 1. Color bets
    print("1. Color Bets")
    red_bet = Bet.create_color_bet("red", amount=30, chips=alice.chips, layout=layout)
    black_bet = Bet.create_color_bet("black", amount=30, chips=alice.chips, layout=layout)
    print(f"   Red bet: covers {len(red_bet.spaces)} numbers")
    print(f"   Black bet: covers {len(black_bet.spaces)} numbers")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.RED]}:1")
    print()

    # 2. Odd/Even bets
    print("2. Odd/Even Bets")
    odd_bet = Bet(BetType.ODD, set(), amount=25, chips=alice.chips, layout=layout)
    even_bet = Bet(BetType.EVEN, set(), amount=25, chips=alice.chips, layout=layout)
    print(f"   Odd bet: covers 18 numbers (1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35)")
    print(f"   Even bet: covers 18 numbers (2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36)")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.ODD]}:1")
    print()

    # 3. High/Low bets
    print("3. High/Low Bets")
    high_bet = Bet(BetType.HIGH, set(), amount=35, chips=alice.chips, layout=layout)
    low_bet = Bet(BetType.LOW, set(), amount=35, chips=alice.chips, layout=layout)
    print(f"   High bet: covers numbers 19-36")
    print(f"   Low bet: covers numbers 1-18")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.HIGH]}:1")
    print()

    # 4. Dozen bets
    print("4. Dozen Bets")
    dozen1_bet = Bet.create_dozen_bet(1, amount=40, chips=alice.chips, layout=layout)
    dozen2_bet = Bet.create_dozen_bet(2, amount=40, chips=alice.chips, layout=layout)
    dozen3_bet = Bet.create_dozen_bet(3, amount=40, chips=alice.chips, layout=layout)
    print(f"   First dozen: covers {len(dozen1_bet.spaces)} numbers (1-12)")
    print(f"   Second dozen: covers {len(dozen2_bet.spaces)} numbers (13-24)")
    print(f"   Third dozen: covers {len(dozen3_bet.spaces)} numbers (25-36)")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.FIRST_DOZEN]}:1")
    print()

    # 5. Column bets
    print("5. Column Bets")
    col1_bet = Bet.create_column_bet(1, amount=45, chips=alice.chips, layout=layout)
    col2_bet = Bet.create_column_bet(2, amount=45, chips=alice.chips, layout=layout)
    col3_bet = Bet.create_column_bet(3, amount=45, chips=alice.chips, layout=layout)
    print(f"   First column: covers {len(col1_bet.spaces)} numbers")
    print(f"   Column 1 numbers: {sorted(col1_bet.spaces, key=int)}")
    print(f"   Second column: covers {len(col2_bet.spaces)} numbers")
    print(f"   Column 2 numbers: {sorted(col2_bet.spaces, key=int)}")
    print(f"   Third column: covers {len(col3_bet.spaces)} numbers")
    print(f"   Column 3 numbers: {sorted(col3_bet.spaces, key=int)}")
    print(f"   Payout ratio: {Bet.PAYOUT_RATIOS[BetType.FIRST_COLUMN]}:1")
    print()

    # Demonstrate betting in action
    print("=== BETTING IN ACTION ===")
    
    # Place some bets
    active_bets = [
        straight_bet,
        red_bet,
        dozen2_bet,
        col1_bet
    ]
    
    total_wagered = sum(bet.amount for bet in active_bets)
    print(f"Alice places {len(active_bets)} bets totaling {total_wagered} chips")
    
    for i, bet in enumerate(active_bets, 1):
        print(f"   {i}. {bet}")
    print()

    # Spin the wheel and check results
    print("Spinning the wheel...")
    game.spin_wheel()
    winning_space = game.current_space
    if winning_space is None:
        print("Error: No winning space found!")
        return
    print(f"Ball lands on: {winning_space.value} ({winning_space.color})")
    print()

    # Check each bet
    print("Checking bet results:")
    total_payout = 0
    
    for i, bet in enumerate(active_bets, 1):
        is_winner = bet.is_winning_bet(winning_space)
        payout = bet.calculate_payout(winning_space)
        status = "WIN" if is_winner else "LOSE"
        
        print(f"   {i}. {bet.bet_type.value}: {status}")
        if is_winner:
            winnings = payout - bet.amount
            print(f"      Payout: {payout} chips (bet: {bet.amount} + winnings: {winnings})")
        else:
            print(f"      Lost: {bet.amount} chips")
        
        total_payout += payout
    
    print()
    net_result = total_payout - total_wagered
    if net_result > 0:
        print(f"🎉 Alice wins {net_result} chips! (Wagered: {total_wagered}, Payout: {total_payout})")
    elif net_result < 0:
        print(f"😞 Alice loses {abs(net_result)} chips (Wagered: {total_wagered}, Payout: {total_payout})")
    else:
        print(f"🤝 Alice breaks even (Wagered: {total_wagered}, Payout: {total_payout})")

    print()
    print("=== BET VALIDATION EXAMPLES ===")
    
    # Show validation in action
    print("Valid bets:")
    try:
        valid_bet = Bet.create_straight_up_bet("0", amount=10, layout=layout)
        print(f"   ✓ {valid_bet}")
    except ValueError as e:
        print(f"   ✗ Error: {e}")
    
    try:
        valid_bet = Bet.create_color_bet("red", amount=20, layout=layout)
        print(f"   ✓ Red bet with {len(valid_bet.spaces)} spaces")
    except ValueError as e:
        print(f"   ✗ Error: {e}")
    
    print("\nInvalid bets:")
    try:
        invalid_bet = Bet.create_straight_up_bet("99", amount=10, layout=layout)
        print(f"   ✓ {invalid_bet}")
    except ValueError as e:
        print(f"   ✗ Invalid space: {e}")
    
    try:
        invalid_bet = Bet.create_color_bet("purple", amount=10, layout=layout)
        print(f"   ✓ {invalid_bet}")
    except ValueError as e:
        print(f"   ✗ Invalid color: {e}")
    
    try:
        invalid_bet = Bet(BetType.STRAIGHT_UP, "17", amount=-5, layout=layout)
        print(f"   ✓ {invalid_bet}")
    except ValueError as e:
        print(f"   ✗ Negative amount: {e}")

    print("\n🎲 Betting demo complete! 🎲")


if __name__ == "__main__":
    main() 