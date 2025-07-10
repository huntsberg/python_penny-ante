from typing import Optional
from penny_ante.chips import Chips


class Player:
    """
    Represents a player in the roulette game.

    Each player has a name and can have chips for betting. Players can buy
    chips and manage their chip collections for placing bets.

    Attributes:
        name (str): The player's name
        chips (Optional[Chips]): The player's chip collection
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a new player with the given name.

        Args:
            name: The player's name (must be unique within a game)
        """
        self.name = name
        self.chips: Optional[Chips] = None

    def buy_chips(self, count: int, value: int = 1) -> None:
        """
        Buy chips for this player.

        If the player doesn't have any chips yet, creates a new chip collection
        with the specified value. If they already have chips, adds to the existing
        collection.

        Args:
            count: The number of chips to buy
            value: The value of each chip (default: 1)

        Raises:
            Exception: If trying to buy chips with a different value than existing chips
        """
        if self.chips is None:
            self.chips = Chips(value=value)
        self.chips.change_chips(count=count)
