#!/usr/bin/env python3
"""
Demo script showcasing the Penny Ante roulette game simulator.

This script demonstrates the new architecture with Table, Croupier, and Layout
classes, as well as the enhanced player and chip management features.
"""

from penny_ante import Game, Player, Chips


def main():
    """Run a comprehensive demo of the roulette game simulator."""
    print("🎰 Welcome to Penny Ante Roulette! 🎰\n")

    # Create a new American roulette game
    print("Creating an American roulette table...")
    game = Game(table_type="AMERICAN")

    # Show table information
    print(f"Table type: {game.table.wheel.type}")
    print(f"Number of spaces: {len(game.table.wheel.spaces)}")
    print(f"Layout type: {game.table.layout.type}")
    print()

    # Add players
    print("Adding players to the game...")
    game.add_player("Alice")
    game.add_player("Bob")
    game.add_player("Charlie")

    # Give players chips
    print("Players buying chips...")
    alice = game.players["Alice"]
    bob = game.players["Bob"]
    charlie = game.players["Charlie"]

    alice.buy_chips(count=20, value=5)  # $100 in $5 chips
    bob.buy_chips(count=50, value=1)  # $50 in $1 chips
    charlie.buy_chips(count=10, value=10)  # $100 in $10 chips

    print(f"Alice has {alice.chips.count} chips worth ${alice.chips.cash_value()}")  # type: ignore
    print(f"Bob has {bob.chips.count} chips worth ${bob.chips.cash_value()}")  # type: ignore
    print(f"Charlie has {charlie.chips.count} chips worth ${charlie.chips.cash_value()}")  # type: ignore
    print()

    # Demonstrate layout functionality
    print("Exploring the betting layout...")
    layout = game.table.layout

    # Find some spaces
    space_0 = layout.find_space("0")
    space_00 = layout.find_space("00")
    space_1 = layout.find_space("1")
    space_36 = layout.find_space("36")

    print(f"Space 0: row {space_0.layout_row}, col {space_0.layout_column}")
    print(f"Space 00: row {space_00.layout_row}, col {space_00.layout_column}")
    print(f"Space 1: row {space_1.layout_row}, col {space_1.layout_column}")
    print(f"Space 36: row {space_36.layout_row}, col {space_36.layout_column}")
    print()

    # Spin the wheel multiple times
    print("Spinning the wheel 10 times...")
    results = []

    for i in range(10):
        game.spin_wheel()
        space = game.current_space
        results.append(space.value)  # type: ignore
        print(f"Spin {i+1}: {space.value} ({space.color})")  # type: ignore

    print(f"\nResults: {', '.join(results)}")
    print()

    # Demonstrate chip operations
    print("Demonstrating advanced chip operations...")

    # Alice adds more chips
    alice.chips.change_chips(count=10)  # Add 10 more $5 chips  # type: ignore
    print(f"Alice added 10 more chips, now has ${alice.chips.cash_value()}")  # type: ignore

    # Create separate chip collections
    red_chips = Chips(value=25)
    red_chips.change_chips(count=4)  # 4 × $25 chips

    blue_chips = Chips(value=100)
    blue_chips.change_chips(count=2)  # 2 × $100 chips

    print(
        f"Red chips: {red_chips.count} × ${red_chips.value} = ${red_chips.cash_value()}"
    )
    print(
        f"Blue chips: {blue_chips.count} × ${blue_chips.value} = ${blue_chips.cash_value()}"
    )

    # Demonstrate different ways to spin
    print("\nDifferent ways to spin the wheel:")

    # Via game (recommended)
    game.spin_wheel()
    print(f"Via game: {game.current_space.value}")  # type: ignore

    # Via croupier
    game.croupier.spin_wheel()
    print(f"Via croupier: {game.current_space.value}")  # type: ignore

    # Via table
    game.table.spin_wheel()
    print(f"Via table: {game.current_space.value}")  # type: ignore

    print("\n🎉 Demo complete! Thanks for playing Penny Ante! 🎉")


if __name__ == "__main__":
    main()
