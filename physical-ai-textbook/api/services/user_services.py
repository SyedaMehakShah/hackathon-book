from datetime import datetime
from typing import Optional, List
from uuid import UUID
import uuid

from models.base import User, UserCreate, UserUpdate, UserProgress, UserProgressCreate, UserProgressUpdate, Translation, TranslationCreate, TranslationUpdate


class UserService:
    """
    Service class for handling user-related operations
    """
    
    def __init__(self):
        # In-memory storage for demo purposes (will be replaced with database)
        self.users_db = {}
        
        # Add a demo user for testing
        demo_user_id = str(uuid.uuid4())
        self.users_db[demo_user_id] = {
            "id": demo_user_id,
            "email": "demo@example.com",
            "name": "Demo User",
            "profile": {"preferences": {"language": "en", "theme": "light"}},
            "createdAt": "2025-12-09T10:00:00Z",
            "updatedAt": "2025-12-09T10:00:00Z"
        }

    async def get_all_users(self) -> List[User]:
        """
        Retrieve all users
        """
        users = []
        for user_data in self.users_db.values():
            users.append(User(
                id=UUID(user_data["id"]),
                email=user_data["email"],
                name=user_data["name"],
                profile=user_data["profile"],
                createdAt=datetime.fromisoformat(user_data["createdAt"]),
                updatedAt=datetime.fromisoformat(user_data["updatedAt"])
            ))
        return users

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by ID
        """
        if user_id not in self.users_db:
            return None
        
        user_data = self.users_db[user_id]
        return User(
            id=UUID(user_data["id"]),
            email=user_data["email"],
            name=user_data["name"],
            profile=user_data["profile"],
            createdAt=datetime.fromisoformat(user_data["createdAt"]),
            updatedAt=datetime.fromisoformat(user_data["updatedAt"])
        )

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email
        """
        for user_data in self.users_db.values():
            if user_data["email"] == email:
                return User(
                    id=UUID(user_data["id"]),
                    email=user_data["email"],
                    name=user_data["name"],
                    profile=user_data["profile"],
                    createdAt=datetime.fromisoformat(user_data["createdAt"]),
                    updatedAt=datetime.fromisoformat(user_data["updatedAt"])
                )
        return None

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user
        """
        user_id = str(uuid.uuid4())
        
        user = {
            "id": user_id,
            "email": user_data.email,
            "name": user_data.name,
            "profile": user_data.profile or {},
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        
        self.users_db[user_id] = user
        
        return User(
            id=UUID(user["id"]),
            email=user["email"],
            name=user["name"],
            profile=user["profile"],
            createdAt=datetime.fromisoformat(user["createdAt"]),
            updatedAt=datetime.fromisoformat(user["updatedAt"])
        )

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """
        Update an existing user
        """
        if user_id not in self.users_db:
            return None
        
        user = self.users_db[user_id]
        
        if user_data.name is not None:
            user["name"] = user_data.name
        if user_data.profile is not None:
            user["profile"] = {**user["profile"], **user_data.profile}
        
        user["updatedAt"] = datetime.now().isoformat()
        
        return User(
            id=UUID(user["id"]),
            email=user["email"],
            name=user["name"],
            profile=user["profile"],
            createdAt=datetime.fromisoformat(user["createdAt"]),
            updatedAt=datetime.fromisoformat(user["updatedAt"])
        )

    async def delete_user(self, user_id: str) -> bool:
        """
        Delete a user
        """
        if user_id in self.users_db:
            del self.users_db[user_id]
            return True
        return False


class UserProgressService:
    """
    Service class for handling user progress-related operations
    """
    
    def __init__(self):
        # In-memory storage for demo purposes (will be replaced with database)
        self.user_progress_db = {}

    async def get_user_progress_by_id(self, progress_id: str) -> Optional[UserProgress]:
        """
        Retrieve user progress by ID
        """
        if progress_id not in self.user_progress_db:
            return None
        
        progress_data = self.user_progress_db[progress_id]
        return UserProgress(
            id=UUID(progress_data["id"]),
            userId=progress_data["userId"],
            chapterId=progress_data["chapterId"],
            completed=progress_data["completed"],
            notes=progress_data.get("notes"),
            lastAccessed=datetime.fromisoformat(progress_data["lastAccessed"])
        )

    async def get_user_progress_by_user_and_chapter(self, user_id: str, chapter_id: str) -> Optional[UserProgress]:
        """
        Retrieve user progress for a specific chapter
        """
        for progress_data in self.user_progress_db.values():
            if progress_data["userId"] == user_id and progress_data["chapterId"] == chapter_id:
                return UserProgress(
                    id=UUID(progress_data["id"]),
                    userId=progress_data["userId"],
                    chapterId=progress_data["chapterId"],
                    completed=progress_data["completed"],
                    notes=progress_data.get("notes"),
                    lastAccessed=datetime.fromisoformat(progress_data["lastAccessed"])
                )
        return None

    async def create_user_progress(self, progress_data: UserProgressCreate) -> UserProgress:
        """
        Create a new user progress record
        """
        progress_id = str(uuid.uuid4())
        
        progress = {
            "id": progress_id,
            "userId": progress_data.userId,
            "chapterId": progress_data.chapterId,
            "completed": progress_data.completed,
            "notes": progress_data.notes,
            "lastAccessed": datetime.now().isoformat()
        }
        
        self.user_progress_db[progress_id] = progress
        
        return UserProgress(
            id=UUID(progress["id"]),
            userId=progress["userId"],
            chapterId=progress["chapterId"],
            completed=progress["completed"],
            notes=progress["notes"],
            lastAccessed=datetime.fromisoformat(progress["lastAccessed"])
        )

    async def update_user_progress(self, progress_id: str, progress_data: UserProgressUpdate) -> Optional[UserProgress]:
        """
        Update an existing user progress record
        """
        if progress_id not in self.user_progress_db:
            return None
        
        progress = self.user_progress_db[progress_id]
        
        if progress_data.completed is not None:
            progress["completed"] = progress_data.completed
        if progress_data.notes is not None:
            progress["notes"] = progress_data.notes
        
        progress["lastAccessed"] = datetime.now().isoformat()
        
        return UserProgress(
            id=UUID(progress["id"]),
            userId=progress["userId"],
            chapterId=progress["chapterId"],
            completed=progress["completed"],
            notes=progress["notes"],
            lastAccessed=datetime.fromisoformat(progress["lastAccessed"])
        )

    async def delete_user_progress(self, progress_id: str) -> bool:
        """
        Delete a user progress record
        """
        if progress_id in self.user_progress_db:
            del self.user_progress_db[progress_id]
            return True
        return False


class TranslationService:
    """
    Service class for handling translation-related operations
    """
    
    def __init__(self):
        # In-memory storage for demo purposes (will be replaced with database)
        self.translations_db = {}

    async def get_translation_by_id(self, translation_id: str) -> Optional[Translation]:
        """
        Retrieve a translation by ID
        """
        if translation_id not in self.translations_db:
            return None
        
        translation_data = self.translations_db[translation_id]
        return Translation(
            id=UUID(translation_data["id"]),
            originalId=translation_data["originalId"],
            originalType=translation_data["originalType"],
            language=translation_data["language"],
            content=translation_data["content"],
            status=translation_data["status"],
            createdAt=datetime.fromisoformat(translation_data["createdAt"]),
            updatedAt=datetime.fromisoformat(translation_data["updatedAt"])
        )

    async def get_translation_by_original_and_language(self, original_id: str, language: str) -> Optional[Translation]:
        """
        Retrieve a translation by original ID and language
        """
        for translation_data in self.translations_db.values():
            if translation_data["originalId"] == original_id and translation_data["language"] == language:
                return Translation(
                    id=UUID(translation_data["id"]),
                    originalId=translation_data["originalId"],
                    originalType=translation_data["originalType"],
                    language=translation_data["language"],
                    content=translation_data["content"],
                    status=translation_data["status"],
                    createdAt=datetime.fromisoformat(translation_data["createdAt"]),
                    updatedAt=datetime.fromisoformat(translation_data["updatedAt"])
                )
        return None

    async def create_translation(self, translation_data: TranslationCreate) -> Translation:
        """
        Create a new translation
        """
        translation_id = str(uuid.uuid4())
        
        translation = {
            "id": translation_id,
            "originalId": translation_data.originalId,
            "originalType": translation_data.originalType,
            "language": translation_data.language,
            "content": translation_data.content,
            "status": translation_data.status,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        
        self.translations_db[translation_id] = translation
        
        return Translation(
            id=UUID(translation["id"]),
            originalId=translation["originalId"],
            originalType=translation["originalType"],
            language=translation["language"],
            content=translation["content"],
            status=translation["status"],
            createdAt=datetime.fromisoformat(translation["createdAt"]),
            updatedAt=datetime.fromisoformat(translation["updatedAt"])
        )

    async def update_translation(self, translation_id: str, translation_data: TranslationUpdate) -> Optional[Translation]:
        """
        Update an existing translation
        """
        if translation_id not in self.translations_db:
            return None
        
        translation = self.translations_db[translation_id]
        
        if translation_data.content is not None:
            translation["content"] = translation_data.content
        if translation_data.status is not None:
            translation["status"] = translation_data.status
        
        translation["updatedAt"] = datetime.now().isoformat()
        
        return Translation(
            id=UUID(translation["id"]),
            originalId=translation["originalId"],
            originalType=translation["originalType"],
            language=translation["language"],
            content=translation["content"],
            status=translation["status"],
            createdAt=datetime.fromisoformat(translation["createdAt"]),
            updatedAt=datetime.fromisoformat(translation["updatedAt"])
        )

    async def delete_translation(self, translation_id: str) -> bool:
        """
        Delete a translation
        """
        if translation_id in self.translations_db:
            del self.translations_db[translation_id]
            return True
        return False