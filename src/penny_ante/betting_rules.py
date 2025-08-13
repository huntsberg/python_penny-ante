import os
import yaml
from typing import Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from penny_ante.bet import BetType


class BettingRules:
    """
    Manages betting rules and configuration for roulette games.
    
    This class reads betting rules from YAML configuration files, including
    payout ratios, minimum bets, maximum bet ratios, and other game-specific
    betting parameters. Automatically selects the appropriate configuration
    file based on table type (American or European).
    
    Attributes:
        config (Dict[str, Any]): The loaded configuration dictionary
        table_type (str): The type of table ('AMERICAN' or 'EUROPEAN')
        payout_ratios (Dict): Payout ratios for each bet type
        minimum_bet_ratios (Dict): Minimum bet ratios for each bet type
        maximum_bet_ratios (Dict): Maximum bet ratios for each bet type
        # Note: house_edge is now calculated dynamically based on payout ratios and table type
        game_rules (Dict): Game-specific rules
        special_rules (Dict): Special betting rules
    """

    DEFAULT_AMERICAN_CONFIG = "config/american_rules.yaml"
    DEFAULT_EUROPEAN_CONFIG = "config/european_rules.yaml"
    
    def __init__(self, config_path: Optional[str] = None, table_type: str = "AMERICAN", 
                 overlay_config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize betting rules from configuration file with optional overlay.
        
        Args:
            config_path: Path to YAML configuration file. If None, uses table-specific default.
            table_type: Type of roulette table ('AMERICAN' or 'EUROPEAN')
            overlay_config: Optional dictionary to overlay on top of the base configuration.
                          This allows partial configurations that inherit missing values from defaults.
            
        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ValueError: If configuration is invalid
        """
        self.table_type = table_type.upper()
        
        # Use table-specific default path if none provided
        if config_path is None:
            if self.table_type == "AMERICAN":
                config_path = self.DEFAULT_AMERICAN_CONFIG
            elif self.table_type == "EUROPEAN":
                config_path = self.DEFAULT_EUROPEAN_CONFIG
            else:
                raise ValueError(f"Unsupported table type: {table_type}")
        
        self.config_path = config_path
        self.overlay_config = overlay_config
        self.config = self._load_config()
        
        # Apply overlay configuration if provided
        if overlay_config:
            self.config = self._apply_overlay(self.config, overlay_config)
        
        self._validate_config(self.config)
        
        # Extract configuration sections
        self.payout_ratios = self._get_payout_ratios()
        self.minimum_bet_ratios = self._get_minimum_bet_ratios()
        self.maximum_bet_ratios = self._get_maximum_bet_ratios()
        self.table_limits = self._get_table_limits()
        self.game_rules = self._get_game_rules()
        self.special_rules = self._get_special_rules()
        # Note: house_edge is now calculated dynamically, not stored
        
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Returns:
            Dictionary containing the configuration
            
        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ValueError: If YAML is invalid
        """
        try:
            # Try absolute path first, then relative to project root
            config_path = Path(self.config_path)
            if not config_path.exists():
                # Try relative to project root
                project_root = Path(__file__).parent.parent.parent
                config_path = project_root / self.config_path
                
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
                
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
                
            if not config:
                raise ValueError("Configuration file is empty or invalid")
                
            # Validate required sections exist
            self._validate_config(config)
            return config
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")
            
    def _apply_overlay(self, base_config: Dict[str, Any], overlay_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply overlay configuration on top of base configuration.
        
        This method performs a deep merge where overlay values take precedence over base values.
        Missing sections in overlay will use base values, allowing partial configurations.
        
        Args:
            base_config: The base configuration (usually from default files)
            overlay_config: The overlay configuration to apply on top
            
        Returns:
            Merged configuration dictionary
        """
        # Start with a deep copy of the base config
        merged_config = self._deep_copy_dict(base_config)
        
        # Apply overlay values
        for section_name, section_value in overlay_config.items():
            if isinstance(section_value, dict) and section_name in merged_config:
                # Merge dictionaries recursively
                if isinstance(merged_config[section_name], dict):
                    merged_config[section_name].update(section_value)
                else:
                    merged_config[section_name] = section_value
            else:
                # Replace entire section
                merged_config[section_name] = section_value
                
        return merged_config
    
    def _deep_copy_dict(self, original: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a deep copy of a dictionary.
        
        Args:
            original: The dictionary to copy
            
        Returns:
            Deep copy of the dictionary
        """
        result = {}
        for key, value in original.items():
            if isinstance(value, dict):
                result[key] = self._deep_copy_dict(value)
            elif isinstance(value, list):
                result[key] = value.copy()
            else:
                result[key] = value
        return result
            
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate that the configuration has all required sections.
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            ValueError: If required sections are missing
        """
        required_sections = ['payout_ratios', 'minimum_bet_ratios', 'maximum_bet_ratios', 'table_limits']
        # Note: house_edge no longer required - calculated automatically
        missing_sections = [section for section in required_sections if section not in config]
        
        if missing_sections:
            raise ValueError(f"Missing required configuration sections: {missing_sections}")
        
        # Note: With separate config files, we no longer need table_type validation
            
    def _get_payout_ratios(self) -> Dict[str, int]:
        """Get payout ratios from configuration."""
        return self.config.get('payout_ratios', {})
        
    def _get_minimum_bet_ratios(self) -> Dict[str, float]:
        """Get minimum bet ratios from configuration."""
        return self.config.get('minimum_bet_ratios', {})
        
    def _get_maximum_bet_ratios(self) -> Dict[str, float]:
        """Get maximum bet ratios from configuration."""
        return self.config.get('maximum_bet_ratios', {})
        
    # Note: _get_house_edge removed - house edge is now calculated dynamically
        
    def _get_table_limits(self) -> Dict[str, int]:
        """Get table limits from configuration."""
        return self.config.get('table_limits', {})
    
    def _get_game_rules(self) -> Dict[str, Any]:
        """Get game-specific rules from configuration."""
        return self.config.get('game_rules', {})
    
    def _get_special_rules(self) -> Dict[str, Any]:
        """Get special betting rules from configuration."""
        return self.config.get('special_rules', {})
        
    def get_payout_ratio(self, bet_type: "BetType") -> int:
        """
        Get the payout ratio for a specific bet type.
        
        Args:
            bet_type: The type of bet
            
        Returns:
            Payout ratio (e.g., 35 for 35:1)
            
        Raises:
            ValueError: If bet type is not configured
        """
        bet_type_str = bet_type.value if hasattr(bet_type, 'value') else str(bet_type)
        
        if bet_type_str not in self.payout_ratios:
            raise ValueError(f"No payout ratio configured for bet type: {bet_type_str}")
            
        return self.payout_ratios[bet_type_str]
        
    def get_minimum_bet(self, bet_type: "BetType") -> int:
        """
        Get the minimum bet amount for a specific bet type.
        
        Args:
            bet_type: The type of bet
            
        Returns:
            Minimum bet amount (calculated from ratio and table minimum)
        """
        bet_type_str = bet_type.value if hasattr(bet_type, 'value') else str(bet_type)
        table_minimum = self.table_limits.get('minimum_bet', 1)
        
        # Get ratio for this bet type or use global ratio
        if bet_type_str in self.minimum_bet_ratios:
            ratio = self.minimum_bet_ratios[bet_type_str]
        elif 'global' in self.minimum_bet_ratios:
            ratio = self.minimum_bet_ratios['global']
        else:
            ratio = 1.0  # Default to 100% of table minimum
            
        return int(table_minimum * ratio)
            
    def get_maximum_bet(self, bet_type: "BetType") -> int:
        """
        Get the maximum bet amount for a specific bet type.
        
        Args:
            bet_type: The type of bet
            
        Returns:
            Maximum bet amount (calculated from ratio and table maximum)
        """
        bet_type_str = bet_type.value if hasattr(bet_type, 'value') else str(bet_type)
        table_maximum = self.table_limits.get('maximum_bet', 1000000)
        
        # Get ratio for this bet type or use global ratio
        if bet_type_str in self.maximum_bet_ratios:
            ratio = self.maximum_bet_ratios[bet_type_str]
        elif 'global' in self.maximum_bet_ratios:
            ratio = self.maximum_bet_ratios['global']
        else:
            ratio = 1.0  # Default to 100% of table maximum
            
        return int(table_maximum * ratio)
            
    def get_house_edge(self, bet_type: "BetType") -> float:
        """
        Calculate the house edge percentage for a specific bet type.
        
        The house edge is calculated mathematically based on:
        - The probability of winning the bet
        - The payout ratio offered
        - The number of possible outcomes (37 for European, 38 for American)
        
        Formula: House Edge = (1 - (Winning Probability × (Payout + 1))) × 100
        
        Args:
            bet_type: The type of bet
            
        Returns:
            Calculated house edge as a percentage (e.g., 5.26 for 5.26%)
        """
        return self._calculate_house_edge(bet_type)
    
    def _calculate_house_edge(self, bet_type: "BetType") -> float:
        """
        Calculate the mathematical house edge for a bet type.
        
        Args:
            bet_type: The type of bet to calculate house edge for
            
        Returns:
            House edge as a percentage
        """
        # Get the number of pockets on the wheel
        total_pockets = 37 if self.table_type == "EUROPEAN" else 38
        
        # Get the payout ratio for this bet type
        payout_ratio = self.get_payout_ratio(bet_type)
        
        # Determine winning outcomes for each bet type
        winning_outcomes = self._get_winning_outcomes(bet_type)
        
        # Calculate probability of winning
        win_probability = winning_outcomes / total_pockets
        
        # Calculate house edge: (1 - (win_probability × (payout + 1))) × 100
        house_edge = (1 - (win_probability * (payout_ratio + 1))) * 100
        
        return round(house_edge, 2)
    
    def _get_winning_outcomes(self, bet_type: "BetType") -> int:
        """
        Get the number of winning outcomes for a specific bet type.
        
        Args:
            bet_type: The type of bet
            
        Returns:
            Number of winning outcomes on the wheel
        """
        bet_type_str = bet_type.value if hasattr(bet_type, 'value') else str(bet_type)
        
        # Inside bets
        if bet_type_str == 'straight_up':
            return 1  # Single number
        elif bet_type_str == 'split':
            return 2  # Two adjacent numbers
        elif bet_type_str == 'street':
            return 3  # Three numbers in a row
        elif bet_type_str == 'corner':
            return 4  # Four numbers in a square
        elif bet_type_str == 'six_line':
            return 6  # Six numbers (two rows)
        
        # Outside bets
        elif bet_type_str in ['red', 'black']:
            return 18  # 18 red or 18 black numbers
        elif bet_type_str in ['odd', 'even']:
            return 18  # 18 odd or 18 even numbers (0 doesn't count)
        elif bet_type_str in ['high', 'low']:
            return 18  # 18 high (19-36) or 18 low (1-18) numbers
        elif bet_type_str in ['first_dozen', 'second_dozen', 'third_dozen']:
            return 12  # 12 numbers in each dozen
        elif bet_type_str in ['first_column', 'second_column', 'third_column']:
            return 12  # 12 numbers in each column
        
        # Default fallback
        else:
            raise ValueError(f"Unknown bet type for house edge calculation: {bet_type_str}")
                
    def validate_bet_amount(self, bet_type: "BetType", amount: int) -> bool:
        """
        Validate that a bet amount is within the allowed range.
        
        Args:
            bet_type: The type of bet
            amount: The bet amount to validate
            
        Returns:
            True if bet amount is valid, False otherwise
        """
        min_bet = self.get_minimum_bet(bet_type)
        max_bet = self.get_maximum_bet(bet_type)
        
        return min_bet <= amount <= max_bet
        
    def get_table_minimum(self) -> int:
        """Get the overall table minimum bet."""
        return self.table_limits.get('minimum_bet', 1)
        
    def get_table_maximum(self) -> int:
        """Get the overall table maximum bet."""
        return self.table_limits.get('maximum_bet', 1000000)
        
    def get_maximum_total_bet(self) -> int:
        """Get the maximum total bet amount per spin."""
        return self.table_limits.get('maximum_total_bet', 10000000)
        
    def is_bet_allowed(self, bet_type: "BetType") -> bool:
        """
        Check if a specific bet type is allowed on this table.
        
        Args:
            bet_type: The type of bet to check
            
        Returns:
            True if bet type is allowed, False otherwise
        """
        bet_type_str = bet_type.value if hasattr(bet_type, 'value') else str(bet_type)
        
        # Check if bet type exists in payout ratios (indicates it's allowed)
        return bet_type_str in self.payout_ratios
        
    def get_all_payout_ratios(self) -> Dict[str, int]:
        """Get all payout ratios as a dictionary."""
        return self.payout_ratios.copy()
        
    def get_table_info(self) -> Dict[str, Any]:
        """
        Get comprehensive table information.
        
        Returns:
            Dictionary with table limits, rules, and configuration
        """
        # Import BetType to calculate a representative house edge
        from penny_ante.bet import BetType
        
        # Calculate house edge for a representative bet type (red)
        try:
            representative_house_edge = self.get_house_edge(BetType.RED)
        except (ValueError, AttributeError):
            # Fallback if calculation fails
            representative_house_edge = 5.26 if self.table_type == "AMERICAN" else 2.70
        
        return {
            'table_type': self.table_type,
            'minimum_bet': self.get_table_minimum(),
            'maximum_bet': self.get_table_maximum(),
            'maximum_total_bet': self.get_maximum_total_bet(),
            'payout_ratios': self.get_all_payout_ratios(),
            'house_edge_calculated': representative_house_edge,
            'total_pockets': 37 if self.table_type == "EUROPEAN" else 38
        }
        
    def get_minimum_bet_ratio(self, bet_type: "BetType") -> float:
        """
        Get the minimum bet ratio for a specific bet type.
        
        Args:
            bet_type: The type of bet
            
        Returns:
            Minimum bet ratio (1.0 or higher, representing multiples of table minimum)
        """
        bet_type_str = bet_type.value if hasattr(bet_type, 'value') else str(bet_type)
        
        if bet_type_str in self.minimum_bet_ratios:
            return self.minimum_bet_ratios[bet_type_str]
        elif 'global' in self.minimum_bet_ratios:
            return self.minimum_bet_ratios['global']
        else:
            return 1.0  # Default to 100% of table minimum

    def get_maximum_bet_ratio(self, bet_type: "BetType") -> float:
        """
        Get the maximum bet ratio for a specific bet type.
        
        Args:
            bet_type: The type of bet
            
        Returns:
            Maximum bet ratio (0.0 to 1.0 or higher)
        """
        bet_type_str = bet_type.value if hasattr(bet_type, 'value') else str(bet_type)
        
        if bet_type_str in self.maximum_bet_ratios:
            return self.maximum_bet_ratios[bet_type_str]
        elif 'global' in self.maximum_bet_ratios:
            return self.maximum_bet_ratios['global']
        else:
            return 1.0  # Default to 100% of table maximum

    @classmethod
    def create_default_config(cls, config_path: str) -> None:
        """
        Create a default configuration file.
        
        Args:
            config_path: Path where to create the configuration file
        """
        default_config = {
            'payout_ratios': {
                'straight_up': 35,
                'split': 17,
                'street': 11,
                'corner': 8,
                'six_line': 5,
                'red': 1,
                'black': 1,
                'odd': 1,
                'even': 1,
                'high': 1,
                'low': 1,
                'first_dozen': 2,
                'second_dozen': 2,
                'third_dozen': 2,
                'first_column': 2,
                'second_column': 2,
                'third_column': 2
            },
            'minimum_bet_ratios': {
                'global': 1.0,
                'straight_up': 1.0,
                'outside_bets': 5.0  # Higher minimum for outside bets
            },
            'maximum_bet_ratios': {
                'global': 1.0,
                'straight_up': 0.5,
                'outside_bets': 1.0
            },
            # Note: house_edge is now calculated automatically
            'table_limits': {
                'AMERICAN': {
                    'minimum_bet': 1,
                    'maximum_bet': 1000000,
                    'maximum_total_bet': 10000000
                },
                'EUROPEAN': {
                    'minimum_bet': 1,
                    'maximum_bet': 1000000,
                    'maximum_total_bet': 10000000
                }
            }
        }
        
        # Ensure directory exists
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as file:
            yaml.dump(default_config, file, default_flow_style=False, sort_keys=False)
            
    def __str__(self) -> str:
        """Return a string representation of the betting rules."""
        return f"BettingRules(table_type={self.table_type}, min_bet={self.get_table_minimum()}, max_bet={self.get_table_maximum()})"
        
    def __repr__(self) -> str:
        """Return a detailed string representation of the betting rules."""
        return f"BettingRules(config_path='{self.config_path}', table_type='{self.table_type}')" 