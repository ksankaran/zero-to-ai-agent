# From: Zero to AI Agent, Chapter 19, Section 19.7
# File: input_validator.py
"""
Input validation for API endpoints using Pydantic.
Validates all user input before processing.
"""

from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, HTTPException, Depends
import re
import logging

logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    """Validated chat request model."""
    
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: str | None = Field(None, max_length=100)
    
    @field_validator('message')
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        """Ensure message has actual content."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty or whitespace only')
        return v.strip()
    
    @field_validator('conversation_id')
    @classmethod
    def valid_conversation_id(cls, v: str | None) -> str | None:
        """Validate conversation ID format."""
        if v is None:
            return v
        # Only allow alphanumeric and hyphens
        if not re.match(r'^[a-zA-Z0-9\-]+$', v):
            raise ValueError('Invalid conversation ID format')
        return v


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    conversation_id: str | None = None


# Example endpoint with validation
app = FastAPI()


async def process_message(message: str) -> str:
    """Process the validated message."""
    # Your LLM call goes here
    return f"Processed: {message}"


async def verify_api_key(api_key: str = None) -> dict:
    """Placeholder for API key verification."""
    # Implement actual verification
    return {"user_id": "demo"}


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, user: dict = Depends(verify_api_key)):
    """
    Chat endpoint with proper validation and error handling.
    
    Validation happens automatically via Pydantic.
    Errors are handled safely without leaking details.
    """
    try:
        result = await process_message(request.message)
        return ChatResponse(
            response=result,
            conversation_id=request.conversation_id
        )
    
    except ValueError as e:
        # Validation error - client's fault
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # Internal error - don't leak details
        logger.error(f"Internal error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred"  # Generic message
        )


# Common validation checks reference:
# | Input         | Validation                                    |
# |---------------|-----------------------------------------------|
# | Message text  | Max length, non-empty, strip whitespace       |
# | IDs           | Format (UUID, alphanumeric), length           |
# | Numbers       | Range, type                                   |
# | URLs          | Format, allowed domains                       |
# | File uploads  | Type, size, content verification              |


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
