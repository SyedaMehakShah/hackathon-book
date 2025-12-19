import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import {useLocation} from '@docusaurus/router';
import GlobalComponents from '@site/src/components/GlobalComponents';

// Accessibility utilities
const AccessibilityUtilities = () => {
  // Ensure proper focus management
  React.useEffect(() => {
    // Add skip link functionality
    const handleKeyDown = (e) => {
      if (e.key === 'Tab' || e.keyCode === 9) {
        document.body.classList.add('keyboard-nav');
      }
    };

    const handleMouseDown = () => {
      document.body.classList.remove('keyboard-nav');
    };

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('mousedown', handleMouseDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('mousedown', handleMouseDown);
    };
  }, []);

  return null;
};

// Skip to content link
const SkipToContentLink = () => {
  const skipLinkRef = React.useRef(null);

  const onClick = (e) => {
    e.preventDefault();
    const mainContent = document.querySelector('#main-content');
    if (mainContent) {
      mainContent.focus();
      mainContent.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <a
      href="#main-content"
      ref={skipLinkRef}
      className="skip-to-content-link"
      onClick={onClick}
      style={{
        position: 'absolute',
        top: '-40px',
        left: 0,
        background: '#000',
        color: '#fff',
        padding: '8px',
        zIndex: 1000,
        textDecoration: 'none',
      }}
    >
      Skip to main content
    </a>
  );
};

// Accessible layout wrapper
export default function Layout(props) {
  const location = useLocation();

  // Add landmark roles for accessibility
  React.useEffect(() => {
    const pageContent = document.querySelector('main');
    if (pageContent) {
      pageContent.setAttribute('role', 'main');
      pageContent.setAttribute('id', 'main-content');
      pageContent.setAttribute('tabindex', '-1');
    }
  }, [location.pathname]);

  return (
    <>
      <SkipToContentLink />
      <AccessibilityUtilities />
      <OriginalLayout {...props} />
      <GlobalComponents />
    </>
  );
}