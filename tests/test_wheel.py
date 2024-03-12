import unittest

from .context import penny_ante
from penny_ante.wheel import Wheel


class TestWheel(unittest.TestCase):
    # Require the wheel type or throw an exception
    def test_throw_exception_if_wheel_type_is_not_set(self):
        with self.assertRaises(Exception):
            result = Wheel()

    def test_set_wheel_american(self):
        test_wheel = Wheel(wheel_type = 'AMERICAN')
        result = test_wheel.type
        self.assertEqual(result, 'AMERICAN')

    def test_set_wheel_european(self):
        test_wheel = Wheel(wheel_type = 'EUROPEAN')
        result = test_wheel.type
        self.assertEqual(result, 'EUROPEAN')

    def test_european_wheel_spaces_count_is_correct(self):
        test_wheel = Wheel(wheel_type = 'EUROPEAN')
        self.assertEqual(len(test_wheel.spaces), 37)

    def test_spot_check_european_wheel_spaces(self):
        test_wheel = Wheel(wheel_type = 'EUROPEAN')
        self.assertEqual(test_wheel.spaces[0].color, 'GREEN')
        self.assertEqual(test_wheel.spaces[0].value, '0')
        self.assertEqual(test_wheel.spaces[10].color, 'BLACK')
        self.assertEqual(test_wheel.spaces[10].value, '6')
        self.assertEqual(test_wheel.spaces[21].color, 'RED')
        self.assertEqual(test_wheel.spaces[21].value, '16')
        self.assertEqual(test_wheel.spaces[30].color, 'BLACK')
        self.assertEqual(test_wheel.spaces[30].value, '29')        
        self.assertEqual(test_wheel.spaces[36].color, 'BLACK')
        self.assertEqual(test_wheel.spaces[36].value, '26')     

    def test_american_wheel_spaces_count_is_correct(self):
        test_wheel = Wheel(wheel_type = 'AMERICAN')
        self.assertEqual(len(test_wheel.spaces), 38)

    def test_spot_check_american_wheel_spaces(self):
        test_wheel = Wheel(wheel_type = 'AMERICAN')
        self.assertEqual(test_wheel.spaces[0].color, 'GREEN')
        self.assertEqual(test_wheel.spaces[0].value, '0')
        self.assertEqual(test_wheel.spaces[19].color, 'GREEN')
        self.assertEqual(test_wheel.spaces[19].value, '00')
        self.assertEqual(test_wheel.spaces[10].color, 'RED')
        self.assertEqual(test_wheel.spaces[10].value, '5')
        self.assertEqual(test_wheel.spaces[21].color, 'BLACK')
        self.assertEqual(test_wheel.spaces[21].value, '10')
        self.assertEqual(test_wheel.spaces[30].color, 'RED')
        self.assertEqual(test_wheel.spaces[30].value, '21')        
        self.assertEqual(test_wheel.spaces[37].color, 'BLACK')
        self.assertEqual(test_wheel.spaces[37].value, '2')     


    def test_spin(self):
        test_wheel = Wheel(wheel_type = 'AMERICAN')
        test_wheel.spin()
        first_result = test_wheel.current_space.value
        test_wheel.spin()
        second_result = test_wheel.current_space.value
        self.assertNotEqual(first_result, second_result)

if __name__ == '__main__':
    unittest.main()