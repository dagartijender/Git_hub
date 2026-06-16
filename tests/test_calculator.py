import unittest

from src.calculator import add, divide


class CalculatorTests(unittest.TestCase):
    def test_adds_two_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_divides_two_numbers(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero_raises_error(self):
        with self.assertRaises(ValueError):
            divide(10, 0)


if __name__ == "__main__":
    unittest.main()

