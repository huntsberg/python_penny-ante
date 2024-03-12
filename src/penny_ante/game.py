from penny_ante.wheel import Wheel

class Game:
    def __init__(self, table_type) -> object:
        if table_type == None:
            raise Exception('Table type must be defined when creating the game.')
        self.wheel = Wheel(wheel_type = table_type)
        self.current_space = None

    def spin_wheel(self):
        self.wheel.spin()
        self.current_space = self.wheel.current_space
    
def spin_wheel():
    my_game = Game(table_type = 'AMERICAN')
    my_game.spin_wheel()
    print(my_game.current_space.value)