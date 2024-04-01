from penny_ante.layout import Layout
from penny_ante.wheel import Wheel


class Table:
    def __init__(self, table_type) -> object:
        if table_type == None:
            raise Exception('Table type must be defined when creating the table.')
        self.wheel = Wheel(wheel_type = table_type)
        self.layout = Layout(wheel = self.wheel)

    def spin_wheel(self):
        self.wheel.spin()
