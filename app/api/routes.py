from flask import Blueprint, jsonify, current_app
import sys
import os

# Adjust path to ensure correct imports from 'app' sub-packages
# This assumes 'app' is the top-level package recognized by Python's import system.
# When running main.py, 'app' directory (containing main.py) is often the starting point.
# So, imports like 'from crypto.keys import ...' should resolve if 'app' is in sys.path.
# The sys.path.append in main.py should handle making 'app' findable.

from app.crypto.keys import generate_private_key, derive_public_key
from app.crypto.addresses import hash_public_key, ripemd160_to_base40, base58check_encode_bitcoin
from app.core_logic.base40 import decimal_to_base40, DEFAULT_SYMBOLS

api_bp = Blueprint('api', __name__)

@api_bp.route('/generate_keypair_detailed', methods=['GET'])
def generate_keypair_route():
    try:
        # 1. Generate private key
        priv_key_hex = generate_private_key()
        priv_key_int = int(priv_key_hex, 16)

        # 2. Derive public key and steps
        pub_key_hex, scalar_mult_steps = derive_public_key(priv_key_hex)

        # 3. Convert private key to Base40
        #    Using DEFAULT_SYMBOLS from core_logic.base40
        priv_key_base40 = decimal_to_base40(priv_key_int, DEFAULT_SYMBOLS)

        # 4. Convert public key's X-coordinate to Base40
        #    Public key is '04' + X(64 hex chars) + Y(64 hex chars)
        pub_key_x_hex = pub_key_hex[2:2+64]
        pub_key_x_int = int(pub_key_x_hex, 16)
        pub_key_x_base40 = decimal_to_base40(pub_key_x_int, DEFAULT_SYMBOLS)

        # --- HASH-DEPENDENT OPERATIONS ---
        # These will be affected by the hashlib.sha256 issue in the environment

        # 5. Hash public key (SHA256 then RIPEMD160)
        #    NOTE: hash_public_key will use the environment's (potentially flawed) hashlib
        hashed_pk_ripemd160_bytes = hash_public_key(pub_key_hex)
        hashed_pk_ripemd160_hex = hashed_pk_ripemd160_bytes.hex()

        # 6. Convert RIPEMD-160 hash to 31-symbol Base40 string
        #    Target length 31 as per spec
        address_b40 = ripemd160_to_base40(hashed_pk_ripemd160_bytes, target_length=31, symbols=DEFAULT_SYMBOLS)

        # 7. Convert RIPEMD-160 hash to Base58Check Bitcoin address
        #    Using version 0x00 for mainnet P2PKH by default
        #    NOTE: base58check_encode_bitcoin also uses hashlib for checksum
        address_btc_b58 = base58check_encode_bitcoin(hashed_pk_ripemd160_bytes, version_byte=0x00)

        # --- END OF HASH-DEPENDENT OPERATIONS ---

        response_data = {
            "private_key_hex": priv_key_hex,
            "private_key_base40": priv_key_base40,
            "public_key_uncompressed_hex": pub_key_hex,
            "public_key_x_base40": pub_key_x_base40,
            "hashed_public_key_ripemd160_hex": hashed_pk_ripemd160_hex, # Potentially incorrect
            "address_base40": address_b40,                             # Potentially incorrect
            "address_bitcoin_base58check": address_btc_b58,             # Potentially incorrect
            "scalar_multiplication_steps": scalar_mult_steps
        }

        return jsonify(response_data), 200

    except ValueError as ve:
        current_app.logger.error(f"ValueError in generate_keypair_detailed: {ve}")
        return jsonify({"error": "Invalid input or configuration", "details": str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Exception in generate_keypair_detailed: {e}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred on the server", "details": str(e)}), 500
