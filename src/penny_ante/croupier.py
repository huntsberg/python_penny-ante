from penny_ante.chips import Chips
from penny_ante.space import Space
from penny_ante.table import Table

class Croupier:
    def __init__(self, table) -> None:
        self.table = table

    def spin_wheel(self):
        self.table.spin_wheel()

    def sweep_bets(self):
        pass

    def payout_bets(self):
        pass

    def clear_dolly(self):
        pass
