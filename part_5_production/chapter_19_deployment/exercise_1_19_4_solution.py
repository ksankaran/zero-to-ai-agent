# From: Zero to AI Agent, Chapter 19, Section 19.4
# File: exercise_1_19_4_solution.py
# Exercise 1: Enhanced Logging with Request IDs
#
# This solution demonstrates:
# - JSON-formatted logs
# - Request ID included in all log entries
# - First 100 characters of user message logged
# - Model and token count logged

import logging
import json
import uuid
from datetime import datetime, timezone
from contextvars import ContextVar
from fastapi import FastAPI, Request, Depends, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel


# Context variable to store request ID across async calls
request_id_var: ContextVar[str] = ContextVar('request_id', default='no-request-id')


class EnhancedJSONFormatter(logging.Formatter):
    """JSON formatter that includes request context."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_var.get(),
        }
        
        # Add extra fields from the record
        for key in ['conversation_id', 'processing_time_ms', 'tokens_used', 
                    'model', 'message_preview', 'error_type']:
            if hasattr(record, key):
                log_data[key] = getattr(record, key)
        
        return json.dumps(log_data)


def setup_logging():
    """Set up the enhanced logger."""
    handler = logging.StreamHandler()
    handler.setFormatter(EnhancedJSONFormatter())
    
    logger = logging.getLogger("agent_api")
    logger.handlers = []  # Remove any existing handlers
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger


logger = setup_logging()


def log_with_context(level, message, **extra):
    """Log a message with additional context fields."""
    record = logger.makeRecord(
        logger.name, level, "", 0, message, None, None
    )
    for key, value in extra.items():
        setattr(record, key, value)
    logger.handle(record)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add a unique request ID to each request."""
    
    async def dispatch(self, request: Request, call_next):
        # Generate unique request ID
        req_id = str(uuid.uuid4())[:8]
        request_id_var.set(req_id)
        
        # Add to response headers
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        
        return response


# FastAPI app with enhanced logging
app = FastAPI(title="Agent API with Enhanced Logging")
app.add_middleware(RequestIDMiddleware)


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    processing_time_ms: int


# Simple API key verification
async def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    return api_key


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """Chat endpoint with enhanced logging."""
    start_time = datetime.now()
    conv_id = request.conversation_id or str(uuid.uuid4())
    
    # Preview first 100 chars of message
    message_preview = request.message[:100] + "..." if len(request.message) > 100 else request.message
    
    log_with_context(
        logging.INFO,
        "Chat request started",
        conversation_id=conv_id,
        message_preview=message_preview
    )
    
    try:
        # Simulate agent processing
        import asyncio
        await asyncio.sleep(0.1)
        ai_response = f"This is a simulated response to: {message_preview}"
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Simulated token count
        tokens_used = len(request.message.split()) * 2 + 50
        
        log_with_context(
            logging.INFO,
            "Chat request completed",
            conversation_id=conv_id,
            processing_time_ms=processing_time,
            tokens_used=tokens_used,
            model="gpt-4o-mini"
        )
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conv_id,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        log_with_context(
            logging.ERROR,
            "Chat request failed",
            conversation_id=conv_id,
            processing_time_ms=processing_time,
            error_type=type(e).__name__,
            message_preview=message_preview
        )
        raise HTTPException(status_code=500, detail="An internal error occurred")


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("Agent API with Enhanced Logging")
    print("=" * 60)
    print()
    print("Endpoints:")
    print("  GET  /health   - Health check (no auth required)")
    print("  POST /v1/chat  - Chat endpoint (requires X-API-Key header)")
    print()
    print("Example usage:")
    print('  curl http://localhost:8000/health')
    print()
    print('  curl -X POST http://localhost:8000/v1/chat \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -H "X-API-Key: test-key" \\')
    print('    -d \'{"message": "Hello, how are you?"}\'')
    print()
    print("Watch the console for JSON-formatted logs with request IDs!")
    print("=" * 60)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
