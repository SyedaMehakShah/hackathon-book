---
id: 1
title: Create Physical AI Constitution
stage: constitution
date: 2025-12-09
surface: agent
model: unknown
feature: Physical AI & Humanoid Robotics textbook
branch: main
user: Admin
command: /sp.constitution
labels: [constitution, textbook, ai, robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:

---

## Prompt

/sp.constitution You are Spec-Kit Plus, responsible for producing a complete, production-ready AI-native technical textbook using Docusaurus, Spec-Kit Plus scaffolding, and Claude Code automation.

Your responsibility is to follow all requirements with precision:

1. Build a Docusaurus v3 textbook named:
   "Physical AI & Humanoid Robotics – Panaversity"

2. Structure the book according to the provided course outline:
   - Embodied Intelligence
   - ROS 2
   - Gazebo & Unity Simulation
   - NVIDIA Isaac
   - Vision-Language-Action systems
   - Capstone: Autonomous Humanoid Robot
   - Hardware Requirements Appendix

3. Build a full RAG chatbot integrated inside the book.
   Technologies:
   - FastAPI backend
   - Qdrant Cloud (vector DB)
   - Neon Serverless Postgres (metadata)
   - OpenAI Agents/ChatKit SDK
   Capabilities:
   - Answer questions about the book
   - Answer questions based only on selected/highlighted text
   - Tool calling for search, retrieval, summarization

4. Implement full GitHub Pages deployment workflow:
   - docusaurus.config
   - static files
   - GitHub Actions CI

5. Enable Bonus Features (if user enables flags):
   - Reusable intelligence using Claude Code Subagents & Skills
   - User Signup/Signin using better-auth.com
   - Personalized chapter rendering per logged-in user
   - Urdu translation button per chapter (client-side + server-side)
   - Advanced AI Agent modes inside the book

6. Produce readable, clean, consistent structure:
   - /docs
   - /src
   - /rag
   - /api
   - /agents
   - /skills
   - /auth
   - /scripts
   - book.json, package.json, tsconfig.json

7. The generated code and writing must be:
   - Expert-level
   - Technically correct
   - Using modern patterns
   - Properly commented
   - Fully runnable

8. Always follow:
   - the user's specification
   - the course outline
   - Docusaurus standards
   - best practices of FastAPI, Qdrant, Neon, OpenAI SDK

## Response snapshot

## Final Summary

The constitution for the "Physical AI & Humanoid Robotics – Panaversity" textbook project has been successfully created with the following details:

- **New version**: 1.0.0 (initial version)
- **Bump rationale**: This is an initial constitution for a new project focused on creating a Docusaurus textbook on Physical AI & Humanoid Robotics
- **Files flagged for manual follow-up**: None required
- **Suggested commit message**: `docs: add constitution for Physical AI & Humanoid Robotics textbook project`

The constitution establishes six core principles:
1. Expert-Level Content
2. Hands-On Implementation 
3. Multi-Modal Integration
4. RAG-Powered Learning
5. Modern Development Practices
6. Accessibility & Localization

It also outlines technical requirements, development workflow, and governance for the project.

## Outcome

- ✅ Impact: Created project constitution with 6 core principles
- 🧪 Tests: N/A
- 📁 Files: Updated constitution.md
- 🔁 Next prompts: 
- 🧠 Reflection: Successfully created constitution for Physical AI textbook project

## Evaluation notes (flywheel)

- Failure modes observed: 
- Graders run and results (PASS/FAIL): 
- Prompt variant (if applicable): 
- Next experiment (smallest change to try): 