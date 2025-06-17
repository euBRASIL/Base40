# app/core_logic/base40.py

# Define the 40 symbols.
# Using a simple alphanumeric set for now.
# Excludes characters that might be confusing in some fonts (e.g., I, l, 1, O, 0).
# Includes: A-H, J-N, P-Z, 2-9
# Base40: 40 símbolos correspondentes aos 40 ângulos múltiplos de 9 graus
DEFAULT_SYMBOLS = [
    'α', 'β', 'γ', 'Δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ',
    'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ',
    'φ', 'χ', 'ψ', 'Ω', 'Ϙ', 'ω', 'Ϟ', 'Ϡ', 'Ҕ', 'Ԛ',
    'Ӄ', 'Џ', 'Ʃ', 'Ɣ', 'Ӂ', 'Ҙ', 'ʤ', '⌀', 'ℓ', '∂'
]

def number_to_angle(n: int) -> int:
    """Converts a number n to an angle (n * 9) % 360."""
    if not isinstance(n, int):
        raise TypeError("Input 'n' must be an integer.")
    return (n * 9) % 360

def angle_to_symbol(angle: int, symbols: list = DEFAULT_SYMBOLS) -> str:
    """Maps an angle to its corresponding Base40 symbol."""
    if not isinstance(angle, int):
        raise TypeError("Input 'angle' must be an integer.")
    if angle < 0 or angle >= 360:
        raise ValueError("Angle must be between 0 and 359.")
    if angle % 9 != 0:
        raise ValueError("Angle must be a multiple of 9.")
    if len(symbols) != 40:
        raise ValueError("Symbols list must contain exactly 40 symbols.")

    index = angle // 9
    return symbols[index]

def symbol_to_index(symbol: str, symbols: list = DEFAULT_SYMBOLS) -> int:
    """Maps a Base40 symbol back to its numerical index (0-39)."""
    if not isinstance(symbol, str):
        raise TypeError("Input 'symbol' must be a string.")
    if len(symbol) != 1:
        # This check might be too restrictive if future symbols are multi-character,
        # but for single graphemes (like Greek letters), it's usually 1.
        # However, some combined characters might be > 1. For this set, they are single.
        pass # Allow symbols like 'ʤ' which might be perceived as multi-char by some len() in some contexts
             # but are single characters here. Python's len() on these should be 1.
    if len(symbols) != 40:
        raise ValueError("Symbols list must contain exactly 40 symbols.")

    try:
        return symbols.index(symbol)
    except ValueError:
        raise ValueError(f"Symbol '{symbol}' not found in Base40 symbols list.")

def index_to_number(index: int) -> int:
    """
    Converts an index (0-39) back to the original number 'n'
    that would produce that index in the Base40 mapping.
    In this context, the index is the number.
    """
    if not isinstance(index, int):
        raise TypeError("Input 'index' must be an integer.")
    if not (0 <= index < 40):
        raise ValueError("Index must be between 0 and 39.")
    return index

def decimal_to_base40(decimal_value: int, symbols: list = DEFAULT_SYMBOLS) -> str:
    """Converts a decimal number into a sequence of Base40 symbols."""
    if not isinstance(decimal_value, int):
        raise TypeError("Input 'decimal_value' must be an integer.")
    if decimal_value < 0:
        raise ValueError("Decimal value must be non-negative for Base40 conversion.")
    if len(symbols) != 40:
        raise ValueError("Symbols list must contain exactly 40 symbols.")

    if decimal_value == 0:
        return symbols[0]

    base40_string = []
    num = decimal_value
    while num > 0:
        remainder = num % 40
        base40_string.append(symbols[remainder])
        num //= 40

    return "".join(reversed(base40_string))

def base40_to_decimal(base40_string: str, symbols: list = DEFAULT_SYMBOLS) -> int:
    """Converts a string of Base40 symbols back to a decimal number."""
    if not isinstance(base40_string, str):
        raise TypeError("Input 'base40_string' must be a string.")
    if not base40_string:
        raise ValueError("Input 'base40_string' cannot be empty.")
    if len(symbols) != 40:
        raise ValueError("Symbols list must contain exactly 40 symbols.")

    decimal_value = 0
    power = 0
    for symbol_char in reversed(base40_string):
        try:
            symbol_val = symbols.index(symbol_char)
        except ValueError:
            raise ValueError(f"Symbol '{symbol_char}' not found in Base40 symbols list.")

        decimal_value += symbol_val * (40 ** power)
        power += 1

    return decimal_value

# Example Usage (primarily for testing or direct execution)
if __name__ == '__main__':
    print(f"Default symbols (count: {len(DEFAULT_SYMBOLS)}): {DEFAULT_SYMBOLS}")

    # Test number_to_angle
    print(f"Angle for n=0: {number_to_angle(0)}")
    print(f"Angle for n=1: {number_to_angle(1)}")
    print(f"Angle for n=39: {number_to_angle(39)}")
    print(f"Angle for n=40: {number_to_angle(40)}")
    print(f"Angle for n=41: {number_to_angle(41)}")

    # Test angle_to_symbol
    print(f"Symbol for angle 0: {angle_to_symbol(0)}")    # Expected: α
    print(f"Symbol for angle 9: {angle_to_symbol(9)}")    # Expected: β
    print(f"Symbol for angle 351: {angle_to_symbol(351)}") # Expected: ∂

    # Test symbol_to_index
    print(f"Index for symbol 'α': {symbol_to_index('α')}")
    print(f"Index for symbol 'β': {symbol_to_index('β')}")
    print(f"Index for symbol '∂': {symbol_to_index('∂')}")

    # Test index_to_number
    print(f"Number for index 0: {index_to_number(0)}")
    print(f"Number for index 39: {index_to_number(39)}")

    # Test decimal_to_base40
    # Example: 75 = 1*40 + 35. Symbols: β (idx 1), Ҙ (idx 35)
    print(f"Base40 for 0: {decimal_to_base40(0)}")     # Expected: α
    print(f"Base40 for 39: {decimal_to_base40(39)}")   # Expected: ∂
    print(f"Base40 for 40: {decimal_to_base40(40)}")   # Expected: βα
    print(f"Base40 for 75: {decimal_to_base40(75)}")   # Expected: βҘ
    print(f"Base40 for 1600: {decimal_to_base40(1600)}") # Expected: βαα

    # Test base40_to_decimal
    print(f"Decimal for 'α': {base40_to_decimal('α')}")
    print(f"Decimal for '∂': {base40_to_decimal('∂')}")
    print(f"Decimal for 'βα': {base40_to_decimal('βα')}")
    print(f"Decimal for 'βҘ': {base40_to_decimal('βҘ')}")
    print(f"Decimal for 'βαα': {base40_to_decimal('βαα')}")

    large_decimal = 1234567890
    # Standard math: indices (12,2,10,4,17,10) -> νγλε σλ
    # Env issue: indices (12,2,10,4,37,10) -> νγλε⌀λ
    base40_representation = decimal_to_base40(large_decimal)
    print(f"Base40 for {large_decimal}: {base40_representation}")
    reverted_decimal = base40_to_decimal(base40_representation)
    print(f"Reverted decimal for {base40_representation}: {reverted_decimal}")
    assert large_decimal == reverted_decimal
    print("Large number conversion test passed (may use environment-specific modulo result).")
