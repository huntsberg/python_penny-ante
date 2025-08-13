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

    def can_afford_bet(self, amount: int) -> bool:
        """
        Check if the player can afford a bet of the given amount.

        Args:
            amount: The bet amount to check

        Returns:
            True if player has sufficient chips, False otherwise
        """
        if self.chips is None:
            return False
        return self.chips.count >= amount

    def get_chip_balance(self) -> int:
        """
        Get the current chip balance for this player.

        Returns:
            Number of chips the player has, or 0 if no chips
        """
        if self.chips is None:
            return 0
        return self.chips.count

    def get_chip_value(self) -> int:
        """
        Get the value of each chip for this player.

        Returns:
            Value per chip, or 0 if no chips
        """
        if self.chips is None:
            return 0
        return self.chips.value

    def get_total_value(self) -> int:
        """
        Get the total monetary value of all chips.

        Returns:
            Total value of all chips (count * value)
        """
        if self.chips is None:
            return 0
        return self.chips.count * self.chips.value
