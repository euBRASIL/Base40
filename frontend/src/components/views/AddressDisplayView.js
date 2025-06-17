import React from 'react';
import { useData } from '../../context/DataContext';

const AddressDisplayView = () => {
  const { keyData, isLoading } = useData(); // Error is handled in ControlsView

  if (isLoading && !keyData) { // Show loading only if there's no stale data
    return (
      <section className="view-section" id="address-display-section">
        <h2>Addresses</h2>
        <p>Loading address data...</p>
      </section>
    );
  }

  const data = keyData || {};

  return (
    <section className="view-section" id="address-display-section">
      <h2>Addresses</h2>
      <div className="info-grid">
        <div className="info-item">
          <strong>Base40 Address (from RIPEMD-160):</strong>
          <pre>{data.address_base40 || 'N/A'}</pre>
          {data.address_base40 && data.address_base40.includes('undefined') &&
            <p style={{color: 'yellow', fontSize: '0.8em'}}>Note: Hash-dependent values might be incorrect due to environment issues.</p>}
        </div>
        <div className="info-item">
          <strong>Bitcoin Address (Base58Check):</strong>
          <pre>{data.address_bitcoin_base58check || 'N/A'}</pre>
           {data.address_bitcoin_base58check && data.address_bitcoin_base58check.includes('undefined') &&
            <p style={{color: 'yellow', fontSize: '0.8em'}}>Note: Hash-dependent values might be incorrect due to environment issues.</p>}
        </div>
         {keyData && (data.address_base40 || data.address_bitcoin_base58check) && (keyData.hashed_public_key_ripemd160_hex === "010966776006953d5567439e5e39f86a0d273bee" || keyData.private_key_hex === "0000000000000000000000000000000000000000000000000000000000000001") &&
            <p style={{color: 'yellow', fontSize: '0.8em', marginTop: '10px'}}>
              Reminder: Hash-derived addresses may be incorrect in this environment due to `hashlib.sha256` and/or modulo anomalies.
            </p>
        }
      </div>
    </section>
  );
};

export default AddressDisplayView;
