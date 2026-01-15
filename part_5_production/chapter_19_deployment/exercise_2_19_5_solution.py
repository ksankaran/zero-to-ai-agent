# From: Zero to AI Agent, Chapter 19, Section 19.5
# File: exercise_2_19_5_solution.py (queued_api.py)
# Description: Request queuing system for long-running agent tasks

import asyncio
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from contextlib import asynccontextmanager


# Request status enum
class RequestStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# Stored request data
@dataclass
class QueuedRequest:
    id: str
    message: str
    status: RequestStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None
    position: int = 0


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class QueuedResponse(BaseModel):
    request_id: str
    status: str
    position: int
    message: str


class StatusResponse(BaseModel):
    request_id: str
    status: str
    created_at: str
    position: Optional[int] = None
    result: Optional[str] = None
    error: Optional[str] = None
    processing_time_ms: Optional[int] = None


# The queue system
class RequestQueue:
    """Async request queue with background processing."""
    
    def __init__(self, max_concurrent: int = 5):
        self.requests: Dict[str, QueuedRequest] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
        self.max_concurrent = max_concurrent
        self.active_workers = 0
        self._lock = asyncio.Lock()
        self._workers_started = False
    
    async def enqueue(self, message: str, conversation_id: Optional[str] = None) -> QueuedRequest:
        """Add a request to the queue."""
        request_id = str(uuid.uuid4())
        
        async with self._lock:
            position = self.queue.qsize() + 1
            
            queued = QueuedRequest(
                id=request_id,
                message=message,
                status=RequestStatus.QUEUED,
                created_at=datetime.now(),
                position=position
            )
            
            self.requests[request_id] = queued
            await self.queue.put(request_id)
        
        return queued
    
    async def get_status(self, request_id: str) -> Optional[QueuedRequest]:
        """Get the status of a request."""
        async with self._lock:
            if request_id not in self.requests:
                return None
            
            request = self.requests[request_id]
            
            # Update position if still queued
            if request.status == RequestStatus.QUEUED:
                # Count how many are ahead in queue
                position = 0
                for rid, req in self.requests.items():
                    if req.status == RequestStatus.QUEUED and req.created_at < request.created_at:
                        position += 1
                request.position = position + 1
            
            return request
    
    async def process_request(self, request_id: str):
        """Process a single request."""
        async with self._lock:
            if request_id not in self.requests:
                return
            request = self.requests[request_id]
            request.status = RequestStatus.PROCESSING
            request.started_at = datetime.now()
        
        try:
            # ============================================
            # REPLACE THIS with your actual agent call:
            # result = await agent.ainvoke(
            #     {"messages": [HumanMessage(content=request.message)]},
            #     config={"configurable": {"thread_id": conversation_id}}
            # )
            # ============================================
            
            # Simulated LLM call for demonstration
            await asyncio.sleep(2)  # Simulated processing time
            result = f"Response to: {request.message}"
            
            async with self._lock:
                request.status = RequestStatus.COMPLETED
                request.completed_at = datetime.now()
                request.result = result
                
        except Exception as e:
            async with self._lock:
                request.status = RequestStatus.FAILED
                request.completed_at = datetime.now()
                request.error = str(e)
    
    async def worker(self):
        """Background worker that processes queued requests."""
        while True:
            request_id = await self.queue.get()
            
            try:
                await self.process_request(request_id)
            finally:
                self.queue.task_done()
    
    async def start_workers(self):
        """Start background workers."""
        if self._workers_started:
            return
        
        for _ in range(self.max_concurrent):
            asyncio.create_task(self.worker())
        
        self._workers_started = True
    
    async def cleanup_old_requests(self, max_age_hours: int = 24):
        """Remove completed requests older than max_age_hours."""
        async with self._lock:
            cutoff = datetime.now() - timedelta(hours=max_age_hours)
            to_remove = [
                rid for rid, req in self.requests.items()
                if req.status in (RequestStatus.COMPLETED, RequestStatus.FAILED)
                and req.completed_at and req.completed_at < cutoff
            ]
            for rid in to_remove:
                del self.requests[rid]
            
            return len(to_remove)


# Initialize queue
queue = RequestQueue(max_concurrent=5)


# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: start background workers
    await queue.start_workers()
    yield
    # Shutdown: could wait for queue to drain here


app = FastAPI(lifespan=lifespan)


# Endpoints
@app.post("/v1/chat", response_model=QueuedResponse)
async def submit_chat(request: ChatRequest):
    """Submit a chat request to the queue."""
    queued = await queue.enqueue(
        message=request.message,
        conversation_id=request.conversation_id
    )
    
    return QueuedResponse(
        request_id=queued.id,
        status=queued.status.value,
        position=queued.position,
        message="Request queued. Check /v1/status/{request_id} for results."
    )


@app.get("/v1/status/{request_id}", response_model=StatusResponse)
async def get_status(request_id: str):
    """Get the status of a queued request."""
    request = await queue.get_status(request_id)
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Calculate processing time if completed
    processing_time = None
    if request.started_at and request.completed_at:
        processing_time = int((request.completed_at - request.started_at).total_seconds() * 1000)
    
    return StatusResponse(
        request_id=request.id,
        status=request.status.value,
        created_at=request.created_at.isoformat(),
        position=request.position if request.status == RequestStatus.QUEUED else None,
        result=request.result,
        error=request.error,
        processing_time_ms=processing_time
    )


@app.get("/v1/queue/stats")
async def queue_stats():
    """Get queue statistics."""
    async with queue._lock:
        queued = sum(1 for r in queue.requests.values() if r.status == RequestStatus.QUEUED)
        processing = sum(1 for r in queue.requests.values() if r.status == RequestStatus.PROCESSING)
        completed = sum(1 for r in queue.requests.values() if r.status == RequestStatus.COMPLETED)
        failed = sum(1 for r in queue.requests.values() if r.status == RequestStatus.FAILED)
    
    return {
        "queued": queued,
        "processing": processing,
        "completed": completed,
        "failed": failed,
        "total": len(queue.requests)
    }


@app.post("/v1/queue/cleanup")
async def cleanup_queue(max_age_hours: int = 24):
    """Remove old completed requests."""
    removed = await queue.cleanup_old_requests(max_age_hours)
    return {"removed": removed}


# Run with: uvicorn exercise_2_19_5_solution:app --reload
