from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Create router
router = APIRouter()

class SummarizeRequest(BaseModel):
    content: str
    max_length: Optional[int] = 100
    format: Optional[str] = "text"  # text, bullet_points, key_points

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_content(request: SummarizeRequest):
    """
    Generate summary of selected content
    """
    # In a real implementation, this would use AI to generate a summary
    # For demo, return a mock summary based on the content
    
    # Simple summarization for demo purposes
    content = request.content
    original_length = len(content)
    
    # Create a simple summary by taking the first few sentences
    sentences = content.split('.')
    summary = '. '.join(sentences[:3]) + '.'  # Take first 3 sentences as summary
    
    # If format is bullet points, transform accordingly
    if request.format == "bullet_points":
        summary = "• " + summary.replace('.', '.\n• ')
    elif request.format == "key_points":
        summary = "Key Points:\n- " + summary.replace('.', '.\n- ')
    
    # Limit length if specified
    if len(summary) > request.max_length:
        summary = summary[:request.max_length] + "..."
    
    summary_length = len(summary)
    compression_ratio = round(summary_length / original_length, 2) if original_length > 0 else 0
    
    return SummarizeResponse(
        summary=summary,
        original_length=original_length,
        summary_length=summary_length,
        compression_ratio=compression_ratio
    )