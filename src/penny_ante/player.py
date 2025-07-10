from typing import Optional


class Player:
    """
    Represents a player in the roulette game.

    Each player has a name and can have chips for betting. This is a basic
    implementation that can be extended with additional player functionality
    such as betting history, balance tracking, etc.

    Attributes:
        name (str): The player's name
        chips (Optional[object]): The player's chips (placeholder for future
            implementation)
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a new player with the given name.

        Args:
            name: The player's name (must be unique within a game)
        """
        self.name = name
        self.chips: Optional[object] = None
