import React from 'react';
import { useLocation } from '@docusaurus/router';

interface ChapterContentProps {
  content: string;
}

const ChapterContent: React.FC<ChapterContentProps> = ({ content }) => {
  const location = useLocation();

  // Function to handle text selection and send to RAG system
  const handleTextSelection = () => {
    const selectedText = window.getSelection()?.toString().trim();
    if (selectedText) {
      // In a real implementation, this would send the selected text to the RAG API
      console.log('Selected text:', selectedText);
      // This might open the chat interface with the selected text as context
      // For now, we'll just log it
    }
  };

  // Add event listener for mouseup to detect text selection
  React.useEffect(() => {
    const handleSelection = () => {
      setTimeout(() => {
        const selectedText = window.getSelection()?.toString().trim();
        if (selectedText) {
          handleTextSelection();
        }
      }, 0);
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, [location.pathname]); // Re-run when route changes

  return (
    <div className="chapter-content">
      <div 
        className="markdown-content"
        dangerouslySetInnerHTML={{ __html: content }} 
      />
    </div>
  );
};

export default ChapterContent;