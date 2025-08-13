# Overlay Rules System for Penny Ante

## Overview

The Overlay Rules System allows users to create partial configurations that inherit missing values from default rules. This dramatically simplifies customization by eliminating the need to specify complete configuration files for minor changes.

## How It Works

### Basic Concept

Instead of creating a complete YAML configuration file, users can provide a dictionary that only contains the settings they want to change. The system automatically merges these changes with the appropriate default configuration (American or European).

```python
# Instead of creating a full YAML file, just specify what you want to change
overlay = {
    "table_limits": {
        "minimum_bet": 25,
        "maximum_bet": 5000000
    }
}

game = Game(table_type="AMERICAN", overlay_rules=overlay)
```

### Deep Merge Behavior

The overlay system performs a **deep merge** where:
- ✅ **Overlay values take precedence** over default values
- ✅ **Missing sections inherit** from defaults  
- ✅ **Partial sections merge** with defaults (not replace entirely)
- ✅ **Type safety preserved** through existing validation

## Usage Examples

### 1. **Higher Table Limits Only**

```python
overlay = {
    "table_limits": {
        "minimum_bet": 25,
        "maximum_bet": 5000000
    }
}

game = Game(table_type="AMERICAN", overlay_rules=overlay)
# Result: Higher limits, all other settings remain American defaults
```

### 2. **Custom Payouts Only**

```python
overlay = {
    "payout_ratios": {
        "straight_up": 40,  # Higher than standard 35:1
        "split": 20         # Higher than standard 17:1
    }
}

game = Game(table_type="AMERICAN", overlay_rules=overlay)
# Result: Custom payouts, all other settings remain American defaults
```

### 3. **Special Rules Only**

```python
overlay = {
    "game_rules": {
        "surrender": True,      # Enable surrender rule
        "maximum_repeats": 5    # Stricter monitoring
    },
    "special_rules": {
        "allow_call_bets": True
    }
}

game = Game(table_type="AMERICAN", overlay_rules=overlay)
# Result: Modified rules, all other settings remain American defaults
```

### 4. **Comprehensive Overlay**

```python
overlay = {
    "table_limits": {
        "minimum_bet": 100
    },
    "payout_ratios": {
        "straight_up": 42
    },
    "game_rules": {
        "surrender": True
    }
}

game = Game(table_type="AMERICAN", overlay_rules=overlay)
# Result: Multiple customizations while inheriting other defaults
```

## API Reference

### BettingRules Constructor

```python
BettingRules(
    config_path: Optional[str] = None,
    table_type: str = "AMERICAN", 
    overlay_config: Optional[Dict[str, Any]] = None
)
```

**Parameters:**
- `config_path`: Path to base YAML configuration (uses table defaults if None)
- `table_type`: "AMERICAN" or "EUROPEAN" 
- `overlay_config`: Dictionary to overlay on top of base configuration

### Game Constructor

```python
Game(
    table_type: Optional[str],
    betting_rules_config: Optional[str] = None,
    overlay_rules: Optional[Dict[str, Any]] = None
)
```

**Parameters:**
- `table_type`: "AMERICAN" or "EUROPEAN"
- `betting_rules_config`: Path to base YAML configuration (optional)
- `overlay_rules`: Dictionary to overlay on top of base configuration

## Configuration Sections

### Available Overlay Sections

| Section | Description | Example |
|---------|-------------|---------|
| `payout_ratios` | Payout multipliers for each bet type | `{"straight_up": 40}` |
| `minimum_bet_ratios` | Minimum bet ratios relative to table minimum | `{"red": 10.0}` |
| `maximum_bet_ratios` | Maximum bet ratios relative to table maximum | `{"straight_up": 0.3}` |
| `table_limits` | Table minimum/maximum bet amounts | `{"minimum_bet": 100}` |
| `game_rules` | Game-specific rules (en prison, surrender, etc.) | `{"surrender": true}` |
| `special_rules` | Special betting features | `{"allow_call_bets": true}` |

### Partial Section Updates

The overlay system intelligently merges sections:

