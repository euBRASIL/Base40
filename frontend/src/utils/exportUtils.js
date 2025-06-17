// frontend/src/utils/exportUtils.js

/**
 * Triggers a browser download for the given data as a file.
 * @param {string} data The string content of the file.
 * @param {string} filename The desired name of the file.
 * @param {string} type The MIME type of the file (e.g., 'application/json', 'text/csv').
 */
function triggerDownload(data, filename, type) {
  const blob = new Blob([data], { type: `${type};charset=utf-8;` });
  const link = document.createElement('a');
  if (link.download !== undefined) { // feature detection
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  } else {
    // Fallback for older browsers (less common now)
    alert("Your browser doesn't support direct file downloads. Please try a modern browser.");
  }
}

/**
 * Exports data to a JSON file and triggers a download.
 * @param {object} data The JavaScript object to export.
 * @param {string} filename The desired filename (e.g., 'data.json').
 */
export const exportToJson = (data, filename) => {
  if (!data) {
    console.error('No data provided for JSON export.');
    return;
  }
  try {
    const jsonString = JSON.stringify(data, null, 2); // Pretty print JSON
    triggerDownload(jsonString, filename, 'application/json');
  } catch (error) {
    console.error('Error converting data to JSON:', error);
    alert('Failed to export JSON. See console for details.');
  }
};

/**
 * Converts an array of step objects to a CSV string.
 * @param {Array<object>} stepsData The array of scalar multiplication step objects.
 * @returns {string} The CSV formatted string.
 */
function stepsToCsvString(stepsData) {
  if (!stepsData || stepsData.length === 0) {
    return '';
  }

  const headers = [
    'Step', 'Bit', 'Operation',
    'Point_X_Hex', 'Point_Y_Hex',
    'Base40_Angle', 'Base40_Symbol', 'Rodopios'
  ];

  const csvRows = [headers.join(',')]; // Header row

  stepsData.forEach(step => {
    const row = [
      step.step_number !== undefined ? step.step_number : '',
      step.bit_value !== undefined ? `"${step.bit_value}"` : '', // Enclose bit value in quotes if it might be just '0' or '1'
      `"${step.operation || ''}"`,
      `"${step.point_value_hex?.x || (step.point_value === null ? 'Infinity' : '')}"`,
      `"${step.point_value_hex?.y || (step.point_value === null ? 'Infinity' : '')}"`,
      step.base40_angle !== null && step.base40_angle !== undefined ? step.base40_angle : '',
      `"${step.base40_symbol || ''}"`,
      step.rodopios !== null && step.rodopios !== undefined ? step.rodopios : ''
    ];
    csvRows.push(row.join(','));
  });

  return csvRows.join('\n');
}

/**
 * Exports scalar multiplication steps data to a CSV file and triggers a download.
 * @param {Array<object>} stepsData The array of step objects to export.
 * @param {string} filename The desired filename (e.g., 'steps.csv').
 */
export const exportToCsv = (stepsData, filename) => {
  if (!stepsData) {
    console.error('No data provided for CSV export.');
    return;
  }
  try {
    const csvString = stepsToCsvString(stepsData);
    if (csvString) {
      triggerDownload(csvString, filename, 'text/csv');
    } else {
      alert('No data to create CSV from.');
    }
  } catch (error) {
    console.error('Error converting data to CSV:', error);
    alert('Failed to export CSV. See console for details.');
  }
};
