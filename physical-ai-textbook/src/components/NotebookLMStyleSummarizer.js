import React, { useState } from 'react';

const NotebookLMStyleSummarizer = ({ content }) => {
  const [summary, setSummary] = useState('');
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [format, setFormat] = useState('text'); // text, bullet_points, key_points

  const generateSummary = async () => {
    if (!content) return;
    
    setIsSummarizing(true);
    
    try {
      const response = await fetch('/api/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content,
          max_length: 200,
          format: format
        })
      });
      
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error('Error generating summary:', error);
      setSummary('Error generating summary. Please try again.');
    } finally {
      setIsSummarizing(false);
    }
  };

  return (
    <div className="notebooklm-summarizer">
      <div className="summarizer-controls">
        <h4>Generate Summary</h4>
        <div className="format-selector">
          <label>
            <input
              type="radio"
              value="text"
              checked={format === 'text'}
              onChange={(e) => setFormat(e.target.value)}
            />
            Text
          </label>
          <label>
            <input
              type="radio"
              value="bullet_points"
              checked={format === 'bullet_points'}
              onChange={(e) => setFormat(e.target.value)}
            />
            Bullet Points
          </label>
          <label>
            <input
              type="radio"
              value="key_points"
              checked={format === 'key_points'}
              onChange={(e) => setFormat(e.target.value)}
            />
            Key Points
          </label>
        </div>
        <button 
          onClick={generateSummary}
          disabled={isSummarizing || !content}
          className="generate-button"
        >
          {isSummarizing ? 'Generating...' : 'Generate Summary'}
        </button>
      </div>
      
      {summary && (
        <div className="summary-output">
          <h5>Summary:</h5>
          <div className="summary-content">
            {summary}
          </div>
        </div>
      )}
    </div>
  );
};

export default NotebookLMStyleSummarizer;