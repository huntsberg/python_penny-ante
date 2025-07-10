from typing import Union


class Space:
    """
    Represents a single space on a roulette wheel.

    Each space has a location (position on the wheel), a value (the number
    or symbol), and a color (RED, BLACK, or GREEN for house spaces).

    Attributes:
        location (int): The position of this space on the wheel
        value (str): The value displayed on this space (e.g., "0", "00", "1"-"36")
        color (str): The color of this space ('RED', 'BLACK', or 'GREEN')
    """

    def __init__(self, location: int, value: Union[str, int], color: str) -> None:
        """
        Initialize a new roulette wheel space.

        Args:
            location: The position of this space on the wheel (0-based index)
            value: The value displayed on this space (number or symbol)
            color: The color of this space ('RED', 'BLACK', or 'GREEN')

        Raises:
            Exception: If any of the required parameters are None
        """
        if location is None or value is None or color is None:
            raise Exception(
                "To instantiate a space, location, number, and " "color are required."
            )
        self.location = location
        self.value = str(value)
        self.color = color
