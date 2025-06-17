from flask import Blueprint, render_template, current_app, request, redirect, url_for, Response
import sys
import os
import json
import io
import csv

from app.crypto.keys import generate_private_key, derive_public_key
from app.crypto.addresses import hash_public_key, ripemd160_to_base40, base58check_encode_bitcoin
from app.core_logic.base40 import decimal_to_base40, DEFAULT_SYMBOLS
from app.ui_utils import generate_base40_svg_circle

ui_bp = Blueprint('ui', __name__, template_folder='../templates', static_folder='../static')

def get_full_crypto_data():
    # ... (same as before)
    try:
        priv_key_hex = generate_private_key()
        priv_key_int = int(priv_key_hex, 16)
        pub_key_hex, scalar_mult_steps = derive_public_key(priv_key_hex)
        priv_key_base40 = decimal_to_base40(priv_key_int, DEFAULT_SYMBOLS)
        pub_key_x_hex = pub_key_hex[2:2+64]
        pub_key_x_int = int(pub_key_x_hex, 16)
        pub_key_x_base40 = decimal_to_base40(pub_key_x_int, DEFAULT_SYMBOLS)
        hashed_pk_ripemd160_bytes = hash_public_key(pub_key_hex)
        hashed_pk_ripemd160_hex = hashed_pk_ripemd160_bytes.hex()
        address_b40 = ripemd160_to_base40(hashed_pk_ripemd160_bytes, target_length=31, symbols=DEFAULT_SYMBOLS)
        address_btc_b58 = base58check_encode_bitcoin(hashed_pk_ripemd160_bytes, version_byte=0x00)

        return {
            "private_key_hex": priv_key_hex, "private_key_base40": priv_key_base40,
            "public_key_uncompressed_hex": pub_key_hex, "public_key_x_base40": pub_key_x_base40,
            "hashed_public_key_ripemd160_hex": hashed_pk_ripemd160_hex, "address_base40": address_b40,
            "address_bitcoin_base58check": address_btc_b58, "scalar_multiplication_steps": scalar_mult_steps
        }, None
    except Exception as e:
        current_app.logger.error(f"Error generating crypto data: {e}", exc_info=True)
        return None, str(e)

@ui_bp.route('/', methods=['GET', 'POST'])
def index():
    data_bundle = None
    error_msg = None
    svg_visualization_markup = None
    animation_symbols = [] # For JS animation

    data_bundle, error_msg = get_full_crypto_data()

    if data_bundle and data_bundle.get('scalar_multiplication_steps'):
        steps = data_bundle['scalar_multiplication_steps']
        if steps:
            animation_symbols = [step.get('base40_symbol') for step in steps if step.get('base40_symbol')]
            # Generate SVG for animation (initial state, JS will take over)
            svg_visualization_markup = generate_base40_svg_circle(for_animation=True)

    if not svg_visualization_markup:
        svg_visualization_markup = generate_base40_svg_circle(for_animation=True) # Default SVG for animation

    return render_template('index.html', data=data_bundle,
                           svg_visualization=svg_visualization_markup,
                           error_message=error_msg,
                           animation_symbols_json=json.dumps(animation_symbols), # Pass symbols as JSON string
                           default_symbols_json=json.dumps(DEFAULT_SYMBOLS)) # Pass DEFAULT_SYMBOLS for JS

# ... (export routes remain the same) ...
@ui_bp.route('/export/json', methods=['GET'])
def export_json():
    data_bundle, error_msg = get_full_crypto_data()
    if error_msg or not data_bundle:
        current_app.logger.error(f"Export JSON failed: {error_msg}")
        return redirect(url_for('ui.index', error_message=f"Could not generate data for JSON export: {error_msg}"))
    json_output = json.dumps(data_bundle, indent=2)
    return Response(
        json_output,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=base40_crypto_data.json"}
    )

@ui_bp.route('/export/csv', methods=['GET'])
def export_csv():
    data_bundle, error_msg = get_full_crypto_data()
    if error_msg or not data_bundle or not data_bundle.get('scalar_multiplication_steps'):
        current_app.logger.error(f"Export CSV failed: {error_msg or 'Missing steps data'}")
        return redirect(url_for('ui.index', error_message=f"Could not generate data for CSV export: {error_msg or 'Missing steps data'}"))
    steps_data = data_bundle['scalar_multiplication_steps']
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    headers = ['Step', 'Bit', 'Operation', 'Point_X_Hex', 'Point_Y_Hex', 'Base40_Angle', 'Base40_Symbol', 'Rodopios']
    writer.writerow(headers)
    for step in steps_data:
        row = [
            step.get('step_number', ''), step.get('bit_value', ''), step.get('operation', ''),
            step.get('point_value_hex', {}).get('x', 'Infinity' if step.get('point_value') is None else ''),
            step.get('point_value_hex', {}).get('y', 'Infinity' if step.get('point_value') is None else ''),
            step.get('base40_angle', '') if step.get('base40_angle') is not None else '',
            step.get('base40_symbol', ''),
            step.get('rodopios', '') if step.get('rodopios') is not None else '' ]
        writer.writerow(row)
    csv_data = output.getvalue()
    output.close()
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=base40_scalar_steps.csv"}
    )
