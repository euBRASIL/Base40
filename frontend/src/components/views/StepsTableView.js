import React from 'react';
import { useData } from '../../context/DataContext';

const StepsTableView = () => {
  const { keyData, isLoading } = useData();

  if (isLoading && !keyData) {
    return (
      <section className="view-section" id="steps-table-section">
        <h2>Scalar Multiplication Steps (256)</h2>
        <p>Loading steps data...</p>
      </section>
    );
  }

  const steps = keyData?.scalar_multiplication_steps;

  if (!steps || steps.length === 0) {
    return (
      <section className="view-section" id="steps-table-section">
        <h2>Scalar Multiplication Steps (256)</h2>
        <p>No scalar multiplication steps to display. Generate keys first.</p>
      </section>
    );
  }

  return (
    <section className="view-section" id="steps-table-section">
      <h2>Scalar Multiplication Steps (256)</h2>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Step</th>
              <th>Bit</th>
              <th>Operation</th>
              <th>Point X (Hex)</th>
              <th>Point Y (Hex)</th>
              <th>B40 Angle</th>
              <th>B40 Symbol</th>
              <th>Rodopios</th>
            </tr>
          </thead>
          <tbody>
            {steps.map((step, index) => (
              <tr key={step.step_number || index}> {/* Fallback to index if step_number is missing */}
                <td>{step.step_number !== undefined ? step.step_number : index + 1}</td>
                <td>{step.bit_value !== undefined ? step.bit_value : 'N/A'}</td>
                <td>{step.operation || 'N/A'}</td>
                <td>{step.point_value_hex?.x || (step.point_value === null ? 'Infinity' : 'N/A')}</td>
                <td>{step.point_value_hex?.y || (step.point_value === null ? 'Infinity' : 'N/A')}</td>
                <td>{step.base40_angle !== null && step.base40_angle !== undefined ? step.base40_angle : 'N/A'}</td>
                <td>{step.base40_symbol || 'N/A'}</td>
                <td>{step.rodopios !== null && step.rodopios !== undefined ? step.rodopios : 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default StepsTableView;
