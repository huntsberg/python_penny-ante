import os
from typing import List, Dict, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from penny_ante.space import Space
    from penny_ante.wheel import Wheel


class Layout:
    """
    Represents the betting layout for a roulette table.

    The layout manages the grid of betting positions and provides methods
    to find specific spaces for placing bets.

    Attributes:
        wheel (Wheel): The associated roulette wheel
        type (str): The type of layout ('AMERICAN' or 'EUROPEAN')
        layout (List[List]): The 2D grid representing the betting layout
        lookup (Dict[str, List[int]]): Lookup table for finding positions
        dolly (Optional): The dolly marker position
    """

    def __init__(self, wheel: "Wheel") -> None:
        """
        Initialize a new betting layout.

        Args:
            wheel: The roulette wheel to create layout for
        """
        self.wheel = wheel
        self.type = wheel.type

        # Initialize the layout grid
        value_lookup: Dict[str, List[int]] = {}
        layout: List[List[Union[int, str, "Space"]]] = [[0 for _ in range(13)] for _ in range(3)]

        if self.wheel.type == "AMERICAN":
            # Set up American layout with 0 and 00
            value_lookup["0"] = [0, 0]
            value_lookup["00"] = [1, 0]
            
        elif self.wheel.type == "EUROPEAN":
            # Set up European layout with only 0
            value_lookup["0"] = [0, 0]

        # Set up the numbered spaces 1-36
        # Numbers 1-36 are arranged in 3 rows and 12 columns
        # Row 0: 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34
        # Row 1: 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35  
        # Row 2: 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36
        
        for column in range(1, 13):  # Columns 1-12
            for row in range(3):  # Rows 0-2
                value = (column - 1) * 3 + row + 1
                value_lookup[str(value)] = [row, column]

        # Now replace the layout positions with the actual space objects
        for space in self.wheel.spaces:
            if str(space.value) in value_lookup:
                lookup = value_lookup[str(space.value)]
                space.layout_row = lookup[0]
                space.layout_column = lookup[1]
                layout[space.layout_row][space.layout_column] = space

        self.layout = layout
        self.lookup = value_lookup
        self.dolly: Optional[object] = None

    def find_space(self, space_value: str) -> "Space":
        """
        Find a space on the layout by its value.

        Args:
            space_value: The value of the space to find

        Returns:
            Space: The space object at the specified position
        """
        coords = self.lookup[space_value]
        space = self.layout[coords[0]][coords[1]]
        # After initialization, these positions should contain Space objects
        from penny_ante.space import Space
        assert isinstance(space, Space)
        return space
