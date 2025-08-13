# Comprehensive Betting Enforcement System

## Overview

I have successfully implemented a comprehensive betting limits and rules enforcement system for the penny-ante roulette library. This system ensures that all betting activities comply with configurable rules and limits, providing a robust foundation for casino-style gaming.

## ✅ Completed Features

### 1. **Individual Bet Amount Limits**
- **Minimum bet enforcement**: Each bet type has configurable minimum amounts
- **Maximum bet enforcement**: Each bet type has configurable maximum amounts based on ratios of table maximum
- **Bet type validation**: Only allowed bet types can be placed
- **Real-time validation**: Limits are checked when bets are created

**Example:**
```python
# Straight up bets limited to 50% of table maximum
bet = Bet.create_straight_up_bet("17", amount=500000, betting_rules=rules)  # ✓ Valid
bet = Bet.create_straight_up_bet("17", amount=600000, betting_rules=rules)  # ✗ Exceeds limit
```

### 2. **Total Bet Limits Across All Players**
- **Table-wide total limits**: Maximum total amount that can be wagered per spin
- **Progressive validation**: Each new bet is checked against running total
- **Multi-player support**: Tracks bets across all players at the table
- **Automatic enforcement**: Prevents exceeding limits before wheel spin

**Example:**
```python
# With 10M total limit, after 9.9M in bets:
game.place_bet(small_bet, "Alice")  # ✓ Valid if under limit
game.place_bet(large_bet, "Alice")  # ✗ Would exceed total limit
```

### 3. **Player Chip Balance Validation**
- **Insufficient funds prevention**: Players cannot bet more chips than they have
- **Real-time balance tracking**: Chip counts updated immediately when bets are placed
- **Balance inquiry methods**: Easy access to player chip information
- **Automatic deduction**: Chips are deducted when bets are successfully placed

**Example:**
```python
player.can_afford_bet(1000)  # Check if player has enough chips
game.place_bet(bet, "Alice")  # Automatically deducts chips if valid
```

### 4. **Betting Phase Management**
- **Open/Closed betting phases**: Control when bets can be placed
- **Automatic phase transitions**: Betting closes when wheel spins
- **Phase validation**: Prevents betting when phase is closed
- **Round management**: Clear bets and open new rounds automatically

**Example:**
```python
game.betting_open  # True initially
game.close_betting()  # Manually close betting
game.place_bet(bet)  # ✗ Raises ValueError: "Betting is closed"
game.spin_wheel()  # Automatically closes betting if open
game.open_betting()  # Start new round
```

### 5. **Special Rules Enforcement**
- **Call bets control**: Enable/disable oral bets without chips on table
- **Neighbor bets control**: Enable/disable bets on wheel-adjacent numbers
- **Progressive betting limits**: Control betting system usage
- **Parlay limits**: Maximum consecutive win reinvestment
- **Configurable rules**: All special rules are YAML-configurable

**Example:**
```python
rules.is_special_rule_enabled('allow_call_bets')  # False
rules.get_game_rule('maximum_parlay')  # 5
```

### 6. **Comprehensive Multi-Bet Validation**
- **Batch validation**: Validate multiple bets together
- **Detailed reporting**: Comprehensive validation results with errors and warnings
- **Bet type analysis**: Count and total amounts by bet type
- **Error aggregation**: Collect all validation issues in one report

**Example:**
```python
validation_result = rules.validate_multiple_bets([bet1, bet2, bet3])
# Returns: {'valid': True, 'errors': [], 'total_amount': 1500, ...}
```

## 🏗️ System Architecture

### Core Components

#### 1. **Enhanced BettingRules Class**
- `validate_total_bet_amount()` - Check total bet limits
- `validate_multiple_bets()` - Comprehensive multi-bet validation
- `is_special_rule_enabled()` - Query special rule status
- `get_game_rule()` - Access game rule values

#### 2. **Enhanced Game Class**
- `place_bet()` - Place bet with full validation
- `close_betting()` / `open_betting()` - Manage betting phases
- `validate_all_bets()` - Validate all active bets
- `get_bet_summary()` - Get comprehensive bet information
- `get_total_bet_amount()` - Get current total bet amount

#### 3. **Enhanced Player Class**
- `can_afford_bet()` - Check if player can afford bet amount
- `get_chip_balance()` - Get current chip count
- `get_total_value()` - Get total monetary value of chips

#### 4. **Enhanced Bet Class**
- Automatic betting rules validation in constructor
- Support for betting_rules parameter in all factory methods
- Integration with table-level validation

## 📋 Configuration

