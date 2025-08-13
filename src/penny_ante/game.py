from typing import Optional, Dict, Any
from penny_ante.table import Table
from penny_ante.croupier import Croupier
from penny_ante.player import Player
from penny_ante.betting_rules import BettingRules


class Game:
    """
    Represents a roulette game with table, croupier, and player management.

    This class manages the overall game state including the roulette table,
    croupier operations, players, and betting rules. It supports both American 
    and European roulette table types with configurable betting rules.

    Attributes:
        table (Table): The roulette table with wheel and layout
        croupier (Croupier): The croupier managing game operations
        players (Dict[str, Player]): Dictionary of players keyed by name
        betting_rules (BettingRules): The betting rules configuration
    """

    def __init__(self, table_type: Optional[str], betting_rules_config: Optional[str] = None,
                 overlay_rules: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a new game with the specified table type and betting rules.

        Args:
            table_type: The type of roulette table ('AMERICAN' or 'EUROPEAN')
            betting_rules_config: Optional path to custom betting rules YAML file.
                                If None, uses the appropriate default config for table type.
            overlay_rules: Optional dictionary to overlay on top of the base configuration.
                         This allows partial configurations that inherit missing values from defaults.

        Raises:
            Exception: If table_type is None or not specified
        """
        if table_type is None:
            raise Exception("Table type must be defined when creating the game.")
        
        self.table = Table(table_type=table_type)
        self.croupier = Croupier(table=self.table)
        self.players: Dict[str, Player] = {}
        
        # Initialize betting rules with table-specific or custom configuration
        self.betting_rules = BettingRules(
            config_path=betting_rules_config, 
            table_type=table_type,
            overlay_config=overlay_rules
        )

    def spin_wheel(self) -> None:
        """
        Spin the roulette wheel via the croupier.

        This method triggers the croupier to spin the wheel and update the
        current game state.
        """
        self.croupier.spin_wheel()

    @property
    def current_space(self):
        """Get the current space where the ball landed."""
        return self.table.wheel.current_space

    def add_player(self, player_name: str) -> bool:
        """
        Add a new player to the game.

        Args:
            player_name: The name of the player to add

        Returns:
            bool: True if player was successfully added

        Raises:
            Exception: If a player with the same name already exists
        """
        if player_name in self.players:
            raise Exception("Multiple players of the same name are not allowed.")

        self.players[player_name] = Player(name=player_name)
        return True

    def buy_chips(
        self, player_name: str, value: Optional[int] = None, count: int = 0
    ) -> bool:
        """
        Allow a player to buy chips (placeholder implementation).

        Args:
            player_name: The name of the player buying chips
            value: The value of each chip (optional)
            count: The number of chips to buy (default: 0)

        Returns:
            bool: True (placeholder implementation)

        Note:
            This is a placeholder method that currently always returns True.
            Full implementation would handle chip transactions.
        """
        return True


def spin_wheel() -> None:
    """
    Standalone function to spin a wheel once and print the result.

    This function creates a new American roulette game, spins the wheel once,
    and prints the value of the space where the ball landed. Used as a
    command-line entry point.
    """
    my_game = Game(table_type="AMERICAN")
    my_game.spin_wheel()
    if my_game.current_space is not None:
        print(my_game.current_space.value)
