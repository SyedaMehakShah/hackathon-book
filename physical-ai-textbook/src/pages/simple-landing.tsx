import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Link from '@docusaurus/Link';

export default function SimpleLanding() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout>
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#0f0f1a',
        color: 'white',
        padding: '2rem',
        textAlign: 'center'
      }}>
        <div style={{ maxWidth: '800px' }}>
          <h1 style={{
            fontSize: '3rem',
            marginBottom: '1rem',
            color: '#64ffda',
            textShadow: '0 0 10px rgba(100, 255, 218, 0.5)'
          }}>
            {siteConfig.title}
          </h1>

          <p style={{
            fontSize: '1.5rem',
            marginBottom: '2rem',
            color: '#e6e6e6'
          }}>
            {siteConfig.tagline}
          </p>

          <div style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '1rem',
            flexWrap: 'wrap',
            marginTop: '2rem'
          }}>
            <Link
              to="/docs/intro"
              style={{
                backgroundColor: '#64ffda',
                color: '#0f0f1a',
                padding: '0.75rem 1.5rem',
                borderRadius: '4px',
                textDecoration: 'none',
                fontWeight: 'bold',
                fontSize: '1.1rem'
              }}
            >
              Read Textbook
            </Link>

            <Link
              to="/docs/embodied-intelligence/"
              style={{
                backgroundColor: '#4a6cf7',
                color: 'white',
                padding: '0.75rem 1.5rem',
                borderRadius: '4px',
                textDecoration: 'none',
                fontWeight: 'bold',
                fontSize: '1.1rem'
              }}
            >
              Start Learning
            </Link>
          </div>

          <div style={{
            marginTop: '3rem',
            padding: '1.5rem',
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            borderRadius: '8px',
            textAlign: 'left'
          }}>
            <h2 style={{ color: '#64ffda' }}>About This Textbook</h2>
            <p>
              This comprehensive textbook covers 13 weeks of content on Physical AI & Humanoid Robotics,
              including:
            </p>
            <ul style={{ textAlign: 'left', paddingLeft: '1.5rem' }}>
              <li>Embodied Intelligence</li>
              <li>ROS 2 Fundamentals</li>
              <li>Simulation Environments (Gazebo/Unity)</li>
              <li>NVIDIA Isaac Platform</li>
              <li>Vision-Language-Action Systems</li>
              <li>Conversational Robotics</li>
            </ul>
          </div>
        </div>
      </div>
    </Layout>
  );
}