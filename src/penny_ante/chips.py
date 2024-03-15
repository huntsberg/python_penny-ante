class Chips:
    def __init__(self, value = None) -> None:
        self.count = 0
        self.value = value

    def cash_value(self):
         if self.value == None:
            return None
         return self.value*self.count

    def add_chips(self, count = None, value = None, chips = None):
        if chips != None:
            if self.value != chips.value:
                raise Exception("To add chip stacks, the chip values must be the same.")
            self.count += chips.count
            return
        if value == None:
            if self.value == None:
                raise Exception("Chip value must be set when adding chips for the first time.")
        else:
            if self.value == None:
                self.value = value
            else:
                raise Exception("Chip Value cannot be changed after the chips have been established.")
        self.count += count 
        return