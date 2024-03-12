class Chips:
    def __init__(self, value = None) -> None:
        self.count = 0
        self.value = value


    def add_chips(self, count, value):
            if self.value == None:
                if value == None:
                    raise Exception("Chip value must be set when adding chips for the first time.")
                else:
                    self.value = value
            else:
                raise Exception("Chip Value cannot be changed after the chips have been established.")
            self.count += count 