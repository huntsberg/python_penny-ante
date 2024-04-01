import os

from penny_ante.space import Space
from penny_ante.wheel import Wheel

class Layout:
    def __init__(self, wheel: Wheel):
        self.wheel = wheel
        self.type = wheel.type

        # Initialize the layout grid
        value_lookup = {}
        layout_by_value = [None] * 3
        layout = [0] * 3 # rows
        for index, row in enumerate(layout):
            layout[index] = [0] * 13

        if self.wheel.type == 'AMERICAN':
            layout[0][0] = '0'
            value_lookup['0'] = [0,0]
            layout[0][1] = '00'
            value_lookup['00'] =[1,0]
            layout[0][2] = 'XX'
            
        elif self.wheel.type == 'EUROPEAN':
            layout[0][0] = '0'
            value_lookup['0'] = [0,0]
            layout[0][1] = 'X0'
            layout[0][2] = 'XX'

        # Set the Values
        value = 1
        for column_index in range (1,13):
            for row_index in range (3):
                layout[row_index][column_index] = value
                value_lookup[str(value)] = [row_index,column_index]
                value += 1

        # Swap the values with the spaces
        for space in self.wheel.spaces:
            lookup = value_lookup[str(space.value)]
            space.layout_row = lookup[0]
            space.layout_column = lookup[1]
            layout[space.layout_row][space.layout_column] = space

        self.layout = layout
        self.lookup = value_lookup
    
        self.dolly = None
    