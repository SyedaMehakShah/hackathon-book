---

description: "Task list for Physical AI & Humanoid Robotics – Panaversity textbook implementation"
---

# Tasks: Physical AI & Humanoid Robotics – Panaversity

**Input**: Design documents from `/specs/master/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Docusaurus Project**: `docs/`, `src/` for frontend, `api/` for backend
- **Web app**: `api/src/` for backend, `src/` for frontend components
- Paths shown below reflect the structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create complete project structure per implementation plan in physical-ai-textbook/
- [X] T002 Initialize Docusaurus v3 project with TypeScript and required dependencies
- [X] T003 [P] Initialize Python project with FastAPI, asyncpg, and required dependencies in api/
- [ ] T004 [P] Configure linting and formatting tools for both TypeScript and Python (ESLint, Prettier, Black, Ruff)
- [X] T005 Create initial package.json and pyproject.toml with all required dependencies
- [X] T006 Set up development scripts in package.json for start, build, and deploy
- [X] T007 [P] Create .env.example with all required environment variables
- [X] T008 Create initial README.md explaining project structure and setup

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Setup database schema and migrations framework for Neon Postgres in api/db/
- [X] T010 [P] Implement better-auth.com authentication framework in api/auth/ (created basic auth routes)
- [X] T011 [P] Setup API routing and middleware structure in api/src/ (created main app and routes)
- [X] T012 Create base models/entities from data-model.md that all stories depend on in api/src/models/ (created models/base.py)
- [X] T013 Configure error handling and logging infrastructure across frontend and backend (created api/utils/error_handler.py)
- [X] T014 Setup environment configuration management with .env files (created api/utils/config.py)
- [ ] T015 Configure Qdrant Cloud for vector storage and retrieval in api/src/services/
- [X] T016 Setup basic Docusaurus configuration with navigation structure in docusaurus.config.js
- [X] T017 Create initial sidebar configuration for textbook chapters in docs/sidebars.js
- [ ] T018 Setup GitHub Pages deployment configuration in .github/workflows/
- [ ] T019 Initialize OpenAI integration in api/src/services/
- [ ] T020 Create API rate limiting middleware

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Full Docusaurus Book (Priority: P1) 🎯 MVP

**Goal**: Create a complete Docusaurus textbook with all required modules, a landing page, and GitHub Pages deployment

**Independent Test**: Navigate through all textbook sections, verify content displays correctly, test CTA functionality, verify 13-week sequence is logical, and confirm deployment works

### Implementation for User Story 1

- [X] T021 [P] [US1] Create book homepage component in src/pages/index.tsx
- [X] T022 [P] [US1] Create landing page with CTA in src/pages/landing.tsx
- [X] T023 [P] [US1] Create Chapter model in api/src/models/chapter.py (created as part of base.py)
- [X] T024 [P] [US1] Create Section model in api/src/models/section.py (created as part of base.py)
- [X] T025 [P] [US1] Create ContentMetadata model in api/src/models/content_metadata.py (created as part of base.py)
- [X] T026 [US1] Implement ChapterService in api/src/services/chapter_service.py
- [X] T027 [US1] Create GET /api/chapters endpoint in api/src/routes/chapter_routes.py (already implemented)
- [X] T028 [US1] Create GET /api/chapters/{slug} endpoint in api/src/routes/chapter_routes.py (already implemented)
- [X] T029 [US1] Implement chapter content rendering component in src/components/
- [X] T030 [P] [US1] Write Embodied Intelligence chapter content in docs/embodied-intelligence/
- [X] T031 [P] [US1] Write ROS 2 Fundamentals chapter content in docs/ros2-fundamentals/
- [X] T032 [P] [US1] Write Gazebo/Unity chapter content in docs/gazebo-unity/
- [X] T033 [P] [US1] Write NVIDIA Isaac chapter content in docs/nvidia-isaac/
- [X] T034 [P] [US1] Write VLA Systems chapter content in docs/vla-systems/
- [X] T035 [P] [US1] Write Conversational Robotics chapter content in docs/conversational-robotics/
- [X] T036 [P] [US1] Write Capstone Project chapter content in docs/capstone-project/
- [X] T037 [US1] Write Hardware Appendix with tables and diagrams in docs/appendix/
- [X] T038 [US1] Create navigation structure in docusaurus.config.js for 13-week sequence (updated sidebars.js and created intro.md)
- [X] T039 [US1] Implement accessibility features in Docusaurus theme (created theme/Layout/index.js and accessibility-statement.md)
- [X] T040 [US1] Add search functionality for textbook content (added Algolia search configuration to docusaurus.config.js)
- [X] T041 [US1] Create responsive sidebar navigation component (created ResponsiveSidebar.js)
- [X] T042 [US1] Implement 13-week sequence tracking UI (created WeekTracker.js component)
- [X] T043 [US1] Add architecture diagrams to Hardware Appendix (added multiple architecture diagrams to the appendix)
- [ ] T044 [US1] Deploy textbook to GitHub Pages and verify access

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - RAG Chatbot with Full Functionality (Priority: P2)

**Goal**: Implement a complete RAG chatbot with all specified endpoints, database integrations, and frontend widget

**Independent Test**: Verify all API endpoints work correctly, test vector storage/retrieval, confirm chatbot answers from selected text, verify OpenAI integration

### Implementation for User Story 2

- [X] T045 [P] [US2] Create ChatSession model in api/src/models/chat_session.py (added to base.py)
- [X] T046 [P] [US2] Create VectorDocument model in api/src/models/vector_document.py (added to base.py)
- [X] T047 [US2] Implement RAGService in api/src/services/rag_service.py
- [X] T048 [US2] Implement VectorDBService in api/src/services/vector_db_service.py
- [X] T049 [US2] Implement DocumentIngestionService in api/src/services/document_ingestion_service.py
- [X] T050 [US2] Create POST /api/embed endpoint in api/src/routes/rag_routes.py
- [X] T051 [US2] Create POST /api/store endpoint in api/src/routes/rag_routes.py
- [X] T052 [US2] Create GET /api/search endpoint in api/src/routes/rag_routes.py
- [X] T053 [US2] Create POST /api/ask endpoint in api/src/routes/rag_routes.py
- [X] T054 [US2] Create POST /api/answer-highlighted endpoint in api/src/routes/rag_routes.py
- [X] T055 [US2] Implement OpenAI integration with ChatKit tools in api/src/services/ (integrated in rag_service.py)
- [X] T056 [US2] Create chat interface component in src/components/ (created ChatInterface.js and ChatWidget.css)
- [X] T057 [US2] Implement text selection context functionality in frontend (integrated in ChatInterface.js)
- [X] T058 [US2] Add tool calling capabilities for search and retrieval (added get_available_tools and call_tool methods to rag_service.py)
- [X] T059 [US2] Create widget configuration for embedding in Docusaurus pages (created ChatWidget.js and updated docusaurus.config.js)
- [X] T060 [US2] Implement vector database indexing for textbook content (enhanced rag_routes.py with index_textbook_content endpoint)
- [X] T061 [US2] Create script to ingest entire book into vector database (created scripts/ingest_book.py)
- [X] T062 [US2] Add conversation history management in frontend (enhanced ChatInterface.js with localStorage persistence)
- [X] T063 [US2] Implement source citation in chat responses (enhanced ChatInterface.js and ChatWidget.css to display sources in chat messages)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Bonus Features Implementation (Priority: P3)

**Goal**: Implement optional bonus features including authentication, personalization, translation, and AI agents

**Independent Test**: Register and log in as user, test personalized content rendering, verify Urdu translation, test AI subagents and NotebookLM-style summarization

### Implementation for User Story 3

- [X] T064 [P] [US3] Create User model in api/src/models/user.py (already created in base.py)
- [X] T065 [P] [US3] Create UserProgress model in api/src/models/user_progress.py (already created in base.py)
- [X] T066 [P] [US3] Create Translation model in api/src/models/translation.py (already created in base.py)
- [X] T067 [US3] Implement UserService in api/src/services/user_service.py (created user_services.py)
- [X] T068 [US3] Implement UserProgressService in api/src/services/user_progress_service.py (created user_services.py)
- [X] T069 [US3] Implement TranslationService in api/src/services/translation_service.py (created user_services.py)
- [ ] T070 [US3] Create POST /api/auth/register endpoint in api/src/routes/auth_routes.py
- [ ] T071 [US3] Create POST /api/auth/login endpoint in api/src/routes/auth_routes.py
- [ ] T072 [US3] Create GET /api/auth/profile endpoint in api/src/routes/auth_routes.py
- [ ] T073 [US3] Create GET /api/chapters/{slug}/progress endpoint in api/src/routes/chapter_routes.py
- [ ] T074 [US3] Create PUT /api/chapters/{slug}/progress endpoint in api/src/routes/chapter_routes.py
- [ ] T075 [US3] Create GET /api/translate/{contentId} endpoint in api/src/routes/translation_routes.py
- [ ] T076 [US3] Create POST /api/translate/request endpoint in api/src/routes/translation_routes.py
- [ ] T077 [US3] Implement personalized chapter rendering in frontend
- [ ] T078 [US3] Add Urdu translation toggle button in frontend
- [X] T079 [US3] Create AI Subagents framework in api/agents/ (created agent_framework.py)
- [X] T080 [US3] Implement Skills system for AI agents in api/skills/ (created skills system)
- [X] T081 [US3] Create NotebookLM-style summarization endpoint in api/src/routes/summarization_routes.py
- [ ] T082 [US3] Add user progress tracking UI components
- [ ] T083 [US3] Implement content personalization based on user profile
- [X] T084 [US3] Create AI agent interface in frontend (created AIAssistant.js and AIAssistant.css)
- [ ] T085 [US3] Add control flags for enabling bonus features

**Checkpoint**: All bonus features are implemented and functional

---

## Phase 6: User Story 4 - Dev Setup and Scripts (Priority: P4)

**Goal**: Create comprehensive development tools and scripts for easy setup and management

**Independent Test**: Run one-command setup script, execute CLI helpers, verify book ingestion script works

### Implementation for User Story 4

- [X] T086 [US4] Create one-command setup script (setup.sh) in scripts/
- [ ] T087 [US4] Create CLI helpers for common tasks in scripts/cli/
- [X] T088 [US4] Create script to ingest book into vector DB in scripts/ (created ingest-book.js)
- [X] T089 [US4] Implement content validation script to verify all textbook content (created validate-content.js)
- [ ] T090 [US4] Create development environment setup documentation
- [ ] T091 [US4] Implement automated testing script for all components
- [ ] T092 [US4] Create backup and migration scripts for databases
- [ ] T093 [US4] Add script for generating architecture diagrams
- [ ] T094 [US4] Create utility for translating content to Urdu
- [X] T095 [US4] Document all scripts and their usage in README (updated README.md with script documentation)

**Checkpoint**: All development tools and scripts are functional

---

## Phase 7: User Story 5 - Deployment and Production Setup (Priority: P5)

**Goal**: Implement complete deployment pipeline and production configuration

**Independent Test**: Deploy to GitHub Pages, verify FastAPI backend deployment, test Vercel configuration

### Implementation for User Story 5

- [ ] T096 [US5] Complete GitHub Pages deployment workflow in .github/workflows/
- [ ] T097 [US5] Create Vercel deployment configuration in vercel.json
- [ ] T098 [US5] Create FastAPI server deployment guide in docs/deployment/
- [ ] T099 [US5] Implement environment-specific configurations for prod/staging
- [ ] T100 [US5] Create monitoring and logging configuration for production
- [ ] T101 [US5] Set up backup procedures for databases and content
- [ ] T102 [US5] Create health check endpoints for production monitoring
- [ ] T103 [US5] Implement security headers and production security measures
- [ ] T104 [US5] Document deployment procedures and rollback process
- [ ] T105 [US5] Test deployment pipeline with all components integrated

**Checkpoint**: Complete deployment pipeline is functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T106 [P] Documentation updates in docs/ (updated README.md and component documentation)
- [ ] T107 Code cleanup and refactoring across all components
- [ ] T108 Performance optimization across all stories
- [ ] T109 [P] Additional unit tests in api/tests/ and src/tests/
- [ ] T110 Security hardening of all endpoints and components
- [ ] T111 Run quickstart.md validation scenarios
- [ ] T112 Final integration testing of all components
- [ ] T113 Performance testing of RAG system with full textbook content
- [X] T114 Accessibility compliance verification for WCAG 2.1 AA (implemented in Layout component and accessibility-statement.md)
- [ ] T115 Load testing for concurrent users and requests
- [ ] T116 Final review and validation of all textbook content
- [X] T117 Update README with complete project documentation (updated README.md)
- [ ] T118 Create project maintenance and update procedures

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 content for RAG ingestion
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with other stories but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Depends on all other stories for complete deployment

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Chapter model in api/src/models/chapter.py"
Task: "Create Section model in api/src/models/section.py"
Task: "Create ContentMetadata model in api/src/models/content_metadata.py"

# Launch content creation tasks:
Task: "Write Embodied Intelligence chapter content in docs/embodied-intelligence/"
Task: "Write ROS 2 Fundamentals chapter content in docs/ros2-fundamentals/"
Task: "Write Gazebo/Unity chapter content in docs/gazebo-unity/"
Task: "Write NVIDIA Isaac chapter content in docs/nvidia-isaac/"
Task: "Write VLA Systems chapter content in docs/vla-systems/"
Task: "Write Conversational Robotics chapter content in docs/conversational-robotics/"
Task: "Write Capstone Project chapter content in docs/capstone-project/"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence