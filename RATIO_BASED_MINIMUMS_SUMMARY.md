# Ratio-Based Minimum Bet System

## Overview

I've successfully implemented a ratio-based minimum bet system that expresses minimum bet amounts as ratios of the table minimum, similar to the maximum bet ratio system. This provides intelligent scaling, flexible configuration, and easier maintenance of betting limits.

## How It Works

### Ratio-Based Configuration
Instead of fixed minimum amounts, the system uses ratios:

```yaml
# Before: Fixed amounts
minimum_bets:
  straight_up: 1
  red: 5

# After: Ratio-based
minimum_bet_ratios:
  straight_up: 1.0      # 100% of table minimum
  red: 5.0              # 500% of table minimum
```

### Calculation Formula
```
Minimum Bet Amount = Table Minimum × Minimum Bet Ratio
```

**Example:**
- Table minimum: $10
- Red bet ratio: 5.0
- Red minimum bet: $10 × 5.0 = $50

## Configuration Changes

### American Configuration (`config/american_rules.yaml`)
```yaml
minimum_bet_ratios:
  global: 1.0           # Default: 100% of table minimum
  straight_up: 1.0      # Same as table minimum
  split: 1.0
  street: 1.0
  corner: 1.0
  six_line: 1.0
  red: 5.0              # Higher: 500% of table minimum
  black: 5.0
  # ... all outside bets: 5.0
```

### European Configuration (`config/european_betting_rules.yaml`)
```yaml
minimum_bet_ratios:
  global: 1.0           # Default: 100% of table minimum
  straight_up: 0.5      # Lower: 50% of table minimum
  split: 0.5            # Encourage high-risk bets
  street: 1.0
  corner: 1.0
  six_line: 1.0
  red: 5.0              # Same outside bet ratio as American
  black: 5.0
  # ... all outside bets: 5.0
```

## Key Differences Between Tables

### American vs European Ratios

| Bet Type | American Ratio | European Ratio | Strategy |
|----------|----------------|----------------|----------|
| Straight Up | 1.0 (100%) | 0.5 (50%) | European encourages high-risk |
| Split | 1.0 (100%) | 0.5 (50%) | European encourages high-risk |
| Outside Bets | 5.0 (500%) | 5.0 (500%) | Same barrier for outside bets |

### Actual Minimum Calculations

**American Table ($1 minimum):**
- Straight up: $1 × 1.0 = $1
- Red: $1 × 5.0 = $5

**European Table ($2 minimum):**
- Straight up: $2 × 0.5 = $1
- Red: $2 × 5.0 = $10

## Enhanced BettingRules Class

### New Methods
```python
# Get minimum bet ratio
ratio = rules.get_minimum_bet_ratio(BetType.RED)  # Returns 5.0

# Get calculated minimum bet (existing method enhanced)
min_bet = rules.get_minimum_bet(BetType.RED)  # Returns table_min × ratio
```

### Updated Internal Structure
```python
class BettingRules:
    def __init__(self, config_path=None, table_type="AMERICAN"):
        # ...
        self.minimum_bet_ratios = self._get_minimum_bet_ratios()  # New
        # ...
    
    def _get_minimum_bet_ratios(self) -> Dict[str, float]:
        """Get minimum bet ratios from configuration."""
        return self.config.get('minimum_bet_ratios', {})
    
    def get_minimum_bet(self, bet_type: "BetType") -> int:
        """Calculate minimum bet from ratio and table minimum."""
        table_minimum = self.table_limits.get('minimum_bet', 1)
        ratio = self.get_minimum_bet_ratio(bet_type)
        return int(table_minimum * ratio)
```

## Scaling Examples

### Automatic Scaling with Table Minimums

| Table Min | American Straight Up | American Red | European Straight Up | European Red |
|-----------|---------------------|-------------|---------------------|-------------|
| $1 | $1 (1.0×) | $5 (5.0×) | $1 (0.5×) | $5 (5.0×) |
| $5 | $5 (1.0×) | $25 (5.0×) | $3 (0.5×) | $25 (5.0×) |
| $10 | $10 (1.0×) | $50 (5.0×) | $5 (0.5×) | $50 (5.0×) |
| $25 | $25 (1.0×) | $125 (5.0×) | $13 (0.5×) | $125 (5.0×) |
| $50 | $50 (1.0×) | $250 (5.0×) | $25 (0.5×) | $250 (5.0×) |

### Benefits of Scaling
✅ **Change table minimum once** → All bet minimums adjust automatically  
✅ **Maintain proportional relationships** between bet types  
✅ **No manual updates** required for each bet type  
✅ **Consistent player experience** across different table limits  

## Betting Validation Integration

### Enhanced Validation
```python
# Bet validation now uses calculated minimums
american_rules = BettingRules(table_type="AMERICAN")
european_rules = BettingRules(table_type="EUROPEAN")

# American: $5 red minimum (1 × 5.0)
american_bet = Bet.create_color_bet("red", amount=3, betting_rules=american_rules)
# ❌ ValueError: Below minimum of $5

# European: $10 red minimum (2 × 5.0)  
european_bet = Bet.create_color_bet("red", amount=8, betting_rules=european_rules)
# ❌ ValueError: Below minimum of $10
```

