# app/crypto/secp256k1_utils.py

import sys
import os

# Assuming the project root (/app) is in sys.path via test execution context or PYTHONPATH

from app.core_logic.base40 import number_to_angle, angle_to_symbol, DEFAULT_SYMBOLS

# SECP256k1 Curve Parameters
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0
B = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Point at infinity
POINT_INFINITY = None

def inverse_mod(k, p):
    """Computes the modular multiplicative inverse of k modulo p using Fermat's Little Theorem."""
    if k == 0:
        raise ZeroDivisionError('division by zero')
    if k < 0:
        # k % p can be negative in Python if k < 0
        return pow(k % p, p - 2, p)
    return pow(k, p - 2, p)

def is_on_curve(x, y, a=A, b=B, p=P):
    """Checks if a point (x, y) is on the curve y^2 = x^3 + ax + b (mod p)."""
    if x is None or y is None: # Point at infinity
        return True
    return (y * y - (x * x * x + a * x + b)) % p == 0

def point_addition(p1, p2, a=A, b=B, p=P):
    """Performs point addition on the elliptic curve."""
    if p1 == POINT_INFINITY:
        return p2
    if p2 == POINT_INFINITY:
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 != y2:
        return POINT_INFINITY # p1 + (-p1) = infinity

    if x1 == x2: # This implies y1 == y2 (handled above if y1 != y2)
        # Point doubling case
        return point_doubling(p1, a, b, p)

    # Standard point addition
    # slope (s) = (y2 - y1) * (x2 - x1)^-1 mod p
    s_num = (y2 - y1) % p
    s_den = inverse_mod((x2 - x1) % p, p)
    s = (s_num * s_den) % p

    # x3 = (s^2 - x1 - x2) mod p
    x3 = (s * s - x1 - x2) % p
    # y3 = (s * (x1 - x3) - y1) mod p
    y3 = (s * (x1 - x3) - y1) % p

    return (x3, y3)

def point_doubling(pt, a=A, b=B, p=P):
    """Performs point doubling on the elliptic curve."""
    if pt == POINT_INFINITY:
        return POINT_INFINITY

    x1, y1 = pt

    if y1 == 0: # Tangent is vertical
        return POINT_INFINITY

    # slope (s) = (3*x1^2 + a) * (2*y1)^-1 mod p
    s_num = (3 * x1 * x1 + a) % p
    s_den = inverse_mod((2 * y1) % p, p)
    s = (s_num * s_den) % p

    # x3 = (s^2 - 2*x1) mod p
    x3 = (s * s - 2 * x1) % p
    # y3 = (s * (x1 - x3) - y1) mod p
    y3 = (s * (x1 - x3) - y1) % p

    return (x3, y3)

def scalar_multiplication(k: int, G=(Gx, Gy), symbols: list = DEFAULT_SYMBOLS, a=A, b=B, p=P):
    """
    Performs scalar multiplication (k * G) on the elliptic curve using the double-and-add algorithm.
    Records detailed steps for visualization.
    k: private key as an integer.
    G: generator point.
    symbols: Base40 symbols list.
    Returns a tuple: (final_public_key_point, steps_details_list)
    Each step detail is a dictionary:
    {
        'step_number': int (1 to 256),
        'bit_value': str (0 or 1),
        'operation': str ('Double' or 'Double & Add G'),
        'point_value': tuple (x, y) or None,
        'point_value_hex': {'x': hex_str, 'y': hex_str} or None,
        'base40_angle': int or None,
        'base40_symbol': str or None,
        'rodopios': int or None (change in symbol index from previous step)
    }
    """
    if not isinstance(k, int):
        raise TypeError("Scalar 'k' (private key) must be an integer.")
    if k <= 0 or k >= N: # Private key must be in [1, N-1]
        raise ValueError(f"Scalar 'k' must be between 1 and N-1. Got: {k}")

    final_result_point = POINT_INFINITY
    steps_details_final = []
    previous_symbol_index_final = None

    for i in range(255, -1, -1): # Iterate 256 times, for each bit index
        bit_value = (k >> i) & 1 # Get the i-th bit (MSB is i=255, LSB is i=0)

        operation_performed = []

        final_result_point = point_doubling(final_result_point, a, b, p)
        operation_performed.append("Double")

        if bit_value == 1:
            final_result_point = point_addition(final_result_point, G, a, b, p)
            operation_performed.append("Add G")

        current_x_final = final_result_point[0] if final_result_point else None
        current_y_final = final_result_point[1] if final_result_point else None

        base40_angle_val_final = None
        base40_symbol_val_final = None
        rodopios_val_final = None

        if current_x_final is not None:
            n_for_angle_final = current_x_final % 40
            base40_angle_val_final = number_to_angle(n_for_angle_final)
            current_symbol_index_final = base40_angle_val_final // 9
            base40_symbol_val_final = symbols[current_symbol_index_final]

            if previous_symbol_index_final is not None:
                rodopios_val_final = (current_symbol_index_final - previous_symbol_index_final + 40) % 40
            else:
                # First step that produces a symbol. Rodopios from a hypothetical "zero" state.
                # Or, if defined as "change from previous step", it's 0 if previous was infinity.
                rodopios_val_final = 0
            previous_symbol_index_final = current_symbol_index_final
        else:
            rodopios_val_final = 0 # Or None, if point is infinity, no symbol change
            previous_symbol_index_final = None

        steps_details_final.append({
            'step_number': 256 - i,
            'bit_value': str(bit_value),
            'operation': " & ".join(operation_performed),
            'point_value': final_result_point,
            'point_value_hex': {'x': hex(current_x_final), 'y': hex(current_y_final)} if current_x_final is not None else None,
            'base40_angle': base40_angle_val_final,
            'base40_symbol': base40_symbol_val_final,
            'rodopios': rodopios_val_final
        })

    return final_result_point, steps_details_final


