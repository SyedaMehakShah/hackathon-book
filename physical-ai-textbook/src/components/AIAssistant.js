import React, { useState, useEffect } from 'react';
import './AIAssistant.css';

const AIAssistant = ({ initialAgents = [] }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [task, setTask] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [agents, setAgents] = useState(initialAgents);

  const executeAgentTask = async () => {
    if (!selectedAgent || !task.trim()) return;

    setIsLoading(true);
    setResult(null);

    try {
      // In a real implementation, this would call the agent orchestrator
      // For now, we'll simulate the response with a timeout
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Mock response based on the task
      let mockResult;
      if (task.toLowerCase().includes('translate')) {
        mockResult = {
          success: true,
          translated_content: `[MOCK TRANSLATION] ${task.substring(0, 30)}... translated`,
          target_language: 'ur'
        };
      } else if (task.toLowerCase().includes('search') || task.toLowerCase().includes('find')) {
        mockResult = {
          success: true,
          query: task,
          results: [
            { id: 1, title: 'Mock Result 1', content: 'This is a mock result...' },
            { id: 2, title: 'Mock Result 2', content: 'This is another mock result...' }
          ]
        };
      } else {
        mockResult = {
          success: true,
          answer: `Mock answer to: "${task}"`,
          sources: ['mock-source-1', 'mock-source-2']
        };
      }

      setResult(mockResult);
    } catch (error) {
      setResult({
        success: false,
        error: 'Error executing agent task. Please try again.'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const toggleAssistant = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="ai-assistant-container">
      {isOpen && (
        <div className="ai-assistant-window">
          <div className="ai-assistant-header">
            <h3>AI Agent Assistant</h3>
            <button className="ai-assistant-close" onClick={toggleAssistant} aria-label="Close assistant">
              ×
            </button>
          </div>
          
          <div className="ai-assistant-content">
            <div className="agent-selector">
              <label>Select an Agent:</label>
              <select 
                value={selectedAgent?.id || ''} 
                onChange={(e) => {
                  const agent = agents.find(a => a.id === e.target.value);
                  setSelectedAgent(agent || null);
                }}
              >
                <option value="">Choose an agent...</option>
                {agents.map(agent => (
                  <option key={agent.id} value={agent.id}>
                    {agent.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="task-input">
              <label>Enter your task:</label>
              <textarea
                value={task}
                onChange={(e) => setTask(e.target.value)}
                placeholder="e.g., 'Find information about ROS 2', 'Translate this chapter to Urdu', 'Answer: What is embodied intelligence?'"
                rows={3}
              />
            </div>
            
            <button 
              onClick={executeAgentTask} 
              disabled={isLoading || !selectedAgent || !task.trim()}
              className="execute-task-button"
            >
              {isLoading ? 'Processing...' : 'Execute Task'}
            </button>
            
            {result && (
              <div className={`result-container ${result.success ? 'success' : 'error'}`}>
                <h4>Result:</h4>
                {result.success ? (
                  <div className="result-content">
                    {result.answer && <p><strong>Answer:</strong> {result.answer}</p>}
                    {result.translated_content && (
                      <div>
                        <p><strong>Translated Content:</strong></p>
                        <p>{result.translated_content}</p>
                        <p><strong>Target Language:</strong> {result.target_language}</p>
                      </div>
                    )}
                    {result.results && (
                      <div>
                        <p><strong>Search Results:</strong></p>
                        <ul>
                          {result.results.map((res, index) => (
                            <li key={index}>
                              <strong>{res.title}:</strong> {res.content}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {result.sources && (
                      <p><strong>Sources:</strong> {result.sources.join(', ')}</p>
                    )}
                  </div>
                ) : (
                  <p className="error-message">{result.error}</p>
                )}
              </div>
            )}
          </div>
        </div>
      )}
      
      {!isOpen && (
        <button className="ai-assistant-toggle" onClick={toggleAssistant} aria-label="Open AI assistant">
          🤖
        </button>
      )}
    </div>
  );
};

export default AIAssistant;