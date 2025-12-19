from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from routes import chapter_routes, rag_routes, auth_routes, translation_routes, summarization_routes

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="API for the Physical AI & Humanoid Robotics textbook with RAG capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Docusaurus frontend
        "http://127.0.0.1:3000",
        "http://localhost:8080",    # HTML frontend if used
        "http://127.0.0.1:8080",
        "*"  # For development purposes only
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chapter_routes.router, prefix="/api", tags=["chapters"])
app.include_router(rag_routes.router, prefix="/api", tags=["rag"])
app.include_router(auth_routes.router, prefix="/api", tags=["auth"])
app.include_router(translation_routes.router, prefix="/api", tags=["translation"])
app.include_router(summarization_routes.router, prefix="/api", tags=["summarization"])

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Physical AI & Humanoid Robotics Textbook API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2025-12-09T10:00:00Z"}

def main():
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

if __name__ == "__main__":
    main()