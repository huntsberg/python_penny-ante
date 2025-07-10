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

    def cash_value(self) -> Optional[int]:
        """
        Calculate the total cash value of all chips in this collection.

        Returns:
            Optional[int]: The total value (count * value) or None if no value is set
        """
        if self.value is None:
            return None
        return self.value * self.count

    def change_chips(
        self,
        count: Optional[int] = None,
        value: Optional[int] = None,
        chips: Optional["Chips"] = None,
    ) -> None:
        """
        Change the number of chips in this collection.

        This method can add/remove chips or merge with another chip collection.
        If merging with another collection, the values must match.

        Args:
            count: The number of chips to add (positive) or remove (negative)
            value: The value of each chip (required if not previously set)
            chips: Another Chips object to merge with this one

        Raises:
            Exception: If chip values don't match when merging
            Exception: If trying to remove more chips than available
            Exception: If chip value is not set and value parameter is None
            Exception: If attempting to change the chip value after it's been set
        """
        if chips is not None:
            if self.value != chips.value:
                raise Exception(
                    "To change chip stacks, the chip values must be the same."
                )
            self.count += chips.count
            return

        if count is not None and self.count + count < 0:
            raise Exception(
                "There are not enough chips available to make the requested chip count change."
            )

        if value is None:
            if self.value is None:
                raise Exception(
                    "Chip value must be set when adding chips for the first time."
                )
        else:
            if self.value is None:
                self.value = value
            else:
                raise Exception(
                    "Chip Value cannot be changed after the chips have been established."
                )

        if count is not None:
            self.count += count

    def add_chips(self, count: int, value: Optional[int] = None) -> None:
        """
        Add chips to this collection (convenience method).

        Args:
            count: The number of chips to add
            value: The value of each chip (required if not previously set)

        Raises:
            Exception: If chip value is not set and value parameter is None
            Exception: If attempting to change the chip value after it's been set
        """
        self.change_chips(count=count, value=value)
