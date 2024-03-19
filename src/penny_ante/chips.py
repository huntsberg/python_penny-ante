class Chips:
    def __init__(self, value = None) -> None:
        self.count = 0
        self.value = value

    def cash_value(self):
         if self.value == None:
            return None
         return self.value*self.count

    def change_chips(self, count = None, value = None, chips = None):
        if chips != None:
            if self.value != chips.value:
                raise Exception("To change chip stacks, the chip values must be the same.")
            self.count += chips.count
            return
        
        if self.count + count < 0:
            raise Exception("There are not enough chips available to make the requested chip count change.")

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