if __name__ == '__main__':
    # Test SECP256k1 operations
    assert is_on_curve(Gx, Gy)
    print(f"Generator G ({hex(Gx)}, {hex(Gy)}) is on curve.")

    G_point = (Gx, Gy)
    G2_point = point_doubling(G_point)
    assert is_on_curve(G2_point[0], G2_point[1])
    print(f"2G ({hex(G2_point[0])}, {hex(G2_point[1])}) is on curve.")

    # Expected 2G (values from a trusted source for comparison if needed)
    G2_expected_x = 0xC6047F9441ED7D6D3045406E95C07CD85C778E4B8CEF3CA7ABAC09B95C709EE5
    G2_expected_y = 0x1AE168FEA63DC339A3C58419466CEAEEF7F632653266D0E1236431A950CFE52A
    assert G2_point[0] == G2_expected_x
    assert G2_point[1] == G2_expected_y
    print("Point doubling G matches expected 2G.")

    G3_point = point_addition(G_point, G2_point)
    assert is_on_curve(G3_point[0], G3_point[1])
    print(f"3G (G + 2G) ({hex(G3_point[0])}, {hex(G3_point[1])}) is on curve.")

    pub_key_k1, steps_k1 = scalar_multiplication(1)
    assert pub_key_k1 == G_point
    print(f"Scalar multiplication for k=1 yields G. Steps: {len(steps_k1)}")

    pub_key_k2, steps_k2 = scalar_multiplication(2)
    assert pub_key_k2 == G2_point
    print(f"Scalar multiplication for k=2 yields 2G. Steps: {len(steps_k2)}")

    pub_key_k3, steps_k3 = scalar_multiplication(3)
    # Expected 3G (calculated from G + 2G)
    assert pub_key_k3[0] == G3_point[0] and pub_key_k3[1] == G3_point[1]
    print(f"Scalar multiplication for k=3 yields 3G. Steps: {len(steps_k3)}")

    k_large = N - 1
    print(f"Testing scalar multiplication for k = N-1 (a large key)...")
    pub_key_large, steps_large = scalar_multiplication(k_large)
    assert is_on_curve(pub_key_large[0], pub_key_large[1])
    print(f"Public key for k=N-1: ({hex(pub_key_large[0])}, {hex(pub_key_large[1])}) is on curve.")
    print(f"Number of steps recorded for k=N-1: {len(steps_large)}")
    assert len(steps_large) == 256

    print("SECP256k1 utils self-tests (basic) passed.")

    if steps_k3:
        print("\nDetails for k=3 (last few steps where actual computation happens):")
        # For k=3 (binary ...0011)
        # Bits are processed from MSB (i=255) to LSB (i=0)
        # Step 1 (i=255, bit=(k>>255)&1 = 0): Double(Inf)=Inf. Result: Inf
        # ...
        # Step 254 (i=1, bit=(k>>1)&1 = 1): Double(Prev). Add G.
        # Step 255 (i=0, bit=(k>>0)&1 = 1): Double(Prev). Add G.
        # The step_number is 256-i. So step 255 is i=1, step 256 is i=0.

        relevant_steps_k3 = [s for s in steps_k3 if s['step_number'] >= 254] # Last 3 steps
        for step in relevant_steps_k3:
            point_x_hex = hex(step['point_value'][0]) if step['point_value'] else 'Inf'
            print(f"  Step {step['step_number']}: Bit '{step['bit_value']}', Op: {step['operation']}, "
                  f"Pt.X: {point_x_hex}, "
                  f"Symbol: {step['base40_symbol']}, Rodopios: {step['rodopios']}")

    last_step_k1 = steps_k1[-1]
    if last_step_k1['point_value']:
        expected_n_k1 = last_step_k1['point_value'][0] % 40
        expected_angle_k1 = number_to_angle(expected_n_k1)
        expected_symbol_k1 = angle_to_symbol(expected_angle_k1)

        print(f"\nFor k=1, last step (step {last_step_k1['step_number']}) X: {hex(last_step_k1['point_value'][0])}")
        print(f"  X % 40 = {expected_n_k1}")
        print(f"  Expected angle: {expected_angle_k1}, Got: {last_step_k1['base40_angle']}")
        print(f"  Expected symbol: {expected_symbol_k1}, Got: {last_step_k1['base40_symbol']}")
        assert last_step_k1['base40_angle'] == expected_angle_k1
        assert last_step_k1['base40_symbol'] == expected_symbol_k1
        # Rodopios for the step that produces G for k=1 (bit 0 is 1):
        # Prev point was Inf (after many doublings of Inf). previous_symbol_index_final is None.
        # So rodopios is 0.
        print(f"  Rodopios: {last_step_k1['rodopios']}")
        assert last_step_k1['rodopios'] == 0 # Expect 0 as it's the first symbol generated in effect
    print("Base40 mapping in scalar multiplication steps for k=1 verified.")
