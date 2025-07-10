from typing import Optional
from penny_ante.layout import Layout
from penny_ante.wheel import Wheel


class Table:
    """
    Represents a roulette table with a wheel and betting layout.

    The table manages the physical components of the roulette game including
    the wheel for spinning and the layout for placing bets.

    Attributes:
        wheel (Wheel): The roulette wheel
        layout (Layout): The betting layout
    """

    def __init__(self, table_type: Optional[str]) -> None:
        """
        Initialize a new roulette table.

        Args:
            table_type: The type of table ('AMERICAN' or 'EUROPEAN')

        Raises:
            Exception: If table_type is None
        """
        if table_type is None:
            raise Exception("Table type must be defined when creating the table.")
        self.wheel = Wheel(wheel_type=table_type)
        self.layout = Layout(wheel=self.wheel)

    def spin_wheel(self) -> None:
        """Spin the roulette wheel."""
        self.wheel.spin()
