from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from uuid import UUID
import uuid

from models.base import Chapter, ChapterCreate, ChapterUpdate, UserProgress, UserProgressCreate

# Create router
router = APIRouter()

# In-memory storage for demo purposes (will be replaced with database)
chapters_db = {}
user_progress_db = {}

# Mock data for initial chapters
initial_chapters = [
    {
        "id": str(uuid.uuid4()),
        "title": "Introduction to Physical AI",
        "content": "# Introduction to Physical AI\n\nPhysical AI is the intersection of artificial intelligence and physical systems. It encompasses robotics, embodied intelligence, and the integration of AI algorithms with real-world physical interactions.",
        "slug": "introduction-to-physical-ai",
        "order": 1,
        "category": "Foundations",
        "prerequisites": [],
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Embodied Intelligence Fundamentals",
        "content": "# Embodied Intelligence Fundamentals\n\nEmbodied intelligence refers to the idea that intelligence emerges from the interaction between an agent and its environment. This chapter covers the core principles of embodied cognition.",
        "slug": "embodied-intelligence-fundamentals",
        "order": 2,
        "category": "Foundations",
        "prerequisites": ["introduction-to-physical-ai"],
    },
    {
        "id": str(uuid.uuid4()),
        "title": "ROS 2 for Humanoid Robotics",
        "content": "# ROS 2 for Humanoid Robotics\n\nRobot Operating System (ROS) 2 is a flexible framework for writing robot software. This chapter covers ROS 2 concepts specifically applied to humanoid robotics.",
        "slug": "ros2-humanoid-robotics",
        "order": 3,
        "category": "Systems",
        "prerequisites": ["embodied-intelligence-fundamentals"],
    }
]

# Add initial chapters to the database
for chapter in initial_chapters:
    chapters_db[chapter["slug"]] = chapter

@router.get("/chapters", response_model=List[Chapter])
async def get_chapters(
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: Optional[int] = Query(None, ge=1, description="Limit number of results"),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination")
):
    """
    Retrieve list of all chapters
    """
    result = list(chapters_db.values())
    
    if category:
        result = [ch for ch in result if ch["category"].lower() == category.lower()]
    
    if limit:
        result = result[offset:offset+limit]
    else:
        result = result[offset:]
    
    # Convert to Chapter model format
    chapter_models = []
    for ch in result:
        chapter_models.append(Chapter(
            id=UUID(ch["id"]),
            title=ch["title"],
            content=ch["content"],
            slug=ch["slug"],
            order=ch["order"],
            category=ch["category"],
            prerequisites=ch["prerequisites"],
            createdAt="2025-12-09T10:00:00Z",
            updatedAt="2025-12-09T10:00:00Z"
        ))
    
    return chapter_models


@router.get("/chapters/{slug}", response_model=Chapter)
async def get_chapter(slug: str):
    """
    Retrieve a specific chapter by slug
    """
    if slug not in chapters_db:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter = chapters_db[slug]
    return Chapter(
        id=UUID(chapter["id"]),
        title=chapter["title"],
        content=chapter["content"],
        slug=chapter["slug"],
        order=chapter["order"],
        category=chapter["category"],
        prerequisites=chapter["prerequisites"],
        createdAt="2025-12-09T10:00:00Z",
        updatedAt="2025-12-09T10:00:00Z"
    )


@router.get("/chapters/{slug}/progress", response_model=UserProgress)
async def get_chapter_progress(slug: str):
    """
    Retrieve user progress for a specific chapter
    """
    # For now, return a default progress for demonstration
    # In a real app, we would get the current user from auth
    return UserProgress(
        id=UUID(str(uuid.uuid4())),
        userId="demo-user",  # This would be replaced with actual user ID from auth
        chapterId=slug,
        completed=False,
        lastAccessed="2025-12-09T10:00:00Z"
    )


@router.put("/chapters/{slug}/progress", response_model=UserProgress)
async def update_chapter_progress(slug: str, progress: UserProgressCreate):
    """
    Update user progress for a chapter
    """
    # For now, store in memory for demonstration
    progress_id = str(uuid.uuid4())
    user_progress_db[progress_id] = {
        "id": progress_id,
        "userId": "demo-user",  # This would be replaced with actual user ID from auth
        "chapterId": slug,
        "completed": progress.completed,
        "notes": progress.notes,
        "lastAccessed": "2025-12-09T10:00:00Z"
    }
    
    return UserProgress(
        id=UUID(progress_id),
        userId="demo-user",
        chapterId=slug,
        completed=progress.completed,
        notes=progress.notes,
        lastAccessed="2025-12-09T10:00:00Z"
    )