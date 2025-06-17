// app/static/js/visualization.js
// This script expects `animationSymbolList` to be available globally or passed to init function.
// It also expects `DEFAULT_SYMBOLS_FOR_JS` to be available for mapping symbols to IDs.

let animationTimeoutId = null;
const baseHighlightColor = "#FFFF00"; // Yellow
const defaultLineColor = "#00FF00";  // Green
const defaultTextColor = "#00FF00"; // Green
const defaultDotColor = "#00FF00";   // Green
const animationSpeed = 75; // ms

function sanitizeForIdJS(symbolStr, symbolsArray) {
    const index = symbolsArray.indexOf(symbolStr);
    return index !== -1 ? `s${index}` : null;
}

function updateSvgHighlight(symbolIdSuffix, highlight, symbolsArray) {
    if (!symbolIdSuffix) return;

    const lineElement = document.getElementById(`line-${symbolIdSuffix}`);
    const textElement = document.getElementById(`text-${symbolIdSuffix}`);
    const dotElement = document.getElementById(`dot-${symbolIdSuffix}`);

    if (lineElement) {
        lineElement.setAttribute('stroke', highlight ? baseHighlightColor : defaultLineColor);
        lineElement.setAttribute('stroke-width', highlight ? '3' : '1.5');
    }
    if (textElement) {
        textElement.setAttribute('fill', highlight ? baseHighlightColor : defaultTextColor);
    }
    if (dotElement) {
        dotElement.setAttribute('fill', highlight ? baseHighlightColor : defaultDotColor);
    }
}

function updateCenterText(symbolStr) {
    const centerTextElement = document.getElementById('center-text-display');
    if (centerTextElement) {
        centerTextElement.textContent = symbolStr || "N/A";
        centerTextElement.setAttribute('fill', symbolStr ? "#FFFFFF" : "#008000");
        centerTextElement.setAttribute('font-size', symbolStr ? "24" : "12");
    }
}

function animateRodopios(symbolsList, defaultSymbols) {
    if (animationTimeoutId) {
        clearTimeout(animationTimeoutId);
    }

    let currentStepIndex = 0;
    let lastSymbolIdSuffix = null;

    function animateNext() {
        // De-highlight previous symbol
        if (lastSymbolIdSuffix) {
            updateSvgHighlight(lastSymbolIdSuffix, false, defaultSymbols);
        }

        if (currentStepIndex < symbolsList.length) {
            const currentSymbol = symbolsList[currentStepIndex];
            const currentSymbolIdSuffix = sanitizeForIdJS(currentSymbol, defaultSymbols);

            if (currentSymbolIdSuffix) {
                updateSvgHighlight(currentSymbolIdSuffix, true, defaultSymbols);
                updateCenterText(currentSymbol);
                lastSymbolIdSuffix = currentSymbolIdSuffix;
            } else {
                // Symbol not found in default list, skip or log error
                updateCenterText('?'); // Indicate unknown symbol
                lastSymbolIdSuffix = null;
            }

            currentStepIndex++;
            animationTimeoutId = setTimeout(animateNext, animationSpeed);
        } else {
            // Animation finished, keep last symbol highlighted if it was valid
            if (lastSymbolIdSuffix) {
                 // updateCenterText(symbolsList[symbolsList.length - 1]); // Already set
            } else if (symbolsList.length > 0) {
                // if last symbol was invalid, but list was not empty
                updateCenterText(symbolsList[symbolsList.length - 1] || '?');
            } else {
                updateCenterText("N/A"); // No symbols in list
                 // De-highlight all if list is empty (should be handled by initial SVG render)
            }
        }
    }

    if (symbolsList && symbolsList.length > 0 && defaultSymbols && defaultSymbols.length > 0) {
        // Reset all to default before starting animation
        defaultSymbols.forEach(s => {
            const idSuffix = sanitizeForIdJS(s, defaultSymbols);
            if (idSuffix) updateSvgHighlight(idSuffix, false, defaultSymbols);
        });
        animateNext();
    } else {
        // No symbols to animate, ensure center text is N/A or default
        updateCenterText(defaultSymbols && defaultSymbols.length > 0 ? defaultSymbols[0] : "N/A");
         // De-highlight all if list is empty
        if (defaultSymbols) {
            defaultSymbols.forEach(s => {
                const idSuffix = sanitizeForIdJS(s, defaultSymbols);
                if (idSuffix) updateSvgHighlight(idSuffix, false, defaultSymbols);
            });
        }
    }
}

// Make init function available globally or via event listener
// window.initRodopiosAnimation = animateRodopios;
// Or, if script is loaded after DOM and data is ready:
// if (window.animationSymbolList && window.DEFAULT_SYMBOLS_FOR_JS) {
//     animateRodopios(window.animationSymbolList, window.DEFAULT_SYMBOLS_FOR_JS);
// }
