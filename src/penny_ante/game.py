from penny_ante.wheel import Wheel
from penny_ante.player import Player

class Game:
    def __init__(self, table_type) -> object:
        if table_type == None:
            raise Exception('Table type must be defined when creating the game.')
        self.wheel = Wheel(wheel_type = table_type)
        self.current_space = None
        self.players = dict()

    def spin_wheel(self):
        self.wheel.spin()
        self.current_space = self.wheel.current_space
    
    def add_player(self, player_name) -> bool:
        if player_name in self.players:
            raise Exception("Multiple plaers of the same name are not allowed.")
        
        self.players[player_name] = Player(name = player_name)
        return True

    def buy_chips(self, player_name, value = None, count = 0) -> bool:
        return True


def spin_wheel():
    my_game = Game(table_type = 'AMERICAN')
    my_game.spin_wheel()
    print(my_game.current_space.value)