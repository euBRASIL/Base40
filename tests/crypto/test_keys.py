import unittest
import sys
import os

# Add parent directory of 'app' to Python path (i.e., /app directory itself, which is the project root)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.crypto.keys import generate_private_key, derive_public_key
from app.crypto.secp256k1_utils import N, Gx, Gy

class TestKeys(unittest.TestCase):

    def test_generate_private_key(self):
        for _ in range(10): # Generate a few keys
            priv_key_hex = generate_private_key()
            self.assertEqual(len(priv_key_hex), 64)
            try:
                priv_key_int = int(priv_key_hex, 16)
                self.assertTrue(1 <= priv_key_int < N)
            except ValueError:
                self.fail("Generated private key is not valid hex.")

    def test_derive_public_key_k1(self):
        priv_k1_hex = format(1, '064x')
        pub_key_hex, steps = derive_public_key(priv_k1_hex)

        expected_gx_hex = format(Gx, '064x')
        expected_gy_hex = format(Gy, '064x')
        expected_pub_k1_hex = f"04{expected_gx_hex}{expected_gy_hex}"

        self.assertEqual(pub_key_hex, expected_pub_k1_hex)
        self.assertEqual(len(steps), 256)
        self.assertIsNotNone(steps[-1]['point_value'])
        if steps[-1]['point_value']: # Should not be None
             self.assertEqual(steps[-1]['point_value'][0], Gx)
             self.assertEqual(steps[-1]['point_value'][1], Gy)


    def test_derive_public_key_validations(self):
        with self.assertRaisesRegex(ValueError, "Private key must be a 64-character hex string."):
            derive_public_key("1234")
        with self.assertRaisesRegex(ValueError, "Private key is not a valid hexadecimal string."):
            derive_public_key("xx" * 32)
        with self.assertRaisesRegex(ValueError, "Private key integer value is out of the valid range"):
            derive_public_key(format(0, '064x'))
        with self.assertRaisesRegex(ValueError, "Private key integer value is out of the valid range"):
            derive_public_key(format(N, '064x'))

    def test_derive_public_key_structure(self):
        priv_key_hex = generate_private_key()
        pub_key_hex, steps = derive_public_key(priv_key_hex)

        self.assertTrue(pub_key_hex.startswith('04'))
        self.assertEqual(len(pub_key_hex), 130) # 04 + X(64) + Y(64)
        self.assertEqual(len(steps), 256)

        # Check structure of a step item
        if steps:
            step = steps[0]
            self.assertIn('step_number', step)
            self.assertIn('bit_value', step)
            self.assertIn('operation', step)
            self.assertIn('point_value', step)
            self.assertIn('point_value_hex', step)
            self.assertIn('base40_angle', step)
            self.assertIn('base40_symbol', step)
            self.assertIn('rodopios', step)

if __name__ == '__main__':
    unittest.main()
