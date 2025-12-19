import React from 'react';
import ChatWidget from './ChatWidget';

// This component wraps the entire application to provide global functionality
const GlobalComponents = ({ children }) => {
  return (
    <>
      <ChatWidget />
      {children}
    </>
  );
};

export default GlobalComponents;