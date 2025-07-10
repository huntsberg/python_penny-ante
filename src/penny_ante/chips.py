from typing import Optional


class Chips:
    """
    Represents a collection of chips with a specific value.

    This class manages a stack of chips of the same denomination. Once a chip
    value is set, it cannot be changed. Additional chips can only be added if
    they match the existing value.

    Attributes:
        count (int): The number of chips in this collection
        value (Optional[int]): The value of each chip (None until first chips are added)
    """

    def __init__(self, value: Optional[int] = None) -> None:
        """
        Initialize a new chip collection.

        Args:
            value: The value of each chip (optional, can be set later)
        """
        self.count = 0
        self.value = value

    def add_chips(self, count: int, value: Optional[int] = None) -> None:
        """
        Add chips to this collection.

        If this is the first time adding chips and no value was set during
        initialization, the value parameter is required. Once a value is set,
        it cannot be changed.

        Args:
            count: The number of chips to add
            value: The value of each chip (required if not previously set)

        Raises:
            Exception: If chip value is not set and value parameter is None
            Exception: If attempting to change the chip value after it's been set
        """
        if self.value is None:
            if value is None:
                raise Exception(
                    "Chip value must be set when adding chips " "for the first time."
                )
            else:
                self.value = value
        else:
            raise Exception(
                "Chip Value cannot be changed after the chips " "have been established."
            )
        self.count += count
