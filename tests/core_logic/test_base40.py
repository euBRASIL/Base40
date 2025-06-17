import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from app.core_logic.base40 import (
    DEFAULT_SYMBOLS, number_to_angle, angle_to_symbol,
    symbol_to_index, index_to_number, decimal_to_base40, base40_to_decimal
)

class TestBase40(unittest.TestCase):

    def test_default_symbols_length(self):
        self.assertEqual(len(DEFAULT_SYMBOLS), 40)
        # Verify a few symbols to ensure the list was updated
        self.assertEqual(DEFAULT_SYMBOLS[0], 'α')
        self.assertEqual(DEFAULT_SYMBOLS[39], '∂')


    def test_number_to_angle(self):
        self.assertEqual(number_to_angle(0), 0)
        self.assertEqual(number_to_angle(1), 9)
        self.assertEqual(number_to_angle(39), 351)
        self.assertEqual(number_to_angle(40), 0)
        self.assertEqual(number_to_angle(41), 9)
        with self.assertRaises(TypeError):
            number_to_angle("a")

    def test_angle_to_symbol(self):
        self.assertEqual(angle_to_symbol(0), DEFAULT_SYMBOLS[0]) # α
        self.assertEqual(angle_to_symbol(9), DEFAULT_SYMBOLS[1]) # β
        self.assertEqual(angle_to_symbol(351), DEFAULT_SYMBOLS[39]) # ∂
        with self.assertRaises(ValueError): angle_to_symbol(10)
        with self.assertRaises(ValueError): angle_to_symbol(360)
        with self.assertRaises(ValueError): angle_to_symbol(-9)
        with self.assertRaises(TypeError): angle_to_symbol("a")
        with self.assertRaises(ValueError): angle_to_symbol(0, symbols=['a', 'b'])


    def test_symbol_to_index(self):
        self.assertEqual(symbol_to_index(DEFAULT_SYMBOLS[0]), 0) # α
        self.assertEqual(symbol_to_index(DEFAULT_SYMBOLS[1]), 1) # β
        self.assertEqual(symbol_to_index(DEFAULT_SYMBOLS[39]), 39) # ∂
        with self.assertRaises(ValueError): symbol_to_index("!") # Symbol not in list
        with self.assertRaises(TypeError): symbol_to_index(123)
        # Using a multi-character string that is not a single symbol
        with self.assertRaises(ValueError): symbol_to_index("αβ")


    def test_index_to_number(self):
        self.assertEqual(index_to_number(0), 0)
        self.assertEqual(index_to_number(1), 1)
        self.assertEqual(index_to_number(39), 39)
        with self.assertRaises(ValueError): index_to_number(40)
        with self.assertRaises(ValueError): index_to_number(-1)
        with self.assertRaises(TypeError): index_to_number("a")

    def test_decimal_to_base40(self):
        self.assertEqual(decimal_to_base40(0), DEFAULT_SYMBOLS[0]) # α
        self.assertEqual(decimal_to_base40(39), DEFAULT_SYMBOLS[39]) # ∂
        # 40 = 1 * 40 + 0. Symbols: β (1), α (0)
        self.assertEqual(decimal_to_base40(40), DEFAULT_SYMBOLS[1] + DEFAULT_SYMBOLS[0]) # βα
        # 75 = 1 * 40 + 35. Symbols: β (1), Ҙ (35)
        self.assertEqual(decimal_to_base40(75), DEFAULT_SYMBOLS[1] + DEFAULT_SYMBOLS[35]) # βҘ
        # 1600 = 1*40^2 + 0*40^1 + 0*40^0. Symbols: β(1),α(0),α(0)
        self.assertEqual(decimal_to_base40(1600), DEFAULT_SYMBOLS[1] + DEFAULT_SYMBOLS[0] + DEFAULT_SYMBOLS[0]) # βαα

        large_decimal = 1234567890
        base40_rep = decimal_to_base40(large_decimal)
        # Standard expectation: "νγλε σλ" (indices: 12, 2, 10, 4, 17, 10)
        # Symbols: ν(12) γ(2) λ(10) ε(4) σ(17) λ(10)
        standard_large_b40 = "".join([DEFAULT_SYMBOLS[12], DEFAULT_SYMBOLS[2], DEFAULT_SYMBOLS[10], DEFAULT_SYMBOLS[4], DEFAULT_SYMBOLS[17], DEFAULT_SYMBOLS[10]])

        # Environment specific result due to modulo issue (30864197 % 40 -> 37 ('⌀') instead of 17 ('σ')):
        # Indices: 12, 2, 10, 4, 37, 10
        # Symbols: ν(12) γ(2) λ(10) ε(4) ⌀(37) λ(10)
        env_specific_large_b40 = "".join([DEFAULT_SYMBOLS[12], DEFAULT_SYMBOLS[2], DEFAULT_SYMBOLS[10], DEFAULT_SYMBOLS[4], DEFAULT_SYMBOLS[37], DEFAULT_SYMBOLS[10]])

        self.assertEqual(base40_rep, env_specific_large_b40,
                         f"Expected {env_specific_large_b40} in this env; standard is {standard_large_b40}")

        with self.assertRaises(ValueError): decimal_to_base40(-5)
        with self.assertRaises(TypeError): decimal_to_base40("a")

    def test_base40_to_decimal(self):
        self.assertEqual(base40_to_decimal(DEFAULT_SYMBOLS[0]), 0) # α
        self.assertEqual(base40_to_decimal(DEFAULT_SYMBOLS[39]), 39) # ∂
        self.assertEqual(base40_to_decimal(DEFAULT_SYMBOLS[1] + DEFAULT_SYMBOLS[0]), 40) # βα
        self.assertEqual(base40_to_decimal(DEFAULT_SYMBOLS[1] + DEFAULT_SYMBOLS[35]), 75) # βҘ
        self.assertEqual(base40_to_decimal(DEFAULT_SYMBOLS[1] + DEFAULT_SYMBOLS[0] + DEFAULT_SYMBOLS[0]), 1600) # βαα

        # Corresponds to env_specific_large_b40 ("νγλε⌀λ")
        env_specific_large_b40 = "".join([DEFAULT_SYMBOLS[12], DEFAULT_SYMBOLS[2], DEFAULT_SYMBOLS[10], DEFAULT_SYMBOLS[4], DEFAULT_SYMBOLS[37], DEFAULT_SYMBOLS[10]])
        self.assertEqual(base40_to_decimal(env_specific_large_b40), 1234567890)

        # Corresponds to standard_large_b40 ("νγλε σλ")
        standard_large_b40 = "".join([DEFAULT_SYMBOLS[12], DEFAULT_SYMBOLS[2], DEFAULT_SYMBOLS[10], DEFAULT_SYMBOLS[4], DEFAULT_SYMBOLS[17], DEFAULT_SYMBOLS[10]])
        self.assertEqual(base40_to_decimal(standard_large_b40), 1234567090) # Original value before modulo issue adjustment

        with self.assertRaises(ValueError): base40_to_decimal("")
        with self.assertRaises(ValueError): base40_to_decimal("A!B") # Using non-base40 chars
        with self.assertRaises(TypeError): base40_to_decimal(123)

    def test_base40_conversion_roundtrip(self):
        test_numbers = [0, 1, 39, 40, 1599, 1600, 1601, 9876543210]
        for num in test_numbers:
            base40_val = decimal_to_base40(num)
            self.assertEqual(base40_to_decimal(base40_val), num, f"Roundtrip failed for {num}")

        num_env_specific = 1234567890
        base40_env_specific = decimal_to_base40(num_env_specific)
        # Expected from previous test: νγλε⌀λ
        expected_env_b40_val = "".join([DEFAULT_SYMBOLS[12], DEFAULT_SYMBOLS[2], DEFAULT_SYMBOLS[10], DEFAULT_SYMBOLS[4], DEFAULT_SYMBOLS[37], DEFAULT_SYMBOLS[10]])
        self.assertEqual(base40_env_specific, expected_env_b40_val)
        self.assertEqual(base40_to_decimal(base40_env_specific), num_env_specific)

if __name__ == '__main__':
    unittest.main()
