import React, { createContext, useState, useCallback, useContext } from 'react';
import { fetchKeypairDetailed } from '../services/api';

const DataContext = createContext();

export const useData = () => useContext(DataContext);

export const DataProvider = ({ children }) => {
  const [keyData, setKeyData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateNewKeys = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    setKeyData(null); // Clear previous data
    try {
      const data = await fetchKeypairDetailed();
      setKeyData(data);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred.');
      setKeyData(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <DataContext.Provider value={{ keyData, isLoading, error, generateNewKeys }}>
      {children}
    </DataContext.Provider>
  );
};

export default DataContext;
