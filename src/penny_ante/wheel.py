import os

from penny_ante.space import Space

class Wheel:
    # Does this make a difference - probably not.
    random_size = 6

    def __init__(self, wheel_type):
        if wheel_type == 'AMERICAN':
            self.type = 'AMERICAN'           
        elif wheel_type == 'EUROPEAN':
            self.type = 'EUROPEAN'
        else:
            raise Exception('Wheel type must be defined when creating the wheel.')
        self.spaces = self.__intitialize_wheel()
        self.current_space = None
    
    def __intitialize_wheel(self) -> bool:
        wheel_spaces = []
        values = []
        colors = []
        if self.type == 'AMERICAN':
            values = [
                "0",28,9,26,30,11,7,20,32,17,5,22,34,15,3,24,36,13,1, "00",27,10,25,29,12,8,19,31,18,6,21,33,16,4,23,35,14,2
            ]
            colors = ['RED', 'BLACK']

        elif self.type == 'EUROPEAN':
            values = [
                "0",32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26
            ]
            colors = ['BLACK', 'RED']

        colors.append("GREEN")

        for location, value in enumerate(values):
            self.__set_space(wheel_spaces = wheel_spaces, colors = colors, location = location, value = str(value))

        return wheel_spaces
    
    def __set_space(self, wheel_spaces, colors, location, value):
        
        new_space = Space (value = str(value))
        new_space.wheel_location = location
        if value in ["0", "00"]:
            new_space.color = colors[2]
        else:
            new_space.color = colors[location%2]
        wheel_spaces.append(new_space)


        
    def spin(self) -> bool:
        # Get *self.random_size* number of bytes from the ether and convert them to an int
        # Get the largest random_size bytes and then calculate a percentage.
        # Multiply the percentage by the spaces on the wheel and round to the nearest space.
        # Look up that space in the wheel array and that's the winner.
        # This seems pretty random...

        # Random integer
        random_bytes = os.urandom(self.random_size)
        rand_val = int.from_bytes(random_bytes, "big")

        # Max Integer
        max_bytes = bytes([int('0xFF',16)]) * self.random_size
        max_value = int.from_bytes(max_bytes, "big")

        self.current_space =  self.spaces[(round((rand_val/max_value)*len(self.spaces))) - 1]

        return True

