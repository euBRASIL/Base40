// frontend/src/core_logic_bridge.js

// This file acts as a bridge to share constants like DEFAULT_SYMBOLS
// from the backend's core logic with the frontend.
// In a real full-stack setup, this might be handled differently (e.g., API endpoint, shared package).

export const DEFAULT_SYMBOLS = [
    'α', 'β', 'γ', 'Δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'Ω', 'Ϙ', 'ω', 'Ϟ', 'Ϡ', 'Ҕ', 'Ԛ', 'Ӄ', 'Џ', 'Ʃ', 'Ɣ', 'Ӂ', 'Ҙ', 'ʤ', '⌀', 'ℓ', '∂'
];
// Ensure this list exactly matches the one in app/core_logic/base40.py
