class Space:
    def __init__(self, value):
        if value == None:
            raise Exception("To instantiate a space, a value is required.")
        self.value = str(value)
        self.color = None
        self.wheel_location = None
        self.layout_row = None
        self.layout_column = None