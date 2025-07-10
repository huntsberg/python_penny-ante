# Penny Ante

[![PyPI - Version](https://img.shields.io/pypi/v/penny-ante.svg)](https://pypi.org/project/penny-ante)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/penny-ante.svg)](https://pypi.org/project/penny-ante)

A Python implementation of a roulette wheel game simulator. This package provides classes for managing roulette games, including American and European wheel types, player management, and chip handling.

## Features

- **Multiple Wheel Types**: Support for both American (38 spaces) and European (37 spaces) roulette wheels
- **Player Management**: Add and manage multiple players in a game
- **Chip System**: Handle player chips and betting (basic implementation)
- **Random Number Generation**: Cryptographically secure random number generation using `os.urandom()`
- **Comprehensive Testing**: Full test coverage for all components

## Installation

```console
pip install penny-ante
```

## Quick Start

```python
from penny_ante.game import Game

# Create a new game with American wheel
game = Game(table_type='AMERICAN')

# Add players
game.add_player('Alice')
game.add_player('Bob')

# Spin the wheel
game.spin_wheel()
print(f"Landed on: {game.current_space.value} ({game.current_space.color})")
```

## Usage

### Creating a Game

```python
# American wheel (38 spaces: 0, 00, 1-36)
game = Game(table_type='AMERICAN')

# European wheel (37 spaces: 0, 1-36)
game = Game(table_type='EUROPEAN')
```

### Managing Players

```python
# Add players
game.add_player('Player1')
game.add_player('Player2')

# Players are stored in a dictionary
print(game.players['Player1'].name)  # 'Player1'
```

### Spinning the Wheel

```python
game.spin_wheel()
current_space = game.current_space
print(f"Value: {current_space.value}")
print(f"Color: {current_space.color}")
print(f"Location: {current_space.location}")
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
├── game.py      # Main game logic
├── wheel.py     # Roulette wheel implementation
├── player.py    # Player management
├── space.py     # Individual wheel spaces
└── chips.py     # Chip handling
```

## License

`penny-ante` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
