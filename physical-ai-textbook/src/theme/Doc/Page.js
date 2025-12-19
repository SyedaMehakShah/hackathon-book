import React, { useEffect } from 'react';
import OriginalDocPage from '@theme-original/DocPage';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Head from '@docusaurus/Head';

export default function DocPage(props) {
  const { siteConfig } = useDocusaurusContext();
  
  // Apply cyberpunk styling to documentation pages
  useEffect(() => {
    document.body.classList.add('docusaurus-cyberpunk-doc');
    
    // Add cyberpunk elements to the page
    const cyberpunkElements = document.createElement('div');
    cyberpunkElements.className = 'cyberpunk-doc-overlay';
    cyberpunkElements.innerHTML = `
      <div class="background-container">
        <div class="futuristic-office"></div>
        <div class="glass-panels"></div>
        <div class="floating-code">
          <span class="code-snippet">&lt;html&gt;</span>
          <span class="code-snippet">function() {</span>
          <span class="code-snippet">.class {</span>
          <span class="code-snippet">var x = 5;</span>
          <span class="code-snippet">return x;</span>
          <span class="code-snippet">}&lt;/script&gt;</span>
        </div>
        <div class="particles"></div>
      </div>
      
      <svg class="wire-system" id="wireSystem" width="100%" height="100%"></svg>
      
      <div class="chatbot-orb" id="chatbotOrb">
        <div class="orb-glow"></div>
        <div class="orb-content">AI</div>
        <div class="tooltip">Ask anything from this book</div>
      </div>
    `;
    
    // Insert the cyberpunk elements at the beginning of the body
    document.body.insertBefore(cyberpunkElements, document.body.firstChild);
    
    // Load cyberpunk functionality
    const script = document.createElement('script');
    script.src = './cyberpunk_textbook.js';
    script.async = true;
    document.head.appendChild(script);
    
    // Cleanup on unmount
    return () => {
      document.body.classList.remove('docusaurus-cyberpunk-doc');
      const existingCyberpunk = document.querySelector('.cyberpunk-doc-overlay');
      if (existingCyberpunk) {
        document.body.removeChild(existingCyberpunk);
      }
      document.head.removeChild(script);
    };
  }, []);

  return (
    <>
      <Head>
        <link rel="stylesheet" href="./cyberpunk_textbook.css" />
      </Head>
      <OriginalDocPage {...props} />
    </>
  );
}