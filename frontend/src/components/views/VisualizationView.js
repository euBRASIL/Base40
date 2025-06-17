import React, { useState, useEffect, useRef } from 'react';
import { useData } from '../../context/DataContext';
import { DEFAULT_SYMBOLS } from '../../core_logic_bridge';

const VisualizationView = () => {
  const { keyData, isLoading } = useData();
  const [currentAnimatedSymbol, setCurrentAnimatedSymbol] = useState(null);
  const [currentAnimatedStepIndex, setCurrentAnimatedStepIndex] = useState(-1);
  const animationTimeoutRef = useRef(null); // To store timeout ID for cleanup

  const svgSize = 320;
  const center = svgSize / 2;
  const radius = svgSize * 0.4;
  const symbolRadius = svgSize * 0.45;
  const animationSpeedMs = 75; // milliseconds per step in animation

  const symbolsToUse = typeof DEFAULT_SYMBOLS !== 'undefined' ? DEFAULT_SYMBOLS :
    Array.from({length: 40}, (_, i) => String.fromCharCode(65 + i));

  const getCoordinatesForAngle = (angleDegrees, r) => {
    const angleRadians = (angleDegrees - 90) * (Math.PI / 180);
    return {
      x: center + r * Math.cos(angleRadians),
      y: center + r * Math.sin(angleRadians),
    };
  };

  useEffect(() => {
    // Clear any existing animation timeout when component unmounts or keyData changes
    if (animationTimeoutRef.current) {
      clearTimeout(animationTimeoutRef.current);
    }
    setCurrentAnimatedStepIndex(-1); // Reset animation index
    setCurrentAnimatedSymbol(null); // Reset displayed symbol

    const steps = keyData?.scalar_multiplication_steps;
    if (steps && steps.length > 0) {
      let animIndex = 0;

      const animateNextStep = () => {
        if (animIndex < steps.length) {
          const step = steps[animIndex];
          setCurrentAnimatedSymbol(step.base40_symbol || null); // Update symbol in center
          setCurrentAnimatedStepIndex(animIndex); // To highlight the line in SVG

          animIndex++;
          animationTimeoutRef.current = setTimeout(animateNextStep, animationSpeedMs);
        } else {
          // Animation finished, keep the last step's symbol highlighted and in center
          if (steps.length > 0) {
            setCurrentAnimatedSymbol(steps[steps.length -1].base40_symbol || null);
            setCurrentAnimatedStepIndex(steps.length -1);
          } else {
            setCurrentAnimatedStepIndex(-1);
            setCurrentAnimatedSymbol(null);
          }
        }
      };

      animateNextStep(); // Start the animation
    } else {
      // No steps or keyData, reset
      setCurrentAnimatedStepIndex(-1);
      setCurrentAnimatedSymbol(null);
    }

    // Cleanup function to clear timeout when component unmounts or dependencies change
    return () => {
      if (animationTimeoutRef.current) {
        clearTimeout(animationTimeoutRef.current);
      }
    };
  }, [keyData]); // Rerun effect if keyData changes

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
        <circle cx={center} cy={center} r={radius * 1.05} fill="none" stroke="#005000" strokeWidth="1" />
        <circle cx={center} cy={center} r={radius * 0.2} fill="#050505" stroke="#008000" strokeWidth="1" />

        {symbolsToUse.map((symbol, index) => {
          const angle = index * 9;
          const startCoords = getCoordinatesForAngle(angle, radius * 0.2);
          const endCoords = getCoordinatesForAngle(angle, radius);
          const symbolCoords = getCoordinatesForAngle(angle, symbolRadius);

          let isHighlighted = false;
          if (keyData && keyData.scalar_multiplication_steps && currentAnimatedStepIndex !== -1) {
             const currentStepData = keyData.scalar_multiplication_steps[currentAnimatedStepIndex];
             if (currentStepData && currentStepData.base40_symbol === symbol) {
                 isHighlighted = true;
             }
          }


          return (
            <g key={index}>
              <line
                x1={startCoords.x}
                y1={startCoords.y}
                x2={endCoords.x}
                y2={endCoords.y}
                stroke={isHighlighted ? "#FFFF00" : "#00FF00"}
                strokeWidth={isHighlighted ? "3" : "1.5"}
              />
              <text
                x={symbolCoords.x}
                y={symbolCoords.y}
                fill={isHighlighted ? "#FFFF00" : "#00FF00"}
                fontSize="11"
                textAnchor="middle"
                dominantBaseline="middle"
                style={{ pointerEvents: 'none' }}
              >
                {symbol}
              </text>
              <circle cx={endCoords.x} cy={endCoords.y} r="2" fill={isHighlighted ? "#FFFF00" : "#00FF00"} />
            </g>
          );
        })}

        {currentAnimatedSymbol && (
            <text x={center} y={center} fill="#FFFFFF" fontSize="24" textAnchor="middle" dominantBaseline="central" fontWeight="bold">
                {currentAnimatedSymbol}
            </text>
        )}
         {!currentAnimatedSymbol && !isLoading && (!keyData || !keyData.scalar_multiplication_steps || keyData.scalar_multiplication_steps.length === 0) && (
             <text x={center} y={center} fill="#008000" fontSize="12" textAnchor="middle" dominantBaseline="central">
                N/A
            </text>
         )}
      </svg>
      {/* Optional: Display current animation step number for debugging/info */}
      {/* {currentAnimatedStepIndex !== -1 && keyData &&
        <p style={{textAlign: 'center', fontSize: '0.9em'}}>Animating Step: {currentAnimatedStepIndex + 1} / {keyData.scalar_multiplication_steps.length}</p>
      } */}
    </section>
  );
};

export default VisualizationView;
