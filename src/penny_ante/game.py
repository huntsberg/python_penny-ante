from penny_ante.table import Table
from penny_ante.croupier import Croupier
from penny_ante.player import Player


class Game:
    def __init__(self, table_type) -> object:
        if table_type == None:
            raise Exception('Table type must be defined when creating the game.')
        self.table = Table(table_type = table_type)
        self.croupier = Croupier(table = self.table)
        self.players = dict()

    def spin_wheel(self):
        self.croupier.spin_wheel()
    
    def add_player(self, player_name) -> bool:
        if player_name in self.players:
            raise Exception("Multiple plaers of the same name are not allowed.")
        
        self.players[player_name] = Player(name = player_name)
        return True

def spin_wheel():
    my_game = Game(table_type = 'AMERICAN')
    my_game.spin_wheel()
    print(my_game.current_space.value)