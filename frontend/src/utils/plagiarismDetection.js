import Papa from 'papaparse';

function computeCosineSimilarity(text1, text2) {
  // Convert texts to word frequency vectors
  const words1 = text1.toLowerCase().split(/\s+/);
  const words2 = text2.toLowerCase().split(/\s+/);
  
  // Create word frequency maps
  const freqMap1 = new Map();
  const freqMap2 = new Map();
  
  words1.forEach(word => {
    freqMap1.set(word, (freqMap1.get(word) || 0) + 1);
  });
  
  words2.forEach(word => {
    freqMap2.set(word, (freqMap2.get(word) || 0) + 1);
  });
  
  // Get unique words from both texts
  const uniqueWords = new Set([...freqMap1.keys(), ...freqMap2.keys()]);
  
  // Calculate dot product and magnitudes
  let dotProduct = 0;
  let magnitude1 = 0;
  let magnitude2 = 0;
  
  uniqueWords.forEach(word => {
    const freq1 = freqMap1.get(word) || 0;
    const freq2 = freqMap2.get(word) || 0;
    
    dotProduct += freq1 * freq2;
    magnitude1 += freq1 * freq1;
    magnitude2 += freq2 * freq2;
  });
  
  // Calculate cosine similarity
  return dotProduct / (Math.sqrt(magnitude1) * Math.sqrt(magnitude2));
}

function calculateMetrics(actualLabels, predictions) {
  let truePositives = 0;
  let falsePositives = 0;
  let trueNegatives = 0;
  let falseNegatives = 0;
  
  for (let i = 0; i < actualLabels.length; i++) {
    if (actualLabels[i] === 1 && predictions[i] === 1) truePositives++;
    if (actualLabels[i] === 0 && predictions[i] === 1) falsePositives++;
    if (actualLabels[i] === 0 && predictions[i] === 0) trueNegatives++;
    if (actualLabels[i] === 1 && predictions[i] === 0) falseNegatives++;
  }
  
  const accuracy = (truePositives + trueNegatives) / actualLabels.length;
  const precision = truePositives / (truePositives + falsePositives) || 0;
  const recall = truePositives / (truePositives + falseNegatives) || 0;
  const f1Score = 2 * (precision * recall) / (precision + recall) || 0;
  
  return { accuracy, precision, recall, f1Score };
}

export function processFile(file, threshold) {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      complete: (results) => {
        try {
          const similarityScores = results.data.map(row => 
            computeCosineSimilarity(row.Original, row.Suspect)
          );
          
          const predictions = similarityScores.map(score => 
            score > threshold ? 1 : 0
          );
          
          const actualLabels = results.data.map(row => 
            row.Label.toLowerCase() === 'plagiarized' ? 1 : 0
          );
          
          const report = calculateMetrics(actualLabels, predictions);
          
          resolve({
            similarityScores,
            predictions,
            report,
            fileName: file.name,
            threshold
          });
        } catch (error) {
          reject(new Error('Error processing file. Please ensure the CSV contains "Original", "Suspect", and "Label" columns.'));
        }
      },
      error: (error) => {
        reject(new Error(`Error parsing CSV file: ${error.message}`));
      }
    });
  });
}