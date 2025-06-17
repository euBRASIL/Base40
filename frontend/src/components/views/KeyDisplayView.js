import React from 'react';
import { useData } from '../../context/DataContext';

const KeyDisplayView = () => {
  const { keyData, isLoading, error } = useData();

  if (isLoading) {
    return (
      <section className="view-section" id="key-display-section">
        <h2>Key Information</h2>
        <p>Loading key data...</p>
      </section>
    );
  }

  // No error check here, as error is displayed in ControlsView.
  // If keyData is null (initial state or after an error), show placeholders.
  const data = keyData || {}; // Use empty object if keyData is null to avoid errors accessing properties

  return (
    <section className="view-section" id="key-display-section">
      <h2>Key Information</h2>
      <div className="info-grid">
        <div className="info-item">
          <strong>Private Key (Hex):</strong>
          <pre>{data.private_key_hex || 'N/A'}</pre>
        </div>
        <div className="info-item">
          <strong>Private Key (Base40):</strong>
          <pre>{data.private_key_base40 || 'N/A'}</pre>
        </div>
        <div className="info-item">
          <strong>Public Key (Uncompressed Hex):</strong>
          <pre style={{wordBreak: 'break-all'}}>{data.public_key_uncompressed_hex || 'N/A'}</pre>
        </div>
        <div className="info-item">
          <strong>Public Key X-Coordinate (Base40):</strong>
          <pre>{data.public_key_x_base40 || 'N/A'}</pre>
        </div>
      </div>
    </section>
  );
};

export default KeyDisplayView;
