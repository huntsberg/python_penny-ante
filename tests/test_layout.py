import unittest

from .context import penny_ante
from penny_ante.layout import Layout
from penny_ante.wheel import Wheel

class TestLayout(unittest.TestCase):
    # Require the wheel type or throw an exception
    def test_throw_exception_if_wheel_is_not_set(self):
        with self.assertRaises(Exception):
            result = Layout()

    def test_set_layout_american(self):
        test_wheel = Wheel(wheel_type = 'AMERICAN')
        test_layout = Layout(wheel = test_wheel)
        result = test_layout.type
        self.assertEqual(result, 'AMERICAN')

    def test_set_layout_european(self):
        test_wheel = Wheel(wheel_type = 'EUROPEAN')
        test_layout = Layout(wheel = test_wheel)
        result = test_layout.type
        self.assertEqual(result, 'EUROPEAN')

    def test_spot_check_layout_spaces(self):
        test_wheel = Wheel(wheel_type = 'AMERICAN')
        test_layout = Layout(wheel = test_wheel)
        self.assertEqual(test_layout.layout[0][0].value, '0')
        self.assertEqual(test_layout.layout[1][0].value, '00')
        self.assertEqual(test_layout.layout[0][1].value, '1')
        self.assertEqual(test_layout.layout[1][1].value, '2')
        self.assertEqual(test_layout.layout[2][1].value, '3')
        self.assertEqual(test_layout.layout[2][12].value, '36')
  

    def test_spot_check_lookup_spaces(self):
        test_wheel = Wheel(wheel_type = 'AMERICAN')
        test_layout = Layout(wheel = test_wheel)
        print(test_layout.lookup["0"])
        self.assertEqual(test_layout.lookup["0"], [0,0])
        self.assertEqual(test_layout.lookup["00"], [1,0])
        self.assertEqual(test_layout.lookup["1"], [0,1])
        self.assertEqual(test_layout.lookup["2"], [1,1])
        self.assertEqual(test_layout.lookup["3"], [2,1])
        self.assertEqual(test_layout.lookup["36"], [2,12])

if __name__ == '__main__':
    unittest.main()