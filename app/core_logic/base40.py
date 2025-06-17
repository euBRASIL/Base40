# app/core_logic/base40.py

# Define the 40 symbols.
# Using a simple alphanumeric set for now.
# Excludes characters that might be confusing in some fonts (e.g., I, l, 1, O, 0).
# Includes: A-H, J-N, P-Z, 2-9
DEFAULT_SYMBOLS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' # Adding lowercase to reach 40 symbols
] # Length should be 40

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
        raise ValueError("Input 'symbol' must be a single character.")
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
    print(f"Angle for n=0: {number_to_angle(0)}")  # Expected: 0
    print(f"Angle for n=1: {number_to_angle(1)}")  # Expected: 9
    print(f"Angle for n=39: {number_to_angle(39)}") # Expected: 351
    print(f"Angle for n=40: {number_to_angle(40)}") # Expected: 0
    print(f"Angle for n=41: {number_to_angle(41)}") # Expected: 9

    # Test angle_to_symbol
    print(f"Symbol for angle 0: {angle_to_symbol(0)}")    # Expected: A (DEFAULT_SYMBOLS[0])
    print(f"Symbol for angle 9: {angle_to_symbol(9)}")    # Expected: B (DEFAULT_SYMBOLS[1])
    print(f"Symbol for angle 351: {angle_to_symbol(351)}") # Expected: h (DEFAULT_SYMBOLS[39])

    # Test symbol_to_index
    print(f"Index for symbol 'A': {symbol_to_index('A')}") # Expected: 0
    print(f"Index for symbol 'B': {symbol_to_index('B')}") # Expected: 1
    print(f"Index for symbol 'h': {symbol_to_index('h')}") # Expected: 39

    # Test index_to_number
    print(f"Number for index 0: {index_to_number(0)}") # Expected: 0
    print(f"Number for index 39: {index_to_number(39)}") # Expected: 39

    # Test decimal_to_base40
    print(f"Base40 for 0: {decimal_to_base40(0)}")     # Expected: A (symbols[0])
    print(f"Base40 for 39: {decimal_to_base40(39)}")   # Expected: h (symbols[39])
    print(f"Base40 for 40: {decimal_to_base40(40)}")   # Expected: BA (symbols[1]symbols[0])
    print(f"Base40 for 75: {decimal_to_base40(75)}")   # Expected: Bh (1*40 + 35) -> B=1, h=35
                                                       # 75 % 40 = 35 (h)
                                                       # 75 // 40 = 1 (B)
    print(f"Base40 for 1600: {decimal_to_base40(1600)}") # Expected: BAA (1*40^2 + 0*40^1 + 0*40^0)

    # Test base40_to_decimal
    print(f"Decimal for 'A': {base40_to_decimal('A')}")     # Expected: 0
    print(f"Decimal for 'h': {base40_to_decimal('h')}")     # Expected: 39
    print(f"Decimal for 'BA': {base40_to_decimal('BA')}")   # Expected: 40
    print(f"Decimal for 'Bh': {base40_to_decimal('Bh')}")   # Expected: 75
    print(f"Decimal for 'BAA': {base40_to_decimal('BAA')}") # Expected: 1600

    try:
        print(f"Symbol for angle 5: {angle_to_symbol(5)}")
    except ValueError as e:
        print(f"Error (expected): {e}")

    try:
        print(f"Index for symbol '*': {symbol_to_index('*')}")
    except ValueError as e:
        print(f"Error (expected): {e}")

    try:
        custom_symbols = ['0', '1'] # Not 40
        print(f"Decimal for '10' with custom symbols: {base40_to_decimal('10', custom_symbols)}")
    except ValueError as e:
        print(f"Error (expected for custom symbols): {e}")

    # A larger number for conversion
    large_decimal = 1234567890
    base40_representation = decimal_to_base40(large_decimal)
    print(f"Base40 for {large_decimal}: {base40_representation}")
    reverted_decimal = base40_to_decimal(base40_representation)
    print(f"Reverted decimal for {base40_representation}: {reverted_decimal}")
    assert large_decimal == reverted_decimal
    print("Large number conversion test passed.")
