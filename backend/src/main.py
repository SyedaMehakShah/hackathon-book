from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import query_router, upload_router, select_router, rag_router
from src.database.database import get_rag_service

# Create FastAPI app instance
app = FastAPI(
    title="Integrated RAG Chatbot for a Published Book",
    description="A Retrieval-Augmented Generation chatbot that answers questions based strictly on book content",
    version="1.0.0"
)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize required services on startup"""
    rag_service = get_rag_service()
    await rag_service.initialize_qdrant_collection()

# Include API routers
app.include_router(query_router, prefix="/api/v1", tags=["query"])
app.include_router(upload_router, prefix="/api/v1", tags=["upload"])
app.include_router(select_router, prefix="/api/v1", tags=["select"])
app.include_router(rag_router, prefix="/api/v1/rag", tags=["rag"])

@app.get("/")
def read_root():
    return {"message": "Integrated RAG Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}