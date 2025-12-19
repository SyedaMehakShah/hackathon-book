from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from uuid import UUID

from models.base import User, UserCreate, UserUpdate

# Create router
router = APIRouter()

# In-memory storage for demo purposes (will be replaced with database)
users_db = {}

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    user: User
    token: str

class ProfileResponse(BaseModel):
    user: User

@router.post("/auth/register", response_model=User)
async def register_user(user_data: UserCreate):
    """
    Register a new user
    """
    user_id = str(uuid.uuid4())
    
    # Create user object
    user = {
        "id": user_id,
        "email": user_data.email,
        "name": user_data.name,
        "profile": {},
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    
    # In a real app, we would hash the password
    # For demo, we'll just store the user info
    users_db[user_id] = user
    
    return User(
        id=UUID(user["id"]),
        email=user["email"],
        name=user["name"],
        profile=user["profile"],
        createdAt=datetime.fromisoformat(user["createdAt"]),
        updatedAt=datetime.fromisoformat(user["updatedAt"])
    )

@router.post("/auth/login", response_model=LoginResponse)
async def login_user(login_data: LoginRequest):
    """
    Authenticate user
    """
    # Find user by email
    user = None
    for usr in users_db.values():
        if usr["email"] == login_data.email:
            user = usr
            break
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # In a real app, we would verify the password
    # For demo, we'll just return the user with a mock token
    token = f"mock_token_{user['id']}"
    
    return LoginResponse(
        user=User(
            id=UUID(user["id"]),
            email=user["email"],
            name=user["name"],
            profile=user["profile"],
            createdAt=datetime.fromisoformat(user["createdAt"]),
            updatedAt=datetime.fromisoformat(user["updatedAt"])
        ),
        token=token
    )

@router.get("/auth/profile", response_model=ProfileResponse)
async def get_profile():
    """
    Retrieve user profile
    """
    # In a real app, we would get the user from the auth token
    # For demo, return a mock user
    mock_user = {
        "id": str(uuid.uuid4()),
        "email": "demo@example.com",
        "name": "Demo User",
        "profile": {"preferences": {"language": "en", "theme": "light"}},
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    
    return ProfileResponse(
        user=User(
            id=UUID(mock_user["id"]),
            email=mock_user["email"],
            name=mock_user["name"],
            profile=mock_user["profile"],
            createdAt=datetime.fromisoformat(mock_user["createdAt"]),
            updatedAt=datetime.fromisoformat(mock_user["updatedAt"])
        )
    )