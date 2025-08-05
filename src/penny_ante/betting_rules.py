import os
import yaml
from typing import Dict, Any, Optional, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from penny_ante.bet import BetType


class BettingRules:
    """
    Manages         betting rules and configuration for roulette games.
    
    This class reads betting rules from YAML configuration files, including
    payout ratios, minimum bets, maximum bet ratios, and other casino-specific
    betting parameters.
    
    Attributes:
        config (Dict[str, Any]): The loaded configuration dictionary
        table_type (str): The type of table ('AMERICAN' or 'EUROPEAN')
        payout_ratios (Dict): Payout ratios for each bet type
        minimum_bets (Dict): Minimum bet amounts for each bet type
        maximum_bet_ratios (Dict): Maximum bet ratios for each bet type
        house_edge (Dict): House edge percentages for each bet type
    """
    
    DEFAULT_CONFIG_PATH = "config/betting_rules.yaml"
    
    def __init__(self, config_path: Optional[str] = None, table_type: str = "AMERICAN") -> None:
        """
        Initialize betting rules from configuration file.
        
        Args:
            config_path: Path to YAML configuration file. If None, uses default.
            table_type: Type of table ('AMERICAN' or 'EUROPEAN')
            
        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ValueError: If configuration is invalid
        """
        self.table_type = table_type
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = self._load_config()
        
        # Extract configuration sections
        self.payout_ratios = self._get_payout_ratios()
        self.minimum_bets = self._get_minimum_bets()
        self.maximum_bet_ratios = self._get_maximum_bet_ratios()
        self.house_edge = self._get_house_edge()
        self.table_limits = self._get_table_limits()
        
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
            
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate that the configuration has all required sections.
        
        Args:
            config: Configuration dictionary to validate
            
        Raises:
            ValueError: If required sections are missing
        """
        required_sections = ['payout_ratios', 'minimum_bets', 'maximum_bet_ratios', 'table_limits']
        missing_sections = [section for section in required_sections if section not in config]
        
        if missing_sections:
            raise ValueError(f"Missing required configuration sections: {missing_sections}")
            
        # Validate table type specific configuration exists
        if self.table_type not in config.get('table_limits', {}):
            raise ValueError(f"No configuration found for table type: {self.table_type}")
            
    def _get_payout_ratios(self) -> Dict[str, int]:
        """Get payout ratios from configuration."""
        return self.config.get('payout_ratios', {})
        
    def _get_minimum_bets(self) -> Dict[str, int]:
        """Get minimum bets from configuration."""
        return self.config.get('minimum_bets', {})
        
    def _get_maximum_bet_ratios(self) -> Dict[str, float]:
        """Get maximum bet ratios from configuration."""
        return self.config.get('maximum_bet_ratios', {})
        
    def _get_house_edge(self) -> Dict[str, float]:
        """Get house edge percentages from configuration."""
        return self.config.get('house_edge', {})
        
    def _get_table_limits(self) -> Dict[str, Any]:
        """Get table-specific limits from configuration."""
        table_config = self.config.get('table_limits', {}).get(self.table_type, {})
        return table_config
        
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
            Minimum bet amount
        """
        bet_type_str = bet_type.value if hasattr(bet_type, 'value') else str(bet_type)
        
        # Return specific minimum or global minimum
        if bet_type_str in self.minimum_bets:
            return self.minimum_bets[bet_type_str]
        elif 'global' in self.minimum_bets:
            return self.minimum_bets['global']
        else:
            return self.table_limits.get('minimum_bet', 1)
            
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
        Get the house edge percentage for a specific bet type.
        
        Args:
            bet_type: The type of bet
            
        Returns:
            House edge as a percentage (e.g., 5.26 for 5.26%)
        """
        bet_type_str = bet_type.value if hasattr(bet_type, 'value') else str(bet_type)
        
        # Return specific house edge or default based on table type
        if bet_type_str in self.house_edge:
            return self.house_edge[bet_type_str]
        else:
            # Default house edges
            if self.table_type == "AMERICAN":
                return 5.26  # Standard American roulette house edge
            else:
                return 2.70  # Standard European roulette house edge
                
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
        return {
            'table_type': self.table_type,
            'minimum_bet': self.get_table_minimum(),
            'maximum_bet': self.get_table_maximum(),
            'maximum_total_bet': self.get_maximum_total_bet(),
            'payout_ratios': self.get_all_payout_ratios(),
            'house_edge_default': 5.26 if self.table_type == "AMERICAN" else 2.70
        }
        
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
            'minimum_bets': {
                'global': 1,
                'straight_up': 1,
                'outside_bets': 5  # Higher minimum for outside bets
            },
            'maximum_bet_ratios': {
                'global': 1.0,
                'straight_up': 0.5,
                'outside_bets': 1.0
            },
            'house_edge': {
                'straight_up': 5.26,
                'outside_bets': 5.26
            },
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