```python
# Base config has:
# payout_ratios:
#   straight_up: 35
#   split: 17  
#   red: 1

# Overlay:
overlay = {
    "payout_ratios": {
        "straight_up": 40
    }
}

# Result:
# payout_ratios:
#   straight_up: 40  # ← Overlaid
#   split: 17        # ← Inherited
#   red: 1           # ← Inherited
```

## Benefits

### 🎯 **Simplified Customization**
- **No complete files needed**: Only specify what you want to change
- **Reduced configuration burden**: Inherit sensible defaults automatically
- **Type-safe**: Leverage existing validation and error handling

### 🔄 **Flexible Inheritance** 
- **Table-specific defaults**: Automatic American vs European base configurations
- **Deep merging**: Partial section updates preserve other values
- **Custom base configs**: Overlay on top of custom YAML files

### 🛡️ **Backward Compatibility**
- **Existing code unchanged**: All current configurations continue to work
- **Optional feature**: Overlay is opt-in, defaults to original behavior
- **Validation preserved**: All existing validation rules still apply

### 🚀 **Use Cases**

| Scenario | Traditional Approach | Overlay Approach |
|----------|---------------------|------------------|
| Higher table limits | Create complete 87-line YAML file | 4-line dictionary |
| Custom payout for one bet | Copy entire config, modify one value | 1-line dictionary |
| Enable surrender rule | Duplicate full config structure | 1-line dictionary |
| Multiple minor changes | Maintain separate config files | Single overlay dictionary |

## Examples in Action

### Before: Traditional Approach

```yaml
# custom_high_limits.yaml (87 lines)
payout_ratios:
  straight_up: 35
  split: 17
  street: 11
  corner: 8
  six_line: 5
  red: 1
  black: 1
  # ... 20+ more lines

minimum_bet_ratios:
  global: 1.0
  straight_up: 1.0
  # ... 15+ more lines

table_limits:
  minimum_bet: 100      # ← Only thing we wanted to change!
  maximum_bet: 5000000  # ← Only thing we wanted to change!
  maximum_total_bet: 50000000

# ... 50+ more lines
```

### After: Overlay Approach

```python
# Just 4 lines!
overlay = {
    "table_limits": {
        "minimum_bet": 100,
        "maximum_bet": 5000000
    }
}

game = Game(table_type="AMERICAN", overlay_rules=overlay)
```

## Error Handling

The overlay system preserves all existing validation:

```python
# This will still raise validation errors
invalid_overlay = {
    "payout_ratios": {
        "invalid_bet_type": 50  # ← Will fail validation
    }
}

# This will still validate properly
valid_overlay = {
    "table_limits": {
        "minimum_bet": -5  # ← Will fail table limits validation
    }
}
```

## Testing

The overlay system includes comprehensive tests covering:

- ✅ **Basic overlay functionality** 
- ✅ **Deep merge behavior**
- ✅ **Multiple section overlays**
- ✅ **European vs American base configs**
- ✅ **Integration with Game class**
- ✅ **Validation preservation**
- ✅ **Custom config file compatibility**

Run tests with:
```bash
python -m pytest tests/test_overlay_rules.py -v
```

## Migration Guide

### For Existing Users
**No migration needed!** All existing code continues to work unchanged:

```python
# This still works exactly as before
game = Game(table_type="AMERICAN")
rules = BettingRules(config_path="my_config.yaml", table_type="EUROPEAN")
```

### For New Features
Add overlay parameters to leverage new functionality:

```python
# NEW: Add overlay_rules parameter
game = Game(
    table_type="AMERICAN",
    overlay_rules={"table_limits": {"minimum_bet": 50}}
)

# NEW: Add overlay_config parameter  
rules = BettingRules(
    table_type="EUROPEAN",
    overlay_config={"game_rules": {"la_partage": False}}
)
```

---

## Summary

The Overlay Rules System transforms configuration management from:
- ❌ **Verbose**: 87-line YAML files for minor changes
- ❌ **Error-prone**: Copying and modifying large config files  
- ❌ **Maintenance burden**: Multiple config files to maintain

To:
- ✅ **Concise**: Few-line dictionaries for changes
- ✅ **Safe**: Automatic inheritance of validated defaults
- ✅ **Maintainable**: Single source of truth with targeted overlays

This makes the Penny Ante library much more accessible for users who want to customize game behavior without deep configuration file management.