// frontend/src/core_logic_bridge.js

// This file acts as a bridge to share constants like DEFAULT_SYMBOLS
// from the backend's core logic with the frontend.
// In a real full-stack setup, this might be handled differently (e.g., API endpoint, shared package).

export const DEFAULT_SYMBOLS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'
];
// Ensure this list exactly matches the one in app/core_logic/base40.py