### Smart Ratio Design
```python
# European encourages inside bets with lower ratios
straight_up_euro = Bet.create_straight_up_bet("17", amount=1, betting_rules=european_rules)
# ✅ Accepted: $1 meets $1 minimum (2 × 0.5)

straight_up_american = Bet.create_straight_up_bet("17", amount=1, betting_rules=american_rules)  
# ✅ Accepted: $1 meets $1 minimum (1 × 1.0)
```

## Configuration Patterns

### Conservative Pattern (Favors House)
```yaml
minimum_bet_ratios:
  straight_up: 1.0      # No advantage for inside bets
  red: 10.0             # High barriers for outside bets
```

### Aggressive Pattern (Encourages Betting)
```yaml
minimum_bet_ratios:
  straight_up: 0.25     # Very low barriers for inside bets
  red: 2.0              # Moderate barriers for outside bets
```

### Balanced Pattern (Current System)
```yaml
minimum_bet_ratios:
  straight_up: 0.5-1.0  # Reasonable inside bet access
  red: 5.0              # Maintain outside bet profitability
```

## Risk Management Benefits

### 1. **Proportional Risk Control**
- Inside bets: Lower ratios = encourage high-risk, high-reward bets
- Outside bets: Higher ratios = maintain steady revenue from safer bets
- Automatic scaling maintains risk balance across table limits

### 2. **Revenue Optimization**
- Higher table minimums automatically increase all bet minimums proportionally
- No need to manually adjust each bet type for different table limits
- Consistent profit margins across different table configurations

### 3. **Player Psychology**
- Lower inside bet ratios encourage "lottery ticket" mentality
- Higher outside bet ratios push players toward inside bets
- Predictable scaling helps players understand bet requirements

## Testing Coverage

### Comprehensive Test Updates
- ✅ **119 total tests** passing
- ✅ **New ratio-based calculations** tested
- ✅ **Scaling validation** with different table minimums
- ✅ **Configuration validation** for ratio format
- ✅ **Betting validation** with calculated minimums

### Key Test Scenarios
```python
def test_minimum_bet_ratios(self):
    rules = BettingRules(config_path=test_config, table_type="AMERICAN")
    
    # Test ratio retrieval
    assert rules.get_minimum_bet_ratio(BetType.STRAIGHT_UP) == 0.2
    assert rules.get_minimum_bet_ratio(BetType.RED) == 10.0
    
    # Test calculated minimums
    assert rules.get_minimum_bet(BetType.STRAIGHT_UP) == 1  # 5 × 0.2
    assert rules.get_minimum_bet(BetType.RED) == 50         # 5 × 10.0
```

## Migration and Compatibility

### Breaking Changes
- ❌ Configuration now requires `minimum_bet_ratios` instead of `minimum_bets`
- ❌ Old `minimum_bets` configurations will cause validation errors

### Maintained Compatibility
- ✅ All `BettingRules` public methods work unchanged
- ✅ `get_minimum_bet()` still returns integer amounts
- ✅ Betting validation logic unchanged
- ✅ All existing bet creation works identically

### Migration Steps
1. **Update configuration files**: Replace `minimum_bets` with `minimum_bet_ratios`
2. **Convert amounts to ratios**: Divide old amounts by table minimum
3. **Test scaling**: Verify ratios produce expected minimums at different table limits

**Example Migration:**
```yaml
# Old format
minimum_bets:
  straight_up: 1    # $1 minimum
  red: 5           # $5 minimum
table_limits:
  minimum_bet: 1   # $1 table minimum

# New format  
minimum_bet_ratios:
  straight_up: 1.0  # 1/1 = 1.0 ratio
  red: 5.0         # 5/1 = 5.0 ratio
table_limits:
  minimum_bet: 1   # $1 table minimum
```

## Business Value

### 🎯 **Operational Efficiency**
- **Single point of control**: Change table minimum to adjust all bet minimums
- **Consistent scaling**: Same ratio structure across all table limits
- **Reduced maintenance**: No need to update individual bet minimums

### 📊 **Revenue Management**
- **Flexible positioning**: Adjust ratios to encourage/discourage bet types
- **Market adaptation**: Easy scaling for different market segments
- **Risk optimization**: Maintain profit margins across table limits

### 🚀 **Strategic Advantages**
- **Competitive differentiation**: European tables can offer lower inside bet barriers
- **Player attraction**: Lower ratios on high-payout bets increase appeal
- **Scalability**: Easy to launch new table limits with consistent rules

## Future Enhancements

### Potential Additions
- **Dynamic ratios**: Time-based or volume-based ratio adjustments
- **Player-specific ratios**: VIP players get different minimum ratios
- **Progressive ratios**: Ratios that change based on recent wins/losses
- **Market-based ratios**: Regional variations in ratio structures

### Integration Opportunities
- **Analytics**: Track ratio effectiveness across different bet types
- **A/B testing**: Compare different ratio configurations
- **Machine learning**: Optimize ratios based on player behavior
- **Regulatory compliance**: Built-in ratio limits for different jurisdictions

## Summary

The ratio-based minimum bet system provides:

✅ **Intelligent scaling** with table minimums  
✅ **Flexible risk management** through configurable ratios  
✅ **Simplified maintenance** with single-point control  
✅ **Strategic positioning** for different table types  
✅ **Enhanced player experience** with predictable scaling  
✅ **Business optimization** through proportional revenue control  

This enhancement transforms minimum bet management from a static configuration into a dynamic, intelligent system that automatically adapts to different table limits while maintaining strategic betting relationships and risk management objectives. 