from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime

from models.base import Chapter, ChapterCreate, ChapterUpdate


class ChapterService:
    """
    Service class for handling chapter-related operations
    """
    
    def __init__(self):
        # In-memory storage for demo purposes (will be replaced with database)
        self.chapters_db = {}
        
        # Initialize with some sample chapters
        initial_chapters = [
            {
                "id": str(uuid.uuid4()),
                "title": "Introduction to Physical AI",
                "content": "# Introduction to Physical AI\n\nPhysical AI is the intersection of artificial intelligence and physical systems. It encompasses robotics, embodied intelligence, and the integration of AI algorithms with real-world physical interactions.\n\n## Learning Objectives\n\n- Understand the core concepts of Physical AI\n- Differentiate between traditional AI and Physical AI\n- Explore real-world applications\n\n## Key Terms\n\n- Embodied Intelligence: Intelligence that emerges through interaction with the physical world\n- Agent-Environment Interaction: The core principle of Physical AI",
                "slug": "introduction-to-physical-ai",
                "order": 1,
                "category": "Foundations",
                "prerequisites": [],
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Embodied Intelligence Fundamentals",
                "content": "# Embodied Intelligence Fundamentals\n\nEmbodied intelligence refers to the idea that intelligence emerges from the interaction between an agent and its environment. This chapter covers the core principles of embodied cognition.\n\n## The Embodiment Hypothesis\n\nThe embodiment hypothesis suggests that intelligence is shaped by the body and its interactions with the environment.\n\n## Key Principles\n\n1. Intelligence is not just computation\n2. The body plays a crucial role in cognition\n3. Environment shapes intelligent behavior\n\n## Applications\n\n- Humanoid robotics\n- Adaptive systems\n- Bio-inspired computing",
                "slug": "embodied-intelligence-fundamentals",
                "order": 2,
                "category": "Foundations",
                "prerequisites": ["introduction-to-physical-ai"],
            },
            {
                "id": str(uuid.uuid4()),
                "title": "ROS 2 for Humanoid Robotics",
                "content": "# ROS 2 for Humanoid Robotics\n\nRobot Operating System (ROS) 2 is a flexible framework for writing robot software. This chapter covers ROS 2 concepts specifically applied to humanoid robotics.\n\n## ROS 2 Architecture\n\nROS 2 uses a DDS (Data Distribution Service) based architecture for communication.\n\n## Key Components\n\n- Nodes: Individual processes that perform computation\n- Topics: Named buses for data transfer\n- Services: Synchronous request/response communication\n- Actions: Extended services with feedback and goals\n\n## Humanoid-Specific Packages\n\n- `ros2_control`: Hardware abstraction and control\n- `moveit2`: Motion planning\n- `navigation2`: Navigation stack\n- `rviz2`: 3D visualization",
                "slug": "ros2-humanoid-robotics",
                "order": 3,
                "category": "Systems",
                "prerequisites": ["embodied-intelligence-fundamentals"],
            }
        ]
        
        # Add initial chapters to the database
        for chapter in initial_chapters:
            self.chapters_db[chapter["slug"]] = chapter

    async def get_all_chapters(self, category: Optional[str] = None, limit: Optional[int] = None, offset: int = 0) -> List[Chapter]:
        """
        Retrieve all chapters, with optional filtering
        """
        chapters = list(self.chapters_db.values())
        
        if category:
            chapters = [ch for ch in chapters if ch["category"].lower() == category.lower()]
        
        if limit:
            chapters = chapters[offset:offset+limit]
        else:
            chapters = chapters[offset:]
        
        # Convert to Chapter models
        chapter_models = []
        for ch in chapters:
            chapter_models.append(Chapter(
                id=UUID(ch["id"]),
                title=ch["title"],
                content=ch["content"],
                slug=ch["slug"],
                order=ch["order"],
                category=ch["category"],
                prerequisites=ch["prerequisites"],
                createdAt=datetime.fromisoformat(ch.get("createdAt", "2025-12-09T10:00:00")) if "createdAt" in ch else datetime.now(),
                updatedAt=datetime.fromisoformat(ch.get("updatedAt", "2025-12-09T10:00:00")) if "updatedAt" in ch else datetime.now()
            ))
        
        return chapter_models

    async def get_chapter_by_slug(self, slug: str) -> Optional[Chapter]:
        """
        Retrieve a chapter by its slug
        """
        if slug not in self.chapters_db:
            return None
        
        chapter = self.chapters_db[slug]
        return Chapter(
            id=UUID(chapter["id"]),
            title=chapter["title"],
            content=chapter["content"],
            slug=chapter["slug"],
            order=chapter["order"],
            category=chapter["category"],
            prerequisites=chapter["prerequisites"],
            createdAt=datetime.fromisoformat(chapter.get("createdAt", "2025-12-09T10:00:00")) if "createdAt" in chapter else datetime.now(),
            updatedAt=datetime.fromisoformat(chapter.get("updatedAt", "2025-12-09T10:00:00")) if "updatedAt" in chapter else datetime.now()
        )

    async def create_chapter(self, chapter_data: ChapterCreate) -> Chapter:
        """
        Create a new chapter
        """
        chapter_id = str(uuid.uuid4())
        
        chapter = {
            "id": chapter_id,
            "title": chapter_data.title,
            "content": chapter_data.content,
            "slug": chapter_data.slug,
            "order": chapter_data.order,
            "category": chapter_data.category,
            "prerequisites": chapter_data.prerequisites,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        
        self.chapters_db[chapter_data.slug] = chapter
        
        return Chapter(
            id=UUID(chapter["id"]),
            title=chapter["title"],
            content=chapter["content"],
            slug=chapter["slug"],
            order=chapter["order"],
            category=chapter["category"],
            prerequisites=chapter["prerequisites"],
            createdAt=datetime.fromisoformat(chapter["createdAt"]),
            updatedAt=datetime.fromisoformat(chapter["updatedAt"])
        )

    async def update_chapter(self, slug: str, chapter_data: ChapterUpdate) -> Optional[Chapter]:
        """
        Update an existing chapter
        """
        if slug not in self.chapters_db:
            return None
        
        chapter = self.chapters_db[slug]
        
        # Update fields if provided
        if chapter_data.title is not None:
            chapter["title"] = chapter_data.title
        if chapter_data.content is not None:
            chapter["content"] = chapter_data.content
        if chapter_data.order is not None:
            chapter["order"] = chapter_data.order
        if chapter_data.category is not None:
            chapter["category"] = chapter_data.category
        if chapter_data.prerequisites is not None:
            chapter["prerequisites"] = chapter_data.prerequisites
        
        chapter["updatedAt"] = datetime.now().isoformat()
        
        return Chapter(
            id=UUID(chapter["id"]),
            title=chapter["title"],
            content=chapter["content"],
            slug=chapter["slug"],
            order=chapter["order"],
            category=chapter["category"],
            prerequisites=chapter["prerequisites"],
            createdAt=datetime.fromisoformat(chapter["createdAt"]),
            updatedAt=datetime.fromisoformat(chapter["updatedAt"])
        )

    async def delete_chapter(self, slug: str) -> bool:
        """
        Delete a chapter
        """
        if slug in self.chapters_db:
            del self.chapters_db[slug]
            return True
        return False