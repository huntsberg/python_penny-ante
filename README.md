# Penny Ante

[![PyPI - Version](https://img.shields.io/pypi/v/penny-ante.svg)](https://pypi.org/project/penny-ante)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/penny-ante.svg)](https://pypi.org/project/penny-ante)

A Python implementation of a roulette wheel game simulator with a realistic game architecture. This package provides classes for managing roulette games, including American and European wheel types, table management, croupier operations, player management, and comprehensive chip handling.

## Features

- **Realistic Game Architecture**: Modeled after real game operations with Table, Croupier, and Layout classes
- **Multiple Wheel Types**: Support for both American (38 spaces) and European (37 spaces) roulette wheels
- **Professional Table Management**: Integrated wheel and betting layout management
- **Croupier Operations**: Dedicated croupier for handling game operations and wheel spinning
- **Betting Layout**: Proper roulette table layout with space positioning and lookup functionality
- **Advanced Player Management**: Full player lifecycle with chip purchasing and management
- **Comprehensive Chip System**: Complete chip handling with cash value calculation and transaction management
- **Random Number Generation**: Cryptographically secure random number generation using `os.urandom()`
- **Type Safety**: Full type hints throughout the codebase for better development experience
- **Comprehensive Testing**: Full test coverage for all components with 43 test cases

## Installation

```console
pip install penny-ante
```

## Quick Start

```python
from penny_ante.game import Game

# Create a new game with American table
game = Game(table_type='AMERICAN')

# Add players and give them chips
game.add_player('Alice')
game.add_player('Bob')

# Players can buy chips
game.players['Alice'].buy_chips(count=10, value=5)  # 10 chips worth $5 each
game.players['Bob'].buy_chips(count=20, value=1)    # 20 chips worth $1 each

# Spin the wheel
game.spin_wheel()
print(f"Landed on: {game.current_space.value} ({game.current_space.color})")
print(f"Alice has ${game.players['Alice'].chips.cash_value()} in chips")
```

## Architecture Overview

The package uses a realistic game architecture:

- **Game**: Main game controller that orchestrates all components
- **Table**: Manages the physical roulette table with wheel and betting layout
- **Croupier**: Handles game operations, wheel spinning, and bet management
- **Layout**: Manages the betting grid and space positioning for bet placement
- **Wheel**: The roulette wheel with cryptographically secure spinning
- **Player**: Individual players with chip management capabilities
- **Chips**: Chip collections with value tracking and transaction handling
- **Space**: Individual spaces on the wheel with position and color information

## Key Features

### 🎯 **Overlay Configuration System**
Create custom rules that inherit from defaults - no need to specify complete configurations!

```python
# Only specify what you want to change
overlay = {
    "table_limits": {"minimum_bet": 25, "maximum_bet": 5000000},
    "payout_ratios": {"straight_up": 40}  # Higher than standard 35:1
}

game = Game(table_type="AMERICAN", overlay_rules=overlay)
# Everything else inherits from American defaults
```

**Benefits:**
- ✅ **Simplified customization** - specify only what changes
- ✅ **Automatic inheritance** - missing values use sensible defaults  
- ✅ **Type-safe** - full validation and error handling preserved
- ✅ **Backward compatible** - existing code works unchanged

See `examples/overlay_rules_demo.py` for comprehensive examples.

## Usage

### Creating a Game

```python
from penny_ante.game import Game

# American table (38 spaces: 0, 00, 1-36)
game = Game(table_type='AMERICAN')

# European table (37 spaces: 0, 1-36)
game = Game(table_type='EUROPEAN')

# Access table components
print(f"Wheel type: {game.table.wheel.type}")
print(f"Layout type: {game.table.layout.type}")
print(f"Number of spaces: {len(game.table.wheel.spaces)}")
```

### Managing Players and Chips

```python
# Add players
game.add_player('Player1')
game.add_player('Player2')

# Players can buy chips
player1 = game.players['Player1']
player1.buy_chips(count=50, value=1)  # 50 chips worth $1 each

# Check chip values
print(f"Player1 has {player1.chips.count} chips")
print(f"Total value: ${player1.chips.cash_value()}")

# Add more chips of the same value
player1.chips.change_chips(count=25)  # Add 25 more chips
print(f"Now has {player1.chips.count} chips worth ${player1.chips.cash_value()}")
```

### Working with the Table and Croupier

```python
# The croupier manages the game
croupier = game.croupier
croupier.spin_wheel()

# Access the table layout
layout = game.table.layout
space_1 = layout.find_space('1')  # Find space with value '1'
print(f"Space 1 is at row {space_1.layout_row}, column {space_1.layout_column}")

# Direct table access
table = game.table
print(f"Table has {len(table.wheel.spaces)} spaces")
```

### Spinning the Wheel

```python
# Spin via game (recommended)
game.spin_wheel()

# Or spin via croupier directly
game.croupier.spin_wheel()

# Or spin via table directly
game.table.spin_wheel()

# Access the result
current_space = game.current_space
print(f"Value: {current_space.value}")
print(f"Color: {current_space.color}")
print(f"Wheel location: {current_space.wheel_location}")
print(f"Layout position: ({current_space.layout_row}, {current_space.layout_column})")
```

### Advanced Chip Operations

```python
from penny_ante.chips import Chips

# Create chip collections
red_chips = Chips(value=5)
red_chips.change_chips(count=10)  # Add 10 chips

blue_chips = Chips(value=25)
blue_chips.change_chips(count=4)  # Add 4 chips

print(f"Red chips: {red_chips.count} × ${red_chips.value} = ${red_chips.cash_value()}")
print(f"Blue chips: {blue_chips.count} × ${blue_chips.value} = ${blue_chips.cash_value()}")

# Combine chip collections (must be same value)
more_red = Chips(value=5)
more_red.change_chips(count=5)
red_chips.change_chips(chips=more_red)  # Merge collections

print(f"Combined red chips: {red_chips.count} × ${red_chips.value} = ${red_chips.cash_value()}")
```

## Development

This project uses [Poe the Poet](https://poethepoet.natn.io/) for task management. 

### Prerequisites

Install these tools globally with [pipx](https://pypa.github.io/pipx/) (recommended):

```console
# Install pipx if you haven't already
pip install pipx

# Install global development tools
pipx install poethepoet
pipx install black
pipx install build
```

> **Why pipx?** pipx installs tools in isolated environments, preventing dependency conflicts while making them available globally. This is the recommended way to install Python CLI tools.

Alternatively, you can install poe locally:
```console
pip install poethepoet
```

### Development Setup

**Quick setup (recommended):**
```console
# Run the automated setup script
./setup-dev.sh
```

**Manual setup:**
```console
# Install the package in development mode
poe install-dev

# Show version info
poe info
```

### Testing

```console
# Run all tests
poe test

# Run tests with coverage
poe test-all

# Run tests quickly (stop on first failure)
poe test-fast

# Generate HTML coverage report
poe test-cov-html
```

### Code Quality

```console
# Format code with Black
poe format

# Check formatting
poe format-check

# Show formatting diff
poe format-diff

# Run all quality checks
poe check-all
```

### Development Utilities

```console
# Demo: spin wheel once
poe demo

# Demo: spin wheel 5 times
poe wheel-demo

# Clean build artifacts
poe clean

# Build package
poe build
```

### Composite Tasks

```console
# Setup development environment
poe dev-setup

# Pre-commit checks (format + all checks)
poe pre-commit

# CI pipeline (format-check + test with coverage)
poe ci

# Release readiness check
poe release-check
```

### Available Tasks

Run `poe --help` to see all available tasks:

- **Testing**: `test`, `test-fast`, `test-cov`, `test-cov-report`, `test-cov-html`, `test-all`
- **Code Quality**: `format`, `format-check`, `format-diff`, `lint`, `check-all`
- **Development**: `demo`, `wheel-demo`, `info`, `clean`, `build`, `install-dev`, `setup`
- **Composite**: `dev-setup`, `pre-commit`, `ci`, `release-check`

### Project Structure

```
src/penny_ante/
├── __init__.py
├── game.py      # Main game controller
├── table.py     # Roulette table management
├── croupier.py  # Croupier operations
├── layout.py    # Betting layout management
├── wheel.py     # Roulette wheel implementation
├── player.py    # Player management with chip support
├── space.py     # Individual wheel spaces
└── chips.py     # Comprehensive chip handling
```

## API Reference

### Core Classes

- **`Game`**: Main game controller with table, croupier, and player management
- **`Table`**: Manages wheel and betting layout for a roulette table
- **`Croupier`**: Handles game operations and wheel spinning
- **`Layout`**: Manages betting grid with space positioning and lookup
- **`Wheel`**: Roulette wheel with cryptographically secure spinning
- **`Player`**: Individual player with chip management capabilities
- **`Chips`**: Chip collection with value tracking and transactions
- **`Space`**: Individual wheel space with position and color information

### Key Methods

- **`Game.spin_wheel()`**: Spin the wheel via the croupier
- **`Game.add_player(name)`**: Add a new player to the game
- **`Player.buy_chips(count, value)`**: Purchase chips for the player
- **`Chips.change_chips(count, value, chips)`**: Modify chip collection
- **`Chips.cash_value()`**: Calculate total cash value of chips
- **`Layout.find_space(value)`**: Find a space on the betting layout
- **`Wheel.spin()`**: Spin the wheel and set current_space

## License

`penny-ante` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
