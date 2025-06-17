# app/ui_utils.py
import math
import cgi # For escaping attributes if needed, though not strictly for class/id if simple
from app.core_logic.base40 import DEFAULT_SYMBOLS

def generate_base40_svg_circle(target_symbol_to_highlight=None, svg_size=320, for_animation=False):
    center = svg_size / 2
    radius = svg_size * 0.4
    symbol_radius = svg_size * 0.45
    inner_circle_radius = radius * 0.2
    svg_elements = []

    # Make a simple unique ID for symbols that might not be valid CSS selectors directly
    def sanitize_for_id(symbol_str):
        # Simplified: just use index for animation IDs to avoid issues with complex symbols in selectors
        return f"s{DEFAULT_SYMBOLS.index(symbol_str)}" if symbol_str in DEFAULT_SYMBOLS else "invalid_symbol"

    svg_elements.append(
        f'<circle cx="{center}" cy="{center}" r="{radius * 1.05}" fill="none" stroke="#005000" stroke-width="1" />'
    )
    svg_elements.append(
        f'<circle cx="{center}" cy="{center}" r="{inner_circle_radius}" fill="#050505" stroke="#008000" stroke-width="1" />'
    )

    def get_coordinates_for_angle(angle_degrees, r):
        angle_radians = math.radians(angle_degrees - 90)
        return {"x": center + r * math.cos(angle_radians), "y": center + r * math.sin(angle_radians)}

    for index, symbol_char in enumerate(DEFAULT_SYMBOLS):
        angle = index * 9
        start_coords = get_coordinates_for_angle(angle, inner_circle_radius)
        end_coords = get_coordinates_for_angle(angle, radius)
        symbol_coords = get_coordinates_for_angle(angle, symbol_radius)

        is_static_highlighted = (symbol_char == target_symbol_to_highlight and not for_animation)

        # Default styles, will be overridden by JS if for_animation
        line_color = "#FFFF00" if is_static_highlighted else "#00FF00"
        line_width = "3" if is_static_highlighted else "1.5"
        text_fill = "#FFFF00" if is_static_highlighted else "#00FF00"

        symbol_id_suffix = sanitize_for_id(symbol_char)

        svg_elements.append(
            f'<line id="line-{symbol_id_suffix}" class="base40-line" '
            f'x1="{start_coords["x"]}" y1="{start_coords["y"]}" x2="{end_coords["x"]}" y2="{end_coords["y"]}" '
            f'stroke="{line_color if not for_animation else "#00FF00"}" stroke-width="{line_width if not for_animation else "1.5"}" />'
        )
        svg_elements.append(
            f'<text id="text-{symbol_id_suffix}" class="base40-text-on-circle" '
            f'x="{symbol_coords["x"]}" y="{symbol_coords["y"]}" fill="{text_fill if not for_animation else "#00FF00"}" '
            f'font-size="11" text-anchor="middle" dominant-baseline="middle" style="pointer-events: none; font-family: 'Consolas', 'Monaco', 'Courier New', Courier, monospace;">{cgi.escape(symbol_char)}</text>'
        )
        svg_elements.append(
            f'<circle id="dot-{symbol_id_suffix}" class="base40-dot" '
            f'cx="{end_coords["x"]}" cy="{end_coords["y"]}" r="2" fill="{line_color if not for_animation else "#00FF00"}" />'
        )

    # Central text display - ID for JS to update
    central_display_text = target_symbol_to_highlight if target_symbol_to_highlight and not for_animation else (DEFAULT_SYMBOLS[0] if for_animation and DEFAULT_SYMBOLS else "N/A")
    central_display_fill = "#FFFFFF" if target_symbol_to_highlight and not for_animation else ("#FFFFFF" if for_animation else "#008000")
    central_display_fontsize = "24" if target_symbol_to_highlight and not for_animation else ("24" if for_animation else "12")

    svg_elements.append(
        f'<text id="center-text-display" x="{center}" y="{center}" fill="{central_display_fill}" font-size="{central_display_fontsize}" '
        f'text-anchor="middle" dominant-baseline="central" font-weight="bold" style="font-family: 'Consolas', 'Monaco', 'Courier New', Courier, monospace;">{cgi.escape(central_display_text)}</text>'
    )
    return f'<svg id="base40-visualization-svg" width="{svg_size}" height="{svg_size}" xmlns="http://www.w3.org/2000/svg">{"".join(svg_elements)}</svg>'
