import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { HtmlClassNameProvider } from '@docusaurus/theme-common';

// Cyberpunk-themed landing page component
export default function CyberpunkLanding() {
  const { siteConfig } = useDocusaurusContext();

  useEffect(() => {
    // Add cyberpunk styling to the body
    document.body.classList.add('cyberpunk-landing');

    // Dynamically load the cyberpunk functionality
    const script = document.createElement('script');
    script.src = './cyberpunk_textbook.js';
    script.async = true;
    document.body.appendChild(script);

    // Cleanup on unmount
    return () => {
      document.body.classList.remove('cyberpunk-landing');
      document.body.removeChild(script);
    };
  }, []);

  return (
    <HtmlClassNameProvider className="cyberpunk-landing">
      <Layout>
        <div className="cyberpunk-container">
          {/* Background Elements */}
          <div className="background-container">
            <div className="futuristic-office"></div>
            <div className="glass-panels"></div>
            <div className="floating-code">
              <span className="code-snippet">&lt;html&gt;</span>
              <span className="code-snippet">function() {'{'}</span>
              <span className="code-snippet">.class {'{'}</span>
              <span className="code-snippet">var x = 5;</span>
              <span className="code-snippet">return x;</span>
              <span className="code-snippet">{'}'}</span>
              <span className="code-snippet">&lt;/script&gt;</span>
            </div>
            <div className="particles"></div>
          </div>

          {/* Wire System Container */}
          <svg className="wire-system" id="wireSystem" width="100%" height="100%"></svg>

          {/* Main Content Container */}
          <div className="main-container">
            {/* Central Textbook */}
            <div className="textbook-container" id="textbookContainer">
              <div className="book" id="textbook">
                <div className="book-cover">
                  <div className="circuit-pattern"></div>
                  <div className="ai-chip"></div>
                  <h1 className="book-title">CYBER TEXTBOOK</h1>
                  <p className="subtitle">AI-Powered Learning System</p>
                </div>
                <div className="book-pages">
                  <div className="page"></div>
                  <div className="page"></div>
                </div>
                <div className="book-spine"></div>
              </div>
            </div>

            {/* Glassmorphism Buttons */}
            <div className="button-container" id="buttonContainer">
              <button className="glass-button" id="readButton">
                <span className="button-icon">📘</span>
                <span className="button-text">Read Textbook</span>
                <span className="micro-text">Access full content</span>
              </button>

              <button className="glass-button" id="chatButton">
                <span className="button-icon">🤖</span>
                <span className="button-text">Ask AI</span>
                <span className="micro-text">AI-powered explanations</span>
              </button>

              <button className="glass-button" id="exploreButton">
                <span className="button-icon">🧠</span>
                <span className="button-text">Explore Concepts</span>
                <span className="micro-text">Deep-dive into topics</span>
              </button>

              <button className="glass-button" id="labButton">
                <span className="button-icon">⚙️</span>
                <span className="button-text">Frontend Lab</span>
                <span className="micro-text">Interactive examples</span>
              </button>

              <button className="glass-button" id="chaptersButton">
                <span className="button-icon">📂</span>
                <span className="button-text">View Chapters</span>
                <span className="micro-text">Browse content</span>
              </button>
            </div>

            {/* Floating AI Chatbot Orb */}
            <div className="chatbot-orb" id="chatbotOrb">
              <div className="orb-glow"></div>
              <div className="orb-content">AI</div>
              <div className="tooltip">Ask anything from this book</div>
            </div>

            {/* Cursor Effect */}
            <div className="cursor-glow" id="cursorGlow"></div>
          </div>

          {/* Chat Interface (Hidden by default) */}
          <div className="chat-interface" id="chatInterface">
            <div className="chat-header">
              <h3>AI Assistant</h3>
              <button className="close-chat" id="closeChat">close</button>
            </div>
            <div className="chat-messages" id="chatMessages">
              <div className="message ai-message">
                Hello! I'm your AI assistant. Ask me anything about the textbook content.
              </div>
            </div>
            <div className="chat-input-area">
              <input type="text" id="userInput" placeholder="Ask a question about the textbook..." />
              <button id="sendButton">Send</button>
            </div>
          </div>
        </div>
      </Layout>
    </HtmlClassNameProvider>
  );
}