from typing import Optional, Dict, Any, List
from penny_ante.table import Table
from penny_ante.croupier import Croupier
from penny_ante.player import Player
from penny_ante.betting_rules import BettingRules
from penny_ante.bet import Bet


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

    def __init__(
        self,
        table_type: Optional[str],
        betting_rules_config: Optional[str] = None,
        overlay_rules: Optional[Dict[str, Any]] = None,
    ) -> None:
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
        self.active_bets: List[Bet] = []
        self.betting_open = True

        # Initialize betting rules with table-specific or custom configuration
        self.betting_rules = BettingRules(
            config_path=betting_rules_config,
            table_type=table_type,
            overlay_config=overlay_rules,
        )

    def spin_wheel(self) -> None:
        """
        Spin the roulette wheel via the croupier.

        This method triggers the croupier to spin the wheel and update the
        current game state. Automatically closes betting if it's still open.
        """
        # Close betting if still open
        if self.betting_open:
            validation_result = self.close_betting()
            if not validation_result["valid"]:
                raise ValueError(
                    f"Cannot spin wheel: Invalid bets detected - {validation_result['errors']}"
                )

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

    def place_bet(self, bet: Bet, player_name: Optional[str] = None) -> bool:
        """
        Place a bet on the table with full validation.

        Args:
            bet: The bet to place
            player_name: Optional player name for tracking

        Returns:
            True if bet was successfully placed

        Raises:
            ValueError: If betting is closed or bet is invalid
            Exception: If player doesn't have sufficient chips
        """
        if not self.betting_open:
            raise ValueError("Betting is closed")

        # Validate the bet against betting rules
        if not bet.betting_rules:
            bet.betting_rules = self.betting_rules
            bet._validate_betting_rules()

        # If player is specified, validate they have sufficient chips
        if player_name and player_name in self.players:
            player = self.players[player_name]
            if player.chips and player.chips.count < bet.amount:
                raise Exception(
                    f"Player {player_name} has insufficient chips ({player.chips.count}) for bet amount ({bet.amount})"
                )

        # Validate total bet limits
        current_total = sum(b.amount for b in self.active_bets)
        if current_total + bet.amount > self.betting_rules.get_maximum_total_bet():
            raise ValueError(
                f"Adding this bet would exceed maximum total bet limit of {self.betting_rules.get_maximum_total_bet()}"
            )

        # Add the bet to active bets
        self.active_bets.append(bet)

        # Deduct chips from player if specified
        if player_name and player_name in self.players:
            player = self.players[player_name]
            if player.chips:
                player.chips.change_chips(count=-bet.amount)

        return True

    def validate_all_bets(self) -> Dict[str, Any]:
        """
        Validate all active bets against betting rules.

        Returns:
            Dictionary with validation results
        """
        return self.betting_rules.validate_multiple_bets(self.active_bets)

    def close_betting(self) -> Dict[str, Any]:
        """
        Close betting and perform final validation.

        Returns:
            Dictionary with final validation results
        """
        self.betting_open = False
        validation_result = self.validate_all_bets()

        if not validation_result["valid"]:
            # In a real casino, invalid bets would be returned
            # For now, we'll just mark the validation result
            validation_result["action"] = "invalid_bets_detected"

        return validation_result

    def open_betting(self) -> None:
        """Open betting for a new round."""
        self.betting_open = True
        self.active_bets.clear()

    def get_total_bet_amount(self) -> int:
        """Get the total amount of all active bets."""
        return sum(bet.amount for bet in self.active_bets)

    def get_bet_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all active bets.

        Returns:
            Dictionary with bet summary information
        """
        bet_types = {}
        total_amount = 0

        for bet in self.active_bets:
            bet_type = bet.bet_type.value
            if bet_type not in bet_types:
                bet_types[bet_type] = {"count": 0, "total_amount": 0}
            bet_types[bet_type]["count"] += 1
            bet_types[bet_type]["total_amount"] += bet.amount
            total_amount += bet.amount

        return {
            "total_bets": len(self.active_bets),
            "total_amount": total_amount,
            "bet_types": bet_types,
            "betting_open": self.betting_open,
            "max_total_allowed": self.betting_rules.get_maximum_total_bet(),
        }


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
