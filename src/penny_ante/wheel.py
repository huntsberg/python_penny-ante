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
        if self.type == "AMERICAN":
            return self.__create_american_wheel()
        elif self.type == "EUROPEAN":
            return self.__create_european_wheel()
        return []

    def __create_american_wheel(self) -> List[Space]:
        """
        Create an American roulette wheel with 38 spaces (0, 00, 1-36).

        American wheels have both 0 and 00 as green house spaces, with
        numbers 1-36 alternating between red and black colors based on
        traditional roulette wheel layouts.

        Returns:
            List[Space]: List of 38 spaces representing the American wheel
        """
        wheel_spaces = []
        location = 0
        values = [
            [28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1],
            [27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2],
        ]
        house_values = ["0", "00"]
        colors = ["RED", "BLACK"]
        wheel_spaces.append(
            Space(location=location, value=str(house_values[0]), color="GREEN")
        )
        location += 1

        for value in values[0]:
            wheel_spaces.append(
                Space(location=location, value=str(value), color=colors[location % 2])
            )
            location += 1

        wheel_spaces.append(
            Space(location=location, value=str(house_values[1]), color="GREEN")
        )
        location += 1

        for value in values[1]:
            wheel_spaces.append(
                Space(location=location, value=str(value), color=colors[location % 2])
            )
            location += 1

        return wheel_spaces

    def __create_european_wheel(self) -> List[Space]:
        """
        Create a European roulette wheel with 37 spaces (0, 1-36).

        European wheels have only 0 as the green house space, with
        numbers 1-36 alternating between red and black colors based on
        traditional roulette wheel layouts.

        Returns:
            List[Space]: List of 37 spaces representing the European wheel
        """
        wheel_spaces = []
        location = 0
        values = [
            [
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
        ]
        house_values = ["0"]
        colors = ["BLACK", "RED"]
        wheel_spaces.append(
            Space(location=location, value=str(house_values[0]), color="GREEN")
        )
        location += 1
        for set in values:
            for value in set:
                wheel_spaces.append(
                    Space(
                        location=location, value=str(value), color=colors[location % 2]
                    )
                )
                location += 1

        return wheel_spaces

    def spin(self) -> bool:
        """
        Spin the roulette wheel and determine where the ball lands.

        Uses cryptographically secure random number generation (os.urandom)
        to fairly determine the landing space. The random value is normalized
        to select an index within the wheel's spaces, with bounds checking
        to ensure a valid space is always selected.

        Returns:
            bool: True if the spin was successful

        Side Effects:
            Sets self.current_space to the space where the ball landed
        """
        # Get *self.random_size* number of bytes from the ether and convert
        # them to an int. Get the largest random_size bytes and then calculate
        # a percentage. Multiply the percentage by the spaces on the wheel and
        # round to the nearest space. Look up that space in the wheel array
        # and that's the winner. This seems pretty random...

        # Random integer
        random_bytes = os.urandom(self.random_size)
        rand_val = int.from_bytes(random_bytes, "big")

        # Max Integer
        max_bytes = bytes([int("0xFF", 16)]) * self.random_size
        max_value = int.from_bytes(max_bytes, "big")

        # Calculate index and ensure it's within bounds
        index = round((rand_val / max_value) * len(self.spaces))
        index = max(0, min(index, len(self.spaces) - 1))
        self.current_space = self.spaces[index]

        return True
