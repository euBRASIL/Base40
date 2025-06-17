import React from 'react';
import { useData } from '../../context/DataContext';
import { exportToJson, exportToCsv } from '../../utils/exportUtils'; // Import export functions

const ControlsView = () => {
  const { generateNewKeys, isLoading, error, keyData } = useData();

  const handleGenerateKeys = () => {
    generateNewKeys();
  };

  const handleExportJson = () => {
    if (keyData) {
      exportToJson(keyData, 'base40_keypair_data.json');
    } else {
      alert('No data to export. Please generate keys first.');
    }
  };

  const handleExportCsv = () => {
    if (keyData && keyData.scalar_multiplication_steps) {
      exportToCsv(keyData.scalar_multiplication_steps, 'base40_scalar_steps.csv');
    } else {
      alert('No step data to export. Please generate keys first.');
    }
  };

  return (
    <section className="view-section" id="controls-section">
      <h2>Controls</h2>
      <button onClick={handleGenerateKeys} disabled={isLoading}>
        {isLoading ? 'Generating...' : 'Generate New Key Pair'}
      </button>
      <button onClick={handleExportJson} disabled={!keyData || isLoading}>
        Export JSON
      </button>
      <button onClick={handleExportCsv} disabled={!keyData || isLoading || !keyData.scalar_multiplication_steps}>
        Export Steps CSV
      </button>

      {error && <p style={{ color: '#FF0000', marginTop: '10px' }}>Error: {error}</p>}
    </section>
  );
};

export default ControlsView;