### YAML Configuration Structure
```yaml
# Individual bet limits
minimum_bet_ratios:
  global: 1.0
  straight_up: 1.0
  red: 5.0

maximum_bet_ratios:
  global: 1.0
  straight_up: 0.5
  red: 1.0

# Table-wide limits
table_limits:
  minimum_bet: 1
  maximum_bet: 1000000
  maximum_total_bet: 10000000

# Special rules
special_rules:
  allow_call_bets: false
  allow_neighbor_bets: false
  progressive_betting: true
  maximum_parlay: 5

# Game rules
game_rules:
  en_prison: false
  la_partage: false
  maximum_repeats: 10
```

## 🧪 Testing

### Comprehensive Test Suite
- **11 test methods** covering all enforcement scenarios
- **Individual bet limit testing** - min/max amounts per bet type
- **Total bet limit testing** - table-wide limits across players
- **Player balance testing** - chip sufficiency validation
- **Betting phase testing** - open/closed phase management
- **Special rules testing** - rule configuration and queries
- **Edge case testing** - error handling and boundary conditions

### Test Coverage
```bash
python -m pytest tests/test_bet_enforcement.py -v
# ============================================ 11 passed ============================================
```

## 🎯 Usage Examples

### Basic Betting with Enforcement
```python
from penny_ante import Game, Bet

# Create game with automatic rule enforcement
game = Game(table_type="AMERICAN")
game.add_player("Alice")
alice = game.players["Alice"]
alice.buy_chips(count=10000, value=1)

# Place bet with automatic validation
bet = Bet.create_color_bet("red", amount=1000, 
                          layout=game.table.layout,
                          betting_rules=game.betting_rules)
game.place_bet(bet, "Alice")  # Validates amount, balance, and limits

# Check betting status
summary = game.get_bet_summary()
print(f"Total bets: {summary['total_bets']}")
print(f"Total amount: ${summary['total_amount']:,}")
```

### Custom Rules Configuration
```python
# Create game with custom betting rules
custom_rules = {
    'table_limits': {
        'minimum_bet': 10,
        'maximum_bet': 50000,
        'maximum_total_bet': 500000
    },
    'special_rules': {
        'allow_call_bets': True,
        'maximum_parlay': 3
    }
}

game = Game(table_type="AMERICAN", overlay_rules=custom_rules)
```

### Betting Phase Management
```python
# Manage betting phases
game.open_betting()  # Start accepting bets
# ... players place bets ...
validation_result = game.close_betting()  # Stop accepting bets
if validation_result['valid']:
    game.spin_wheel()  # Spin only if all bets are valid
game.open_betting()  # Start new round
```

## 🔒 Security & Integrity

### Validation Layers
1. **Individual bet validation** - Amount limits per bet type
2. **Player balance validation** - Sufficient chip verification
3. **Table total validation** - Aggregate bet limit enforcement
4. **Phase validation** - Betting window enforcement
5. **Special rules validation** - Custom rule compliance

### Error Handling
- **Descriptive error messages** - Clear indication of what went wrong
- **Graceful failure** - System remains stable when limits are exceeded
- **Comprehensive logging** - Detailed validation results for debugging
- **Atomic operations** - Bets are either fully valid or fully rejected

## 🎉 Benefits

### For Casino Operators
- **Risk management** - Configurable limits protect against excessive exposure
- **Compliance** - Enforce gaming regulations and house rules
- **Flexibility** - Easy configuration changes without code modifications
- **Audit trail** - Comprehensive validation logging

### For Players
- **Fair play** - Consistent rule enforcement for all players
- **Clear feedback** - Immediate notification of invalid bets
- **Balance protection** - Cannot accidentally bet more than available
- **Transparent limits** - Clear understanding of betting constraints

### For Developers
- **Robust API** - Comprehensive validation methods
- **Easy integration** - Simple to add to existing games
- **Extensible design** - Easy to add new rules and limits
- **Well tested** - Comprehensive test suite ensures reliability

## 🚀 Future Enhancements

The system is designed to be easily extensible. Potential future additions include:

- **Dynamic limits** - Adjust limits based on game state or player history
- **Player-specific limits** - Individual limits based on player status
- **Time-based rules** - Different limits for different times of day
- **Advanced neighbor bets** - Full implementation of wheel-adjacent betting
- **Progressive jackpot integration** - Special handling for progressive bets
- **Multi-table coordination** - Limits across multiple tables

---

The betting enforcement system provides a solid foundation for professional-grade roulette gaming, ensuring fair play, risk management, and regulatory compliance while maintaining flexibility and ease of use.
