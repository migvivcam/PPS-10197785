# test_calculator.py

import unittest
from calculadora import Calculadora

class TestCalculadora(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_multiplicar_enteros(self):
        self.assertEqual(self.calc.multiplicar(3, 4), 12)

    def test_multiplicar_decimales(self):
        self.assertAlmostEqual(self.calc.multiplicar(2.5, 4), 10.0)

    def test_multiplicar_negativos(self):
        self.assertEqual(self.calc.multiplicar(-2, -3), 6)

    def test_multiplicar_cero(self):
        self.assertEqual(self.calc.multiplicar(0, 5), 0)

if __name__ == "__main__":
    unittest.main()
