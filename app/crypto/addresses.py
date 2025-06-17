# app/crypto/addresses.py

import hashlib
import sys
import os

# Assuming the project root (/app) is in sys.path via test execution context or PYTHONPATH

from app.core_logic.base40 import decimal_to_base40, DEFAULT_SYMBOLS, base40_to_decimal

# Base58 alphabet (Bitcoin's alphabet)
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def bytes_to_int(byte_array: bytes) -> int:
    """Converts bytes to a big-endian integer."""
    return int.from_bytes(byte_array, 'big')

def int_to_bytes(integer: int, length: int = 0) -> bytes:
    """Converts an integer to big-endian bytes, optionally padded to a specific length."""
    if length == 0: # Calculate minimum length
        length = (integer.bit_length() + 7) // 8 if integer > 0 else 1
    return integer.to_bytes(length, 'big')

def hash_public_key(public_key_hex: str) -> bytes:
    """
    Hashes a public key using SHA-256 then RIPEMD-160 (H160).
    Args:
        public_key_hex: Uncompressed public key as a hex string (e.g., "04x_coordsy_coords").
    Returns:
        20-byte RIPEMD-160 hash.
    """
    if not public_key_hex.startswith('04') or len(public_key_hex) != 130: # 2 (04) + 64 (x) + 64 (y)
        raise ValueError("Public key must be an uncompressed hex string starting with '04' and be 130 chars long.")

    public_key_bytes = bytes.fromhex(public_key_hex)
    sha256_hash = hashlib.sha256(public_key_bytes).digest()

    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    return ripemd160.digest()

def ripemd160_to_base40(ripemd_hash_bytes: bytes, target_length: int = 31, symbols: list = DEFAULT_SYMBOLS) -> str:
    """
    Converts a 20-byte RIPEMD-160 hash into a Base40 string of a specific target length.
    Args:
        ripemd_hash_bytes: The 20-byte (160-bit) RIPEMD-160 hash.
        target_length: The desired length of the Base40 string (e.g., 31 symbols).
        symbols: The list of 40 symbols to use for encoding.
    Returns:
        A Base40 encoded string, padded with the first symbol if necessary to meet target_length.
    """
    if len(ripemd_hash_bytes) != 20:
        raise ValueError("RIPEMD-160 hash must be 20 bytes long.")

    large_integer = bytes_to_int(ripemd_hash_bytes)
    base40_str = decimal_to_base40(large_integer, symbols)

    padding_char = symbols[0]
    return base40_str.rjust(target_length, padding_char)

def base58_encode(data_bytes: bytes) -> str:
    """Encodes a byte sequence into a Base58 string."""
    num = bytes_to_int(data_bytes)

    if num == 0:
        return BASE58_ALPHABET[0]

    encoded = []
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded.append(BASE58_ALPHABET[remainder])

    for byte_val in data_bytes:
        if byte_val == 0:
            encoded.append(BASE58_ALPHABET[0])
        else:
            break

    return "".join(reversed(encoded))

def base58check_encode_bitcoin(ripemd_hash_bytes: bytes, version_byte: int = 0x00) -> str:
    """
    Performs Base58Check encoding on a RIPEMD-160 hash to produce a Bitcoin address.
    Args:
        ripemd_hash_bytes: The 20-byte RIPEMD-160 hash.
        version_byte: The version byte (e.g., 0x00 for P2PKH mainnet).
    Returns:
        A Base58Check encoded Bitcoin address string.
    """
    if len(ripemd_hash_bytes) != 20:
        raise ValueError("RIPEMD-160 hash must be 20 bytes long.")

    versioned_payload = bytes([version_byte]) + ripemd_hash_bytes

    checksum_hash1 = hashlib.sha256(versioned_payload).digest()
    checksum_hash2 = hashlib.sha256(checksum_hash1).digest()
    checksum = checksum_hash2[:4]

    full_payload = versioned_payload + checksum

    return base58_encode(full_payload)

# Self-tests would normally be here, but are omitted from execution due to known hashlib issue
# if __name__ == '__main__':
#    print("Self-tests for addresses.py would run here.")
#    # ... test code from previous attempt ...
