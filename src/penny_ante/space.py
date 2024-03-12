class Space:
    def __init__(self, location, value, color):
        if location == None or value == None or color == None:
            raise Exception("To instantiate a space, location, number, and color are rquired.")
        self.location = location
        self.value = str(value)
        self.color = color