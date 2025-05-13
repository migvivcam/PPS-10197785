import unittest
from calculadora import Calculadora

class TestCalculadora(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_multiplicar(self):
        self.assertEqual(self.calc.multiplicar(3, 4), 12)
        self.assertEqual(self.calc.multiplicar(-1, 5), -5)
        self.assertEqual(self.calc.multiplicar(0, 10), 0)

if __name__ == "__main__":
    unittest.main()
