import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { HtmlClassNameProvider } from '@docusaurus/theme-common';

export default function Landing() {
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
        {/* Background Elements */}
        <div className="background-container">
          <div className="futuristic-office"></div>
          <div className="glass-panels"></div>
          <div className="floating-code">
            <span className="code-snippet">&lt;html&gt;</span>
            <span className="code-snippet">function() </span>
            <span className="code-snippet">.class </span>
            <span className="code-snippet">var x = 5;</span>
            <span className="code-snippet">return x;</span>
            <span className="code-snippet">&lt;/script&gt;</span>
          </div>
          <div className="particles"></div>
        </div>

        {/* Wire System Container */}
        <svg className="wire-system" id="wireSystem" width="100%" height="100%"></svg>

        <div className="cyberpunk-container" style={{ position: 'relative', zIndex: 10 }}>
          <div className="container" style={{ padding: '4rem 0' }}>
            <div className="row">
              <div className="col col--8 col--offset-2">
                <h1 style={{
                  textAlign: 'center',
                  fontSize: '3rem',
                  marginBottom: '2rem',
                  fontFamily: "'Orbitron', sans-serif",
                  color: '#00ffff',
                  textShadow: '0 0 10px #00ffff'
                }}>
                  Ready to Master Physical AI & Humanoid Robotics?
                </h1>

                <p style={{
                  textAlign: 'center',
                  fontSize: '1.2rem',
                  lineHeight: '1.6',
                  marginBottom: '3rem',
                  color: 'white'
                }}>
                  Join thousands of students and professionals learning the cutting-edge techniques in embodied intelligence,
                  ROS 2, simulation environments, and NVIDIA Isaac technologies.
                </p>

                <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
                  <Link
                    className="button button--primary button--lg glass-button"
                    to="/docs/intro"
                    style={{
                      background: 'rgba(30, 30, 46, 0.3)',
                      backdropFilter: 'blur(10px)',
                      border: '1px solid rgba(0, 255, 255, 0.3)',
                      borderRadius: '12px',
                      padding: '1rem 1.5rem',
                      color: 'white',
                      fontFamily: "'Space Grotesk', sans-serif",
                      fontSize: '1rem',
                      fontWeight: '500',
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '0.8rem',
                      textDecoration: 'none'
                    }}
                  >
                    Start Learning Today
                  </Link>
                </div>

                <div className="text--center" style={{ marginTop: '3rem' }}>
                  <h2 style={{
                    fontFamily: "'Orbitron', sans-serif",
                    color: '#00ffff',
                    textShadow: '0 0 10px #00ffff'
                  }}>What You'll Learn</h2>
                  <div className="row" style={{ marginTop: '2rem' }}>
                    <div className="col col--4">
                      <h3 style={{
                        fontFamily: "'Orbitron', sans-serif",
                        color: '#ff00ff',
                        textShadow: '0 0 5px #ff00ff'
                      }}>Embodied Intelligence</h3>
                      <p style={{ color: 'white' }}>Explore how intelligence emerges from interaction with the physical world.</p>
                    </div>
                    <div className="col col--4">
                      <h3 style={{
                        fontFamily: "'Orbitron', sans-serif",
                        color: '#ff00ff',
                        textShadow: '0 0 5px #ff00ff'
                      }}>ROS 2 Fundamentals</h3>
                      <p style={{ color: 'white' }}>Master the Robot Operating System for building robotics applications.</p>
                    </div>
                    <div className="col col--4">
                      <h3 style={{
                        fontFamily: "'Orbitron', sans-serif",
                        color: '#ff00ff',
                        textShadow: '0 0 5px #ff00ff'
                      }}>Vision-Language-Action Systems</h3>
                      <p style={{ color: 'white' }}>Build AI systems that can perceive, reason, and act in physical environments.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Floating AI Chatbot Orb */}
        <div className="chatbot-orb" id="chatbotOrb" style={{ zIndex: 100 }}>
          <div className="orb-glow"></div>
          <div className="orb-content">AI</div>
          <div className="tooltip">Ask anything from this book</div>
        </div>
      </Layout>
    </HtmlClassNameProvider>
  );
}