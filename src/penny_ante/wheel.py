import os
from typing import List, Optional

from penny_ante.space import Space


class Wheel:
    """
    Represents a roulette wheel with spaces and spinning functionality.

    This class implements both American (38 spaces) and European (37 spaces)
    roulette wheels. It uses cryptographically secure random number generation
    for fair wheel spins.

    Attributes:
        random_size (int): Number of random bytes to use for spinning (class variable)
        type (str): The type of wheel ('AMERICAN' or 'EUROPEAN')
        spaces (List[Space]): List of all spaces on the wheel
        current_space (Optional[Space]): The space where the ball currently rests
    """

    # Does this make a difference - probably not.
    random_size = 6

    def __init__(self, wheel_type: str) -> None:
        """
        Initialize a roulette wheel of the specified type.

        Args:
            wheel_type: The type of wheel to create ('AMERICAN' or 'EUROPEAN')

        Raises:
            Exception: If wheel_type is not 'AMERICAN' or 'EUROPEAN'
        """
        if wheel_type == "AMERICAN":
            self.type = "AMERICAN"
        elif wheel_type == "EUROPEAN":
            self.type = "EUROPEAN"
        else:
            raise Exception("Wheel type must be defined when creating the wheel.")
        self.spaces = self.__initialize_wheel()
        self.current_space: Optional[Space] = None

    def __initialize_wheel(self) -> List[Space]:
        """
        Initialize the wheel spaces based on the wheel type.

        Returns:
            List[Space]: List of initialized spaces for the wheel
        """
        wheel_spaces = []
        values = []
        colors = []

        if self.type == "AMERICAN":
            values = [
                "0",
                28,
                9,
                26,
                30,
                11,
                7,
                20,
                32,
                17,
                5,
                22,
                34,
                15,
                3,
                24,
                36,
                13,
                1,
                "00",
                27,
                10,
                25,
                29,
                12,
                8,
                19,
                31,
                18,
                6,
                21,
                33,
                16,
                4,
                23,
                35,
                14,
                2,
            ]
            colors = ["RED", "BLACK"]

        elif self.type == "EUROPEAN":
            values = [
                "0",
                32,
                15,
                19,
                4,
                21,
                2,
                25,
                17,
                34,
                6,
                27,
                13,
                36,
                11,
                30,
                8,
                23,
                10,
                5,
                24,
                16,
                33,
                1,
                20,
                14,
                31,
                9,
                22,
                18,
                29,
                7,
                28,
                12,
                35,
                3,
                26,
            ]
            colors = ["BLACK", "RED"]

        colors.append("GREEN")

        for location, value in enumerate(values):
            self.__set_space(
                wheel_spaces=wheel_spaces,
                colors=colors,
                location=location,
                value=str(value),
            )

        return wheel_spaces

    def __set_space(
        self, wheel_spaces: List[Space], colors: List[str], location: int, value: str
    ) -> None:
        """
        Create and add a space to the wheel.

        Args:
            wheel_spaces: List to add the new space to
            colors: List of available colors
            location: Position on the wheel
            value: Value of the space
        """
        new_space = Space(value=str(value))
        new_space.wheel_location = location
        if value in ["0", "00"]:
            new_space.color = colors[2]
        else:
            new_space.color = colors[location % 2]
        wheel_spaces.append(new_space)

    def spin(self) -> bool:
        """
        Spin the roulette wheel and determine where the ball lands.

        Uses cryptographically secure random number generation to select
        a space on the wheel. The result is stored in self.current_space.

        Returns:
            bool: True if the spin was successful

        Raises:
            Exception: If the wheel has no spaces or if random generation fails
        """
        if not self.spaces:
            raise Exception("Cannot spin wheel with no spaces")

        # Use cryptographically secure random number generation
        random_bytes = os.urandom(self.random_size)
        random_int = int.from_bytes(random_bytes, byteorder="big")

        # Ensure we have a valid index
        if len(self.spaces) == 0:
            raise Exception("Wheel has no spaces")

        index = random_int % len(self.spaces)
        self.current_space = self.spaces[index]
        return True
