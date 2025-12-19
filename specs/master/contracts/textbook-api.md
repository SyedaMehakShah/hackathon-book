# Textbook API Endpoints

## Chapter Management

### GET /api/chapters
- Description: Retrieve list of all chapters
- Request: None (query params: category, limit, offset)
- Response: Array of Chapter objects
- Auth: Optional (filtered for user if authenticated)

### GET /api/chapters/{slug}
- Description: Retrieve a specific chapter by slug
- Request: Chapter slug as path parameter
- Response: Single Chapter object with all Sections
- Auth: Optional

### GET /api/chapters/{slug}/progress
- Description: Retrieve user progress for a specific chapter
- Request: Chapter slug as path parameter
- Response: UserProgress object
- Auth: Required

### PUT /api/chapters/{slug}/progress
- Description: Update user progress for a chapter
- Request: Chapter slug as path parameter, completion status in body
- Response: Updated UserProgress object
- Auth: Required

## RAG Chatbot API

### POST /api/chat
- Description: Send a message to the RAG chatbot
- Request: Message content, optional context (selected text)
- Response: Chat response with sources
- Auth: Optional (for anonymous sessions)

### POST /api/chat/context
- Description: Set context based on selected/highlighted text
- Request: Selected text content
- Response: Context ID for subsequent chat requests
- Auth: Optional

### GET /api/chat/history
- Description: Retrieve chat history for a session
- Request: Session ID (optional, for authenticated users)
- Response: Array of chat messages
- Auth: Optional

## Content Search & Retrieval

### GET /api/search
- Description: Search textbook content
- Request: Query string, optional filters (category, tags)
- Response: Array of search results with relevance scores
- Auth: Optional

### POST /api/summarize
- Description: Generate summary of selected content
- Request: Content to summarize
- Response: Summary text
- Auth: Optional

## User Management

### POST /api/auth/register
- Description: Register a new user
- Request: Email, password, name
- Response: User object with authentication token
- Auth: None

### POST /api/auth/login
- Description: Authenticate user
- Request: Email, password
- Response: User object with authentication token
- Auth: None

### GET /api/auth/profile
- Description: Retrieve user profile
- Request: Auth token in header
- Response: User object without sensitive data
- Auth: Required

## Translation API

### GET /api/translate/{contentId}
- Description: Get translation of content in specified language
- Request: Content ID, target language
- Response: Translated content
- Auth: Optional

### POST /api/translate/request
- Description: Request translation of content
- Request: Content ID, target language
- Response: Translation request status
- Auth: Optional