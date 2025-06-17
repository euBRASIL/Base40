# app/crypto/keys.py

import os
import sys

# Assuming the project root (/app) is in sys.path via test execution context or PYTHONPATH

from app.crypto.secp256k1_utils import N, Gx, Gy, scalar_multiplication, POINT_INFINITY
# No, Gx, Gy are defaults in scalar_multiplication. We need G_POINT as (Gx, Gy)
G_POINT = (Gx, Gy)


def generate_private_key() -> str:
    """
    Generates a cryptographically secure 256-bit private key valid for SECP256k1.
    Returns the private key as a 64-character hexadecimal string.
    A private key is an integer k such that 1 <= k < N.
    """
    while True:
        # Generate 32 random bytes (256 bits)
        random_bytes = os.urandom(32)
        private_key_int = int.from_bytes(random_bytes, 'big')
        # Ensure the key is within the valid range [1, N-1]
        if 1 <= private_key_int < N:
            return format(private_key_int, '064x') # Pad with leading zeros to ensure 64 chars

def derive_public_key(private_key_hex: str) -> tuple:
    """
    Derives the public key from a given private key.

    Args:
        private_key_hex: The private key as a 64-character hexadecimal string.

    Returns:
        A tuple containing:
        - public_key_hex (str): The uncompressed public key ('04' + x_hex + y_hex).
        - steps_details (list): A list of dictionaries detailing each step of scalar multiplication.
    Raises:
        ValueError: If private_key_hex is invalid or out of range.
    """
    if not isinstance(private_key_hex, str) or len(private_key_hex) != 64:
        raise ValueError("Private key must be a 64-character hex string.")

    try:
        private_key_int = int(private_key_hex, 16)
    except ValueError:
        raise ValueError("Private key is not a valid hexadecimal string.")

    if not (1 <= private_key_int < N):
        raise ValueError(f"Private key integer value is out of the valid range [1, N-1]. Got {private_key_int}")

    public_key_point, steps = scalar_multiplication(private_key_int, G_POINT)

    if public_key_point == POINT_INFINITY:
        # This should theoretically not happen for valid private keys 1 <= k < N
        raise Exception("Scalar multiplication resulted in point at infinity, which is unexpected for valid private keys.")

    px_hex = format(public_key_point[0], '064x')
    py_hex = format(public_key_point[1], '064x')

    uncompressed_public_key = f"04{px_hex}{py_hex}"

    return uncompressed_public_key, steps

if __name__ == '__main__':
    print("Generating a new private key...")
    priv_key_hex = generate_private_key()
    print(f"  Private Key (hex): {priv_key_hex}")
    assert len(priv_key_hex) == 64
    priv_key_int = int(priv_key_hex, 16)
    assert 1 <= priv_key_int < N
    print(f"  Private Key (int): {priv_key_int} (Valid range: [1, {N-1}])")
    print("  Private key generated successfully and is within valid range.")

    print("\nDeriving public key...")
    try:
        pub_key_hex, multiplication_steps = derive_public_key(priv_key_hex)
        print(f"  Public Key (uncompressed hex): {pub_key_hex}")
        assert pub_key_hex.startswith('04') and len(pub_key_hex) == 2 + 64 + 64
        print(f"  Number of scalar multiplication steps recorded: {len(multiplication_steps)}")
        assert len(multiplication_steps) == 256

        # Check content of a step (e.g., the last one)
        last_step = multiplication_steps[-1]
        print(f"  Last step details (example):")
        print(f"    Bit: {last_step['bit_value']}")
        print(f"    Operation: {last_step['operation']}")
        if last_step['point_value_hex']:
            print(f"    Point.X (hex): {last_step['point_value_hex']['x']}")
        print(f"    Base40 Symbol: {last_step['base40_symbol']}")
        print(f"    Rodopios: {last_step['rodopios']}")

        print("  Public key derived successfully.")

        # Test with a known private key (k=1)
        print("\nTesting with private key k=1...")
        priv_k1_hex = format(1, '064x')
        pub_k1_hex, steps_k1 = derive_public_key(priv_k1_hex)

        expected_gx_hex = format(Gx, '064x')
        expected_gy_hex = format(Gy, '064x')
        expected_pub_k1_hex = f"04{expected_gx_hex}{expected_gy_hex}"

        assert pub_k1_hex == expected_pub_k1_hex
        print(f"  Public key for k=1 matches G: {pub_k1_hex == expected_pub_k1_hex}")
        assert len(steps_k1) == 256
        # The final point in steps_k1 should be G
        final_point_k1_x = steps_k1[-1]['point_value'][0]
        final_point_k1_y = steps_k1[-1]['point_value'][1]
        assert final_point_k1_x == Gx
        assert final_point_k1_y == Gy
        print("  Final point in k=1 steps matches G.")


    except ValueError as ve:
        print(f"Error during key derivation test: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Test invalid private key (e.g., too short, not hex, out of range)
    print("\nTesting invalid private keys:")
    invalid_keys_tests = {
        "short_hex": "1234",
        "non_hex": "xx" * 32,
        "zero_key": "00" * 32,
        "N_key": format(N, '064x') # N itself is invalid
    }
    for name, key_val in invalid_keys_tests.items():
        try:
            derive_public_key(key_val)
            print(f"  Test '{name}' with key '{key_val}': FAILED (should have raised ValueError)")
        except ValueError as e:
            print(f"  Test '{name}' with key '{key_val}': PASSED (Correctly raised ValueError: {e})")

    print("\nKey generation and derivation self-tests completed.")
