from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from penny_ante.table import Table


class Croupier:
    """
    Represents a croupier who manages the roulette game operations.

    The croupier handles the mechanical aspects of the game including
    spinning the wheel, managing bets, and payouts.

    Attributes:
        table (Table): The roulette table being managed
    """

    def __init__(self, table: "Table") -> None:
        """
        Initialize a new croupier.

        Args:
            table: The roulette table to manage
        """
        self.table = table

    def spin_wheel(self) -> None:
        """Spin the roulette wheel on the table."""
        self.table.spin_wheel()

    def sweep_bets(self) -> None:
        """Sweep losing bets from the table (placeholder implementation)."""
        pass

    def payout_bets(self) -> None:
        """Pay out winning bets (placeholder implementation)."""
        pass

    def clear_dolly(self) -> None:
        """Clear the dolly marker from the table (placeholder implementation)."""
        pass
