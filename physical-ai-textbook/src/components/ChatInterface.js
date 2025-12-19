import React, { useState, useEffect, useRef } from 'react';
import './ChatWidget.css';

const ChatInterface = ({ initialMessages = [] }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState(initialMessages);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Initialize session and load history
  useEffect(() => {
    // Generate or retrieve session ID
    let currentSessionId = localStorage.getItem('chat-session-id');
    if (!currentSessionId) {
      currentSessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('chat-session-id', currentSessionId);
    }
    setSessionId(currentSessionId);

    // Load conversation history from localStorage
    const savedHistory = localStorage.getItem('chat-history');
    if (savedHistory) {
      try {
        setMessages(JSON.parse(savedHistory));
      } catch (e) {
        console.error('Error loading chat history:', e);
      }
    }
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('chat-history', JSON.stringify(messages));
  }, [messages]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString(),
      sessionId: sessionId
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare context if there's selected text
      let response;
      if (selectedText) {
        // Use the answer-highlighted endpoint
        response = await fetch('http://localhost:8000/api/answer-highlighted', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            highlighted_text: selectedText,
            question: inputValue
          })
        });
        const data = await response.json();
        const botMessage = {
          id: Date.now() + 1,
          text: data.answer,
          sender: 'bot',
          explanation: data.explanation,
          timestamp: new Date().toISOString(),
          sessionId: sessionId
        };
        setMessages(prev => [...prev, botMessage]);
        setSelectedText(''); // Clear selected text after use
      } else {
        // Use the global RAG query endpoint which matches the backend implementation
        response = await fetch('http://localhost:8000/api/rag/query-global', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question: inputValue,
            book_id: 'physical-ai-textbook', // Default book ID for our textbook
            session_id: sessionId
          })
        });
        const data = await response.json();
        const botMessage = {
          id: Date.now() + 1,
          text: data.answer,
          sender: 'bot',
          sources: data.sources || [],
          confidence: data.confidence || 0,
          timestamp: new Date().toISOString(),
          sessionId: sessionId
        };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date().toISOString(),
        sessionId: sessionId,
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearHistory = () => {
    setMessages([]);
    localStorage.removeItem('chat-history');
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  };

  return (
    <div className="chat-container">
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <h3>Textbook Assistant</h3>
            <div className="header-controls">
              <button
                className="chat-clear-history"
                onClick={clearHistory}
                aria-label="Clear chat history"
                title="Clear conversation history"
              >
                🗑️
              </button>
              <button className="chat-close" onClick={toggleChat} aria-label="Close chat">
                ×
              </button>
            </div>
          </div>

          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="chat-welcome">
                <p>Hello! I'm your Physical AI & Humanoid Robotics textbook assistant.</p>
                <p>Ask me anything about the content, or select text and ask related questions.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
                >
                  <div className="message-content">
                    <p>{message.text}</p>
                    {message.explanation && (
                      <small className="explanation">{message.explanation}</small>
                    )}
                    {message.sources && message.sources.length > 0 && (
                      <div className="sources">
                        <strong>Sources:</strong>
                        <ul>
                          {message.sources.slice(0, 3).map((source, index) => (
                            <li key={index} className="source-item">
                              {source.length > 50 ? `${source.substring(0, 50)}...` : source}
                            </li>
                          ))}
                        </ul>
                        {message.sources.length > 3 && (
                          <small>and {message.sources.length - 3} more sources</small>
                        )}
                      </div>
                    )}
                    {message.confidence && (
                      <small className="confidence">Confidence: {(message.confidence * 100).toFixed(1)}%</small>
                    )}
                    {message.isError && (
                      <small className="error">Error occurred - please try again</small>
                    )}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-content">
                  <p>Thinking...</p>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {selectedText && (
            <div className="selected-text-preview">
              <small>Context: "{selectedText.substring(0, 60)}{selectedText.length > 60 ? '...' : ''}"</small>
            </div>
          )}

          <form className="chat-input-form" onSubmit={handleSubmit}>
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about the textbook..."
              disabled={isLoading}
              aria-label="Type your message"
            />
            <button type="submit" disabled={isLoading || !inputValue.trim()}>
              {isLoading ? 'Sending...' : '→'}
            </button>
          </form>
        </div>
      )}

      {!isOpen && (
        <button className="chat-toggle-button" onClick={toggleChat} aria-label="Open chat">
          💬
        </button>
      )}
    </div>
  );
};

export default ChatInterface;