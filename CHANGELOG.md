# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-27

### Added
- **Overlay rules system**: New flexible betting rule overlay system
  - Support for custom rule modifications without changing base configurations
  - `examples/overlay_rules_demo.py` demonstrating overlay functionality
  - `OVERLAY_RULES_SUMMARY.md` documentation

### Changed
- **BREAKING**: Replaced "casino" terminology with "game" terminology throughout the codebase
  - `casino_rules` → `game_rules` in configuration files and API
  - Updated documentation to use game-focused language
  - Configuration files now use `game_rules` section instead of `casino_rules`
  - All example files and documentation updated to reflect game terminology
- **BREAKING**: Updated configuration file structure
  - `_get_casino_rules()` method renamed to `_get_game_rules()`
  - YAML configuration files require `game_rules` section instead of `casino_rules`

### Fixed
- Updated example configurations to include missing required sections
- Fixed custom configuration demos to work with current betting rules structure
- Corrected documentation references to use actual config file names

## [0.0.3] - 2025-08-05

### Added
- **Ratio-based minimum bet system**: Minimum bet amounts can now be expressed as ratios of the table minimum
- **Separate configuration files**: 
  - `config/american_rules.yaml` for American roulette (38 pockets)
  - `config/european_rules.yaml` for European roulette (37 pockets)
- **Automatic configuration selection**: BettingRules class automatically selects appropriate config based on table type
- **Comprehensive demo scripts**:
  - `examples/ratio_based_minimums_demo.py`
  - `examples/separate_configs_demo.py`
  - `examples/calculated_house_edge_demo.py`
- **Enhanced documentation**:
  - `RATIO_BASED_MINIMUMS_SUMMARY.md`
  - `SEPARATE_CONFIGS_SUMMARY.md`

### Changed
- **BREAKING**: Removed single `config/betting_rules.yaml` in favor of table-specific configs
- **BREAKING**: Updated `BettingRules` constructor to support automatic config selection
- Enhanced unit tests to cover new ratio-based system and configuration management
- Updated Game class to integrate with new betting rules architecture

### Fixed
- Improved betting rules validation and error handling
- Enhanced flexibility and scalability of betting system

## [0.0.2] - 2025-08-05

### Added
- **Configurable betting rules system** with YAML support
- `BettingRules` class for managing betting rules and validation
- `config/betting_rules.yaml` for defining payout ratios, minimum/maximum bets, and house edge
- `examples/betting_rules_demo.py` demonstrating betting rules usage
- **Comprehensive testing system**:
  - 100% test coverage with 57+ test cases
  - `test_bet.py`, `test_bet_comprehensive.py`, `test_bet_edge_cases.py`
  - `TESTING_SUMMARY.md` documenting test coverage and structure
- `examples/betting_demo.py` showcasing bet types and validation
- Bet and BetType classes added to `__init__.py` for better module organization

### Changed
- Enhanced betting system with customizable configurations
- Updated existing classes to integrate with new betting rules
- Improved bet validation and payout calculations

## [0.0.1] - 2025-07-09

### Added
- **New realistic game architecture**:
  - `Table` class: Manages wheel and betting layout
  - `Croupier` class: Handles game operations and wheel spinning  
  - `Layout` class: Manages betting grid and space positioning
- **Enhanced documentation**:
  - Comprehensive README with architecture overview
  - API reference section with all core classes and methods
  - Advanced chip operations examples
  - Realistic game operation examples
- **Code quality improvements**:
  - Type hints throughout codebase
  - Comprehensive docstrings
  - Black code formatting
  - Poe task management system

### Changed
- **BREAKING**: Game class now uses Table and Croupier instead of direct Wheel access
- Enhanced Chips class with `cash_value()` and `change_chips()` methods
- Updated all classes with comprehensive type hints and documentation
- Improved module organization with updated `__init__.py`

### Fixed
- Layout implementation to match expected test behavior
- Merge conflicts between code quality improvements and new architecture
- All 43 tests now passing successfully

## [0.0.0] - 2024-05-07 and earlier

### Added
- **Core roulette simulation**:
  - `Wheel` class supporting American (38 spaces) and European (37 spaces) roulette
  - `Space` class representing individual wheel positions
  - `Game` class for managing overall game state
  - `Player` class with chip management
  - `Chips` class for handling chip operations
- **Basic testing framework** with unit tests for core functionality
- **GitHub integration**:
  - PyLint workflow configuration
  - Repository setup and basic CI
- **Foundation classes**:
  - Random wheel spinning with proper space selection
  - Player management and chip buying system
  - Basic game initialization and configuration

### Fixed
- Off-by-one error in wheel spin routine (commit 9d16519)
- Random number generator test stability issues
- Chip handling error management
- Exception text clarity for 0 vs 00 differentiation
- Test class naming consistency

### Changed
- Refactored wheel creation algorithm
- Updated chip handling to support chip value changes
- Moved chip buying responsibility from Game to Player class
- Enhanced space lookup and wheel-layout integration

---

### Legend
- **BREAKING**: Changes that break backward compatibility
- **Added**: New features
- **Changed**: Changes in existing functionality  
- **Fixed**: Bug fixes
- **Removed**: Removed features 