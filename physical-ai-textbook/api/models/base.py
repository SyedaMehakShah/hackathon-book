from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    profile: Optional[dict] = None


class User(UserBase):
    id: UUID
    profile: Optional[dict] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ChapterBase(BaseModel):
    title: str
    slug: str
    order: int
    category: str
    prerequisites: Optional[List[str]] = []


class ChapterCreate(ChapterBase):
    content: str


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None
    category: Optional[str] = None
    prerequisites: Optional[List[str]] = None


class Chapter(ChapterBase):
    id: UUID
    content: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class SectionBase(BaseModel):
    chapterId: str  # UUID as string
    title: str
    order: int


class SectionCreate(SectionBase):
    content: str


class SectionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None


class Section(SectionBase):
    id: UUID
    content: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class UserProgressBase(BaseModel):
    userId: str  # UUID as string
    chapterId: str  # UUID as string
    completed: bool


class UserProgressCreate(UserProgressBase):
    notes: Optional[str] = None


class UserProgressUpdate(BaseModel):
    completed: Optional[bool] = None
    notes: Optional[str] = None


class UserProgress(UserProgressBase):
    id: UUID
    completionDate: Optional[datetime] = None
    notes: Optional[str] = None
    lastAccessed: datetime

    class Config:
        from_attributes = True


class ContentMetadataBase(BaseModel):
    entityId: str  # Generic ID for any content entity
    entityType: str  # Chapter, Section, etc.
    language: str
    originalId: Optional[str] = None  # For translations


class ContentMetadataCreate(ContentMetadataBase):
    pass


class ContentMetadataUpdate(BaseModel):
    language: Optional[str] = None


class ContentMetadata(ContentMetadataBase):
    id: UUID
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ChatSessionBase(BaseModel):
    userId: Optional[str] = None  # Nullable for anonymous users


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    messages: Optional[List[dict]] = None


class ChatSession(ChatSessionBase):
    id: UUID
    startedAt: datetime
    lastMessageAt: datetime
    messages: List[dict]
    context: Optional[str] = None

    class Config:
        from_attributes = True


class VectorDocumentBase(BaseModel):
    contentId: str  # Foreign key to chapter/section
    content: str


class VectorDocumentCreate(VectorDocumentBase):
    metadata: Optional[dict] = None


class VectorDocumentUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[dict] = None


class VectorDocument(VectorDocumentBase):
    id: UUID
    embedding: Optional[list] = None  # Vector as list
    metadata: Optional[dict] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class TranslationBase(BaseModel):
    originalId: str
    originalType: str  # Chapter, Section, etc.
    language: str
    content: str


class TranslationCreate(TranslationBase):
    status: str = "draft"  # draft, reviewed, published


class TranslationUpdate(BaseModel):
    content: Optional[str] = None
    status: Optional[str] = None


class Translation(TranslationBase):
    id: UUID
    status: str  # draft, reviewed, published
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ChatSessionBase(BaseModel):
    userId: Optional[str] = None  # Nullable for anonymous users


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    messages: Optional[List[dict]] = None


class ChatSession(ChatSessionBase):
    id: UUID
    startedAt: datetime
    lastMessageAt: datetime
    messages: List[dict]
    context: Optional[str] = None

    class Config:
        from_attributes = True


class VectorDocumentBase(BaseModel):
    contentId: str  # Foreign key to chapter/section
    content: str


class VectorDocumentCreate(VectorDocumentBase):
    metadata: Optional[dict] = None


class VectorDocumentUpdate(BaseModel):
    content: Optional[str] = None
    metadata: Optional[dict] = None


class VectorDocument(VectorDocumentBase):
    id: UUID
    embedding: Optional[list] = None  # Vector as list
    metadata: Optional[dict] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True