import React from 'react';
import { FileText } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import '../styles/Header.css';

export const Header = () => {
  const { theme, toggleTheme } = useTheme();
  
  return (
    <header className="header">
      <div className="logo">
        <FileText size={28} />
        <h1>PlagiarismDetect</h1>
      </div> 
      <button 
        className="theme-toggle" 
        onClick={toggleTheme}
        aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      >
        {theme === 'light' ? '🌙' : '☀️'}
      </button>
    </header>
  );
};