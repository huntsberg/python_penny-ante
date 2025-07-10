from typing import Union, Optional


class Space:
    """
    Represents a single space on a roulette wheel.

    Each space has a value (the number or symbol) and various attributes
    that get set during wheel initialization, including position, color,
    and layout coordinates.

    Attributes:
        value (str): The value displayed on this space (e.g., "0", "00", "1"-"36")
        color (Optional[str]): The color of this space ('RED', 'BLACK', or 'GREEN')
        wheel_location (Optional[int]): The position of this space on the wheel
        layout_row (Optional[int]): The row position in the betting layout
        layout_column (Optional[int]): The column position in the betting layout
    """

    def __init__(self, value: Union[str, int]) -> None:
        """
        Initialize a new roulette wheel space.

        Args:
            value: The value displayed on this space (number or symbol)

        Raises:
            Exception: If value is None
        """
        if value is None:
            raise Exception("To instantiate a space, a value is required.")
        self.value = str(value)
        self.color: Optional[str] = None
        self.wheel_location: Optional[int] = None
        self.layout_row: Optional[int] = None
        self.layout_column: Optional[int] = None
