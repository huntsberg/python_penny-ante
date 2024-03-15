from  penny_ante.chips import Chips

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.chips = None

    def buy_chips(self, count, value = 1):
        if self.chips == None:
            self.chips = Chips(value = value)
        self.chips.add_chips(count = count)

    