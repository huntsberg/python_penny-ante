from typing import Optional, Dict
from penny_ante.wheel import Wheel
from penny_ante.player import Player


class Game:
    """
    Represents a roulette game with wheel, players, and game state management.

    This class manages the overall game state including the roulette wheel,
    players, and current game position. It supports both American and European
    roulette wheel types.

    Attributes:
        wheel (Wheel): The roulette wheel used in the game
        current_space (Optional[Space]): The current space the ball landed on
        players (Dict[str, Player]): Dictionary of players keyed by name
    """

    def __init__(self, table_type: Optional[str]) -> None:
        """
        Initialize a new game with the specified table type.

        Args:
            table_type: The type of roulette table ('AMERICAN' or 'EUROPEAN')

        Raises:
            Exception: If table_type is None or not specified
        """
        if table_type is None:
            raise Exception("Table type must be defined when creating the game.")
        self.wheel = Wheel(wheel_type=table_type)
        self.current_space = None
        self.players: Dict[str, Player] = {}

    def spin_wheel(self) -> None:
        """
        Spin the roulette wheel and update the current space.

        This method triggers the wheel to spin and sets the current_space
        to the result of the spin.
        """
        self.wheel.spin()
        self.current_space = self.wheel.current_space

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
    print(my_game.current_space.value)
