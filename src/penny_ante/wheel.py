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
        if self.type == 'AMERICAN':
            return self.__create_american_wheel()
        elif self.type == 'EUROPEAN':
            return self.__create_european_wheel()
        return True

    def __create_american_wheel(self) -> list:
        wheel_spaces = []
        location = 0
        values = [
            [28,9,26,30,11,7,20,32,17,5,22,34,15,3,24,36,13,1],
            [27,10,25,29,12,8,19,31,18,6,21,33,16,4,23,35,14,2]
        ]
        house_values = ["0", "00"]
        colors = ['RED','BLACK']
        wheel_spaces.append(Space(location = location, value = str(house_values[0]), color = 'GREEN') )
        location += 1

        for value in values[0]:
            wheel_spaces.append( Space( location = location, value = str(value), color = colors[location%2] ) )
            location += 1

        wheel_spaces.append(Space(location = location, value = str(house_values[1]), color = 'GREEN') )
        location += 1

        for value in values[1]:
            wheel_spaces.append( Space( location = location, value = str(value), color = colors[location%2] ) )
            location += 1

        return wheel_spaces

    def __create_european_wheel(self) -> list:
        wheel_spaces = []
        location = 0
        values = [
            [32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]
        ]   
        house_values = ["0"] 
        colors = ['BLACK', 'RED']
        wheel_spaces.append(Space(location = location, value = str(house_values[0]), color = 'GREEN') )
        location += 1
        for set in values:
            for value in set:
                wheel_spaces.append( Space( location = location, value = str(value), color = colors[location%2] ) )
                location += 1

        return wheel_spaces

        
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

