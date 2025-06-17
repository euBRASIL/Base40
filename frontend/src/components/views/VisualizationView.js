import React from 'react';
import { useData } from '../../context/DataContext';
import { DEFAULT_SYMBOLS } from '../../core_logic_bridge'; // Assuming a bridge file or direct path later

const VisualizationView = () => {
  const { keyData, isLoading } = useData();

  const svgSize = 320; // Increased size for better visibility
  const center = svgSize / 2;
  const radius = svgSize * 0.4; // Radius for the main circle lines
  const symbolRadius = svgSize * 0.45; // Radius for placing symbols

  // Get the Base40 symbol from the last step of scalar multiplication, if available
  let lastSymbol = null;
  if (keyData && keyData.scalar_multiplication_steps && keyData.scalar_multiplication_steps.length > 0) {
    const lastStep = keyData.scalar_multiplication_steps[keyData.scalar_multiplication_steps.length - 1];
    if (lastStep && lastStep.base40_symbol) {
      lastSymbol = lastStep.base40_symbol;
    }
  }

  // Fallback if DEFAULT_SYMBOLS is not available (e.g. during isolated dev)
  const symbolsToUse = typeof DEFAULT_SYMBOLS !== 'undefined' ? DEFAULT_SYMBOLS :
    Array.from({length: 40}, (_, i) => String.fromCharCode(65 + i)); // A-Z then more letters


  const getCoordinatesForAngle = (angleDegrees, r) => {
    const angleRadians = (angleDegrees - 90) * (Math.PI / 180); // Offset by -90 to start 0deg at top
    return {
      x: center + r * Math.cos(angleRadians),
      y: center + r * Math.sin(angleRadians),
    };
  };

  if (isLoading && !keyData) {
    return (
      <section className="view-section" id="visualization-section">
        <h2>Symbolic Visualization</h2>
        <div style={{ width: `${svgSize}px`, height: `${svgSize}px`, border: '1px solid #00FF00', margin: '20px auto', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <p>Loading Visualization...</p>
        </div>
      </section>
    );
  }

  return (
    <section className="view-section" id="visualization-section">
      <h2>Symbolic Visualization</h2>
      <svg width={svgSize} height={svgSize} style={{ margin: '0 auto', display: 'block' }}>
        {/* Outer circle border */}
        <circle cx={center} cy={center} r={radius * 1.05} fill="none" stroke="#005000" strokeWidth="1" />
        {/* Inner circle for aesthetics */}
        <circle cx={center} cy={center} r={radius * 0.2} fill="#050505" stroke="#008000" strokeWidth="1" />

        {symbolsToUse.map((symbol, index) => {
          const angle = index * 9; // Each symbol is 9 degrees apart
          const startCoords = getCoordinatesForAngle(angle, radius * 0.2); // Start from inner circle
          const endCoords = getCoordinatesForAngle(angle, radius);
          const symbolCoords = getCoordinatesForAngle(angle, symbolRadius);

          const isHighlighted = symbol === lastSymbol;

          return (
            <g key={index}>
              <line
                x1={startCoords.x}
                y1={startCoords.y}
                x2={endCoords.x}
                y2={endCoords.y}
                stroke={isHighlighted ? "#FFFF00" : "#00FF00"} // Yellow if highlighted, else green
                strokeWidth={isHighlighted ? "3" : "1.5"}
              />
              <text
                x={symbolCoords.x}
                y={symbolCoords.y}
                fill={isHighlighted ? "#FFFF00" : "#00FF00"}
                fontSize="11" // Adjusted font size
                textAnchor="middle"
                dominantBaseline="middle"
                style={{ pointerEvents: 'none' }} // Make text non-interactive for now
              >
                {symbol}
              </text>
              {/* Optional: Small circle at the end of each line */}
              <circle cx={endCoords.x} cy={endCoords.y} r="2" fill={isHighlighted ? "#FFFF00" : "#00FF00"} />
            </g>
          );
        })}

        {/* Display current symbol if available */}
        {lastSymbol && (
            <text x={center} y={center} fill="#FFFFFF" fontSize="24" textAnchor="middle" dominantBaseline="central" fontWeight="bold">
                {lastSymbol}
            </text>
        )}
         {!lastSymbol && !isLoading && (
             <text x={center} y={center} fill="#008000" fontSize="12" textAnchor="middle" dominantBaseline="central">
                N/A
            </text>
         )}
      </svg>
      {keyData && !lastSymbol && keyData.scalar_multiplication_steps && keyData.scalar_multiplication_steps.length > 0 && (
        <p style={{textAlign: 'center', fontSize: '0.9em', color: '#FFA500'}}>
            Note: Final step's symbol could not be determined.
        </p>
      )}
    </section>
  );
};

export default VisualizationView;
