import React, { useEffect } from 'react';
import ChatInterface from '../components/ChatInterface';

const ChatWidget = () => {
  // Initialize the chat widget when the component mounts
  useEffect(() => {
    // Any initialization code for the widget can go here
    console.log('Chat widget initialized');
  }, []);

  return (
    <div className="chat-widget-container">
      <ChatInterface />
    </div>
  );
};

// Export as a Docusaurus plugin component
export default ChatWidget;

// Widget configuration
export const widgetConfig = {
  name: 'textbook-assistant',
  displayName: 'Textbook Assistant',
  description: 'An AI-powered assistant for the Physical AI & Humanoid Robotics textbook',
  defaultProps: {
    initialMessages: [],
    enableTextSelection: true,
    enableContext: true,
    position: { bottom: '20px', right: '20px' },
  }
};