# Data Model for Physical AI & Humanoid Robotics Textbook

## Entities

### User
- id: string (UUID)
- email: string
- name: string
- profile: JSON object
- createdAt: datetime
- updatedAt: datetime

### Chapter
- id: string (UUID)
- title: string
- content: string (Markdown)
- slug: string
- order: integer
- category: string
- prerequisites: array of Chapter IDs
- createdAt: datetime
- updatedAt: datetime

### Section
- id: string (UUID)
- chapterId: string (foreign key)
- title: string
- content: string (Markdown)
- order: integer
- createdAt: datetime
- updatedAt: datetime

### UserProgress
- id: string (UUID)
- userId: string (foreign key)
- chapterId: string (foreign key)
- completed: boolean
- completionDate: datetime
- notes: string
- lastAccessed: datetime

### ContentMetadata
- id: string (UUID)
- entityId: string (generic ID for any content entity)
- entityType: string (Chapter, Section, etc.)
- language: string
- originalId: string (for translations)
- createdAt: datetime
- updatedAt: datetime

### ChatSession
- id: string (UUID)
- userId: string (nullable, for anonymous users)
- startedAt: datetime
- lastMessageAt: datetime
- messages: array of message objects
- context: string (selected/highlighted text context)

### VectorDocument
- id: string (UUID) 
- contentId: string (foreign key to chapter/section)
- content: string (chunked text)
- embedding: vector (Qdrant format)
- metadata: JSON object
- createdAt: datetime
- updatedAt: datetime

### Translation
- id: string (UUID)
- originalId: string
- originalType: string (Chapter, Section, etc.)
- language: string
- content: string (translated text)
- status: string (draft, reviewed, published)
- createdAt: datetime
- updatedAt: datetime