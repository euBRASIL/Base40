import unittest
import sys
import os

# Add parent directory of 'app' to Python path (i.e., /app directory itself, which is the project root)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.crypto.secp256k1_utils import (
    P, A, B, Gx, Gy, N, POINT_INFINITY,
    inverse_mod, is_on_curve, point_addition, point_doubling, scalar_multiplication
)
from app.core_logic.base40 import number_to_angle, angle_to_symbol, DEFAULT_SYMBOLS

G_POINT = (Gx, Gy)

class TestSECP256K1Utils(unittest.TestCase):

    def test_curve_parameters(self):
        self.assertTrue(is_on_curve(Gx, Gy))

    def test_inverse_mod(self):
        self.assertEqual(inverse_mod(2, 5), 3) # 2*3 = 6 mod 5 = 1
        self.assertEqual(inverse_mod(7, 13), 2) # 7*2 = 14 mod 13 = 1
        with self.assertRaises(ZeroDivisionError):
            inverse_mod(0, 5)

    def test_point_doubling(self):
        p_2G = point_doubling(G_POINT)
        self.assertTrue(is_on_curve(p_2G[0], p_2G[1]))
        # Add known values for 2G if available for a stronger test
        # For now, just check it's on curve and not infinity

    def test_point_addition(self):
        p_2G = point_doubling(G_POINT)
        p_3G = point_addition(G_POINT, p_2G)
        self.assertTrue(is_on_curve(p_3G[0], p_3G[1]))

        # G + (-G) = Infinity (approximate -G by (Gx, -Gy % P))
        G_minus_approx = (Gx, (P - Gy) % P) # y_neg = -y mod P
        self.assertEqual(point_addition(G_POINT, G_minus_approx), POINT_INFINITY)

        self.assertEqual(point_addition(G_POINT, POINT_INFINITY), G_POINT)
        self.assertEqual(point_addition(POINT_INFINITY, G_POINT), G_POINT)

    def test_scalar_multiplication_small_k(self):
        # k=1
        pub_k1, steps_k1 = scalar_multiplication(1, G_POINT)
        self.assertEqual(pub_k1, G_POINT)
        self.assertEqual(len(steps_k1), 256)
        self.assertEqual(steps_k1[-1]['point_value'], G_POINT)
        # Check Base40 for last step of k=1
        n_for_angle_k1 = Gx % 40
        angle_k1 = number_to_angle(n_for_angle_k1)
        symbol_k1 = angle_to_symbol(angle_k1, DEFAULT_SYMBOLS)
        self.assertEqual(steps_k1[-1]['base40_angle'], angle_k1)
        self.assertEqual(steps_k1[-1]['base40_symbol'], symbol_k1)


        # k=2
        p_2G_manual = point_doubling(G_POINT)
        pub_k2, steps_k2 = scalar_multiplication(2, G_POINT)
        self.assertEqual(pub_k2, p_2G_manual)
        self.assertEqual(len(steps_k2), 256)
        self.assertEqual(steps_k2[-1]['point_value'], p_2G_manual)
        n_for_angle_k2 = p_2G_manual[0] % 40
        angle_k2 = number_to_angle(n_for_angle_k2)
        symbol_k2 = angle_to_symbol(angle_k2, DEFAULT_SYMBOLS)
        self.assertEqual(steps_k2[-1]['base40_angle'], angle_k2)
        self.assertEqual(steps_k2[-1]['base40_symbol'], symbol_k2)


    def test_scalar_multiplication_step_details(self):
        k = 3 # binary ...011
        _, steps = scalar_multiplication(k, G_POINT)
        self.assertEqual(len(steps), 256)

        # Check some properties of steps
        for i, step in enumerate(steps):
            self.assertEqual(step['step_number'], i + 1)
            self.assertIn(step['bit_value'], ['0', '1'])
            self.assertIsNotNone(step['operation'])
            if step['point_value'] is not POINT_INFINITY:
                self.assertTrue(is_on_curve(step['point_value'][0], step['point_value'][1]))
                self.assertIsNotNone(step['base40_angle'])
                self.assertIsNotNone(step['base40_symbol'])
                # Rodopios can be 0 or None for initial steps, or positive
                self.assertTrue(step['rodopios'] is None or isinstance(step['rodopios'], int))
            else: # Point is infinity
                self.assertIsNone(step['base40_angle'])
                self.assertIsNone(step['base40_symbol'])
                # Rodopios for infinity might be 0 or None based on implementation
                self.assertTrue(step['rodopios'] is None or step['rodopios'] == 0)


        # For k=3, the last few operations are important
        # Step 254 (bit index 1): bit (3>>1)&1 = 1. Op: Double & Add G. Point: 2G
        # Step 255 (bit index 0): bit (3>>0)&1 = 1. Op: Double & Add G. Point: 3G (actually (2*2G)+G if not careful)
        # The scalar_multiplication logic is:
        # for i from 255 down to 0: R = 2R; if bit_i_of_k == 1: R = R + G
        # k=3 (...0011)
        # step for bit index 1 (254th step in 0-255, or step_number 2): R becomes 2G. Then R becomes 2G+G = 3G.
        # This is not right. R should be G initially.
        # k=3: R=O
        # i=255 (bit 0): R=2O=O.
        # ...
        # i=1 (bit 1): R=2R. if 1: R=R+G. (This depends on prior R. If R was O, R=G)
        # i=0 (bit 1): R=2R. if 1: R=R+G. (If R was G, R=2G. Then R=2G+G=3G)

        # Let's trace the last point value for k=3
        p_3G_manual = point_addition(G_POINT, point_doubling(G_POINT))
        self.assertEqual(steps[-1]['point_value'], p_3G_manual)


    def test_scalar_multiplication_range(self):
        with self.assertRaises(ValueError):
            scalar_multiplication(0, G_POINT) # k must be >= 1
        with self.assertRaises(ValueError):
            scalar_multiplication(N, G_POINT) # k must be < N

        # Test a large k near N
        pub_key_large, steps_large = scalar_multiplication(N - 1, G_POINT)
        self.assertIsNotNone(pub_key_large)
        self.assertTrue(is_on_curve(pub_key_large[0], pub_key_large[1]))
        self.assertEqual(len(steps_large), 256)

if __name__ == '__main__':
    unittest.main()
