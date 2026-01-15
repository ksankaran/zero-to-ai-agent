# From: Zero to AI Agent, Chapter 19, Section 19.4
# File: exercise_2_19_4_solution.py
# Exercise 2: Metrics Dashboard (extends Exercise 1)
#
# This solution builds on exercise_1_19_4_solution.py, adding:
# - Requests per minute (last 5 minutes)
# - 95th percentile response time
# - Top 5 most common errors
# - Token usage breakdown by conversation

import logging
import json
import uuid
import statistics
from datetime import datetime, timedelta, timezone
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Dict, List, Optional
from collections import defaultdict
from fastapi import FastAPI, Request, Depends, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel


# =============================================================================
# PART 1: Enhanced Logging (from Exercise 1)
# =============================================================================

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
    logger.handlers = []
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
        req_id = str(uuid.uuid4())[:8]
        request_id_var.set(req_id)
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        
        return response


# =============================================================================
# PART 2: Simple Metrics Collector
# =============================================================================

@dataclass
class RequestRecord:
    """A single request record."""
    conversation_id: str
    timestamp: datetime
    duration_ms: int
    tokens_used: int
    success: bool
    error_type: Optional[str] = None


class SimpleMetricsCollector:
    """Simple metrics collector."""
    
    def __init__(self, max_size: int = 1000):
        self.records: List[RequestRecord] = []
        self.max_size = max_size
    
    def record(self, rec: RequestRecord):
        """Add a record."""
        self.records.append(rec)
        # Trim if too large
        if len(self.records) > self.max_size:
            self.records = self.records[-self.max_size:]
    
    def get_requests_per_minute(self, minutes: int = 5) -> List[Dict]:
        """Requests per minute for last N minutes."""
        now = datetime.now()
        result = []
        
        for i in range(minutes):
            start = now - timedelta(minutes=i+1)
            end = now - timedelta(minutes=i)
            count = sum(1 for r in self.records if start <= r.timestamp < end)
            result.append({"minute": start.strftime("%H:%M"), "count": count})
        
        return list(reversed(result))
    
    def get_p95_response_time(self) -> Optional[int]:
        """95th percentile response time."""
        durations = [r.duration_ms for r in self.records if r.success]
        if not durations:
            return None
        
        sorted_d = sorted(durations)
        idx = int(len(sorted_d) * 0.95)
        return sorted_d[min(idx, len(sorted_d) - 1)]
    
    def get_top_errors(self, limit: int = 5) -> List[Dict]:
        """Top N most common errors."""
        counts = defaultdict(int)
        for r in self.records:
            if not r.success and r.error_type:
                counts[r.error_type] += 1
        
        sorted_errors = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [{"error": e, "count": c} for e, c in sorted_errors]
    
    def get_tokens_by_conversation(self, limit: int = 10) -> Dict[str, int]:
        """Token usage by conversation."""
        usage = defaultdict(int)
        for r in self.records:
            usage[r.conversation_id] += r.tokens_used
        
        sorted_usage = sorted(usage.items(), key=lambda x: x[1], reverse=True)[:limit]
        return dict(sorted_usage)
    
    def get_dashboard(self) -> Dict:
        """Get full metrics dashboard."""
        if not self.records:
            return {"message": "No requests yet"}
        
        total = len(self.records)
        successful = sum(1 for r in self.records if r.success)
        durations = [r.duration_ms for r in self.records if r.success]
        
        return {
            "summary": {
                "total_requests": total,
                "successful": successful,
                "failed": total - successful,
                "success_rate": round(successful / total * 100, 1)
            },
            "latency": {
                "avg_ms": round(statistics.mean(durations)) if durations else 0,
                "p95_ms": self.get_p95_response_time()
            },
            "requests_per_minute": self.get_requests_per_minute(5),
            "top_errors": self.get_top_errors(5),
            "tokens_by_conversation": self.get_tokens_by_conversation(10)
        }


# Global metrics
metrics = SimpleMetricsCollector()


# =============================================================================
# PART 3: FastAPI Application
# =============================================================================

app = FastAPI(title="Agent API with Metrics Dashboard")
app.add_middleware(RequestIDMiddleware)


class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    processing_time_ms: int


async def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    return api_key


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


@app.get("/metrics")
async def get_metrics(api_key: str = Depends(verify_api_key)):
    """Get metrics dashboard."""
    return metrics.get_dashboard()


@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """Chat endpoint with metrics tracking."""
    import asyncio
    
    start = datetime.now()
    conv_id = request.conversation_id or str(uuid.uuid4())
    
    message_preview = request.message[:100] + "..." if len(request.message) > 100 else request.message
    
    log_with_context(logging.INFO, "Request started", 
                     conversation_id=conv_id, message_preview=message_preview)
    
    try:
        # Simulate processing
        await asyncio.sleep(0.1)
        response_text = f"Response to: {message_preview}"
        
        duration = int((datetime.now() - start).total_seconds() * 1000)
        tokens = len(request.message.split()) * 2 + 50
        
        # Record metrics
        metrics.record(RequestRecord(
            conversation_id=conv_id,
            timestamp=start,
            duration_ms=duration,
            tokens_used=tokens,
            success=True
        ))
        
        log_with_context(logging.INFO, "Request completed",
                         conversation_id=conv_id, processing_time_ms=duration,
                         tokens_used=tokens, model="gpt-4o-mini")
        
        return ChatResponse(
            response=response_text,
            conversation_id=conv_id,
            processing_time_ms=duration
        )
        
    except Exception as e:
        duration = int((datetime.now() - start).total_seconds() * 1000)
        
        metrics.record(RequestRecord(
            conversation_id=conv_id,
            timestamp=start,
            duration_ms=duration,
            tokens_used=0,
            success=False,
            error_type=type(e).__name__
        ))
        
        log_with_context(logging.ERROR, "Request failed",
                         conversation_id=conv_id, error_type=type(e).__name__)
        
        raise HTTPException(status_code=500, detail="Internal error")


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print("Agent API with Metrics Dashboard")
    print("=" * 50)
    print()
    print("Endpoints:")
    print("  GET  /health  - Health check")
    print("  GET  /metrics - Metrics dashboard (needs X-API-Key)")
    print("  POST /v1/chat - Chat (needs X-API-Key)")
    print()
    print("Try:")
    print("  curl http://localhost:8000/health")
    print('  curl http://localhost:8000/metrics -H "X-API-Key: test"')
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
