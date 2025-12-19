import React from "react";
import { useLocation } from '@docusaurus/router';
import { useEffect } from 'react';

export default function Home() {
  const location = useLocation();

  useEffect(() => {
    // Redirect to the simple dark-themed landing page
    window.location.href = '/simple-landing';
  }, [location.pathname]);

  return null;
}
