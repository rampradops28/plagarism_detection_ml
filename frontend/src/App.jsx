
import React, { useState } from 'react';
import axios from 'axios';
import { FileUpload } from './components/FileUpload';
import { ResultsDisplay } from './components/ResultsDisplay';
import { Header } from './components/Header';
import { ThemeProvider } from './context/ThemeContext'; 
import './styles/App.css';

function App() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileAnalysis = async (file, threshold) => {
    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('threshold', threshold);  

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data && response.status === 200) {
        setResults(response.data);
      } else {
        setError('Unexpected response from server. Please try again.');
      }
    } catch (err) {
      setError(err?.response?.data?.message || 'Error occurred during analysis. Please check your file format and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ThemeProvider>
      <div className="app">
        <Header />
        
        <main className="main-content"> 
          <section className="hero-section">
            <h1>AI-Powered Plagiarism Detection</h1>
            <p>
              Upload your dataset in CSV format. Our system uses <strong>BERT embeddings</strong> and <strong>ML classifiers</strong> 
              to detect content plagiarism with high accuracy.
            </p>
          </section>
 
          <FileUpload onAnalyze={handleFileAnalysis} isLoading={isLoading} />
 
          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}
 
          {results && !isLoading && (
            <ResultsDisplay results={results} />
          )}
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App;
