# Physical AI & Humanoid Robotics – Panaversity

A comprehensive Docusaurus textbook on Physical AI & Humanoid Robotics with integrated RAG chatbot capabilities.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Development](#development)
- [Scripts](#scripts)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [How to Use Claude Code to Continue Writing](#how-to-use-claude-code-to-continue-writing)

## Overview

This project is a comprehensive educational resource on Physical AI & Humanoid Robotics. It combines:

- A complete Docusaurus textbook covering embodied intelligence, ROS 2, Gazebo/Unity simulation, NVIDIA Isaac, Vision-Language-Action systems, and more
- An integrated RAG (Retrieval Augmented Generation) chatbot powered by FastAPI, Qdrant, and OpenAI
- Interactive elements and simulation integration
- Personalized learning paths and multilingual support
- AI subagents and advanced tools for deeper exploration

## Features

- **Comprehensive Textbook**: 13-week curriculum covering all aspects of Physical AI & Humanoid Robotics
- **Integrated Chatbot**: Always-available AI assistant for textbook content with floating widget
- **RAG-Powered Chatbot**: Ask questions about any part of the textbook and get contextual answers
- **Highlight-to-Ask**: Get answers based on selected/highlighted text
- **Contextual Understanding**: Chatbot understands textbook content and provides relevant answers
- **Persistent Chat History**: Conversation history saved in browser storage
- **User Authentication**: Personalized learning experience with progress tracking
- **Multilingual Support**: Urdu translation capability
- **AI Subagents**: Advanced AI tools for deeper exploration using skills-based architecture
- **NotebookLM-Style Summarization**: Generate summaries in multiple formats (text, bullet points, key points)
- **GitHub Pages Deployment**: Fast, reliable hosting
- **Content Validation**: Scripts to validate content integrity
- **Book Ingestion**: Automated process to ingest entire textbook into vector database

## Tech Stack

- **Frontend**: Docusaurus v3 (React-based)
- **Backend**: FastAPI (Python)
- **Database**: Neon Serverless Postgres
- **Vector DB**: Qdrant Cloud
- **AI Integration**: OpenAI API
- **Authentication**: better-auth.com
- **CI/CD**: GitHub Actions
- **AI Framework**: Custom subagent and skills system

## Setup

### Prerequisites

- Node.js 18.x or higher
- Python 3.9 or higher
- npm or yarn package manager
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/physical-ai-textbook.git
   cd physical-ai-textbook
   ```

2. Use the one-command setup script:
   ```bash
   # On Unix/Linux/MacOS:
   ./scripts/setup.sh
   
   # On Windows, run in PowerShell:
   .\scripts\setup.ps1
   ```

3. Or install manually:

   Install frontend dependencies:
   ```bash
   npm install
   ```

   Install Python dependencies:
   ```bash
   cd api
   pip install -r requirements.txt
   # Or using poetry: poetry install
   ```

4. Create environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration
   ```

5. Start the development servers:
   ```bash
   npm start
   ```

## Development

### Project Structure

```
physical-ai-textbook/
├── docs/                 # Textbook content (Markdown files)
├── src/                  # Docusaurus custom components
├── api/                  # FastAPI backend
│   ├── models/           # Data models
│   ├── routes/           # API routes
│   ├── services/         # Business logic
│   └── utils/            # Utility functions
├── rag/                  # RAG implementation
├── agents/               # Subagents & Skills framework
├── skills/               # Skills system for agents
├── auth/                 # Authentication modules
├── scripts/              # Utility scripts
├── .github/workflows/    # CI/CD workflows
├── docusaurus.config.js  # Docusaurus configuration
├── package.json          # NPM dependencies
├── pyproject.toml        # Python dependencies
└── README.md             # Project documentation
```

### Running the Application

To run both frontend and backend simultaneously:

```bash
npm start
```

To run them separately:

Frontend only:
```bash
npm run start:frontend
```

Backend only:
```bash
npm run start:backend
```

## Scripts

This project includes several utility scripts in the `scripts/` directory:

- `setup.sh`: One-command setup script for the entire project
- `ingest-book.js`: Script to ingest the entire textbook into the vector database
- `validate-content.js`: Script to validate all textbook content for correctness
- Additional helper scripts in the `scripts/utils/` directory

## API Endpoints

### Chapter Management
- `GET /api/chapters` - Retrieve list of all chapters
- `GET /api/chapters/{slug}` - Retrieve a specific chapter
- `GET /api/chapters/{slug}/progress` - Retrieve user progress for a chapter
- `PUT /api/chapters/{slug}/progress` - Update user progress

### RAG Chatbot
- `POST /api/embed` - Embed content for storage in vector database
- `POST /api/store` - Store content in the vector database
- `GET /api/search` - Search textbook content
- `POST /api/ask` - Ask a question to the RAG chatbot
- `POST /api/answer-highlighted` - Answer question based on selected text
- `POST /api/rag/query-global` - Global query endpoint for comprehensive textbook search
- `POST /api/v1/rag/query-global` - Legacy global query endpoint (for compatibility)
- `POST /api/chat` - Create a new chat session
- `GET /api/chat/history` - Retrieve chat history
- `POST /api/ingest-book` - Ingest the entire textbook into vector DB

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate user
- `GET /api/auth/profile` - Retrieve user profile

### Translation
- `GET /api/translate/{content_id}` - Get translation of content
- `POST /api/translate/request` - Request translation of content

### Summarization
- `POST /api/summarize` - Generate summary of content

## Deployment

### GitHub Pages

The frontend is configured for GitHub Pages deployment. To build and deploy:

1. Set the correct `baseUrl` in `docusaurus.config.js`
2. Run the deployment script:
   ```bash
   npm run deploy
   ```

The GitHub Actions workflow in `.github/workflows/deploy.yml` will automatically deploy changes to the `gh-pages` branch.

### Backend Deployment

For deploying the FastAPI backend:
1. Ensure all environment variables are configured
2. Deploy the Python application to your preferred hosting platform (Heroku, AWS, Google Cloud, etc.)
3. Configure the API URL in the frontend accordingly

## How to Use Claude Code to Continue Writing

Claude Code can be used to extend this textbook project in many ways:

1. **Add New Chapters**: Create new content in the `docs/` directory following the existing structure.

2. **Extend Backend Functionality**: Add new API endpoints in the `api/routes/` directory, models in `api/models/`, and services in `api/services/`.

3. **Enhance Frontend Components**: Create new React components in the `src/components/` directory.

4. **Create New Skills**: Add new skills to the `api/skills/` directory to extend AI agent capabilities.

5. **Modify Configuration**: Update the Docusaurus configuration in `docusaurus.config.js` to change navigation, themes, or other features.

6. **Add Tests**: Create test files alongside the implementation to ensure quality.

To continue development with Claude Code, you can ask it to:
- Generate new textbook content based on specific robotics topics
- Implement new API endpoints for additional functionality
- Create React components for enhanced user interaction
- Add new AI features or improve existing ones
- Extend the skills system with new capabilities
- Set up additional integrations with robotics simulation tools

Example commands:
```
Help me write a chapter on 'Reinforcement Learning for Robotics'
Add a new skill for '3D model visualization' to the AI agent system
Create a component for 'Interactive robot simulation'
Extend the RAG system to support audio content
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request