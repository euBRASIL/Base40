// frontend/src/services/api.js

// The backend URL. If your Flask app is running on a different port or host,
// update this. For development, Flask often runs on port 5000.
// Create React App dev server usually runs on port 3000.
// To avoid CORS issues in development, you can proxy requests from the
// React dev server to the Flask backend. This is configured in package.json:
// "proxy": "http://localhost:5000" (or your Flask backend URL)
// If using proxy, the fetch URL can be relative: '/api/generate_keypair_detailed'

const API_BASE_URL = '/api'; // Assuming proxy is set up or same origin

/**
 * Fetches detailed key pair information from the backend API.
 * @returns {Promise<Object>} A promise that resolves to the JSON data from the API.
 *                            The structure includes private/public keys, addresses,
 *                            and scalar multiplication steps.
 * @throws {Error} If the network response is not ok or if fetching fails.
 */
export const fetchKeypairDetailed = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/generate_keypair_detailed`);

    if (!response.ok) {
      // Try to parse error details from backend if available
      let errorDetails = 'Network response was not ok.';
      try {
        const errorData = await response.json();
        errorDetails = errorData.error || errorData.details || errorDetails;
      } catch (e) {
        // Could not parse JSON, stick with the network error
      }
      throw new Error(`API Error: ${errorDetails} (Status: ${response.status})`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error("Failed to fetch keypair details:", error);
    // Re-throw the error so the calling component can handle it (e.g., display an error message)
    throw error;
  }
};

// Example of how you might add other API calls in the future:
// export const anotherApiCall = async (params) => { ... };
