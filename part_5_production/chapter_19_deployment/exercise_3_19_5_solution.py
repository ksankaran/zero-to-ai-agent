# From: Zero to AI Agent, Chapter 19, Section 19.5
# File: exercise_3_19_5_solution.py (graceful_shutdown.py)
# Description: Graceful shutdown implementation for production deployments

import asyncio
import signal
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent_api")


class GracefulShutdown:
    """Manage graceful shutdown of the application."""
    
    def __init__(self):
        self.shutdown_requested = False
        self.active_requests = 0
        self._lock = asyncio.Lock()
        self._shutdown_event = asyncio.Event()
    
    async def request_started(self):
        """Called when a request starts processing."""
        async with self._lock:
            if self.shutdown_requested:
                raise RuntimeError("Server is shutting down")
            self.active_requests += 1
    
    async def request_finished(self):
        """Called when a request finishes."""
        async with self._lock:
            self.active_requests -= 1
            if self.shutdown_requested and self.active_requests == 0:
                self._shutdown_event.set()
    
    async def initiate_shutdown(self):
        """Begin graceful shutdown."""
        logger.info("Shutdown requested, stopping new requests...")
        async with self._lock:
            self.shutdown_requested = True
            if self.active_requests == 0:
                self._shutdown_event.set()
    
    async def wait_for_completion(self, timeout: float = 30.0):
        """Wait for all requests to complete."""
        try:
            await asyncio.wait_for(
                self._shutdown_event.wait(),
                timeout=timeout
            )
            logger.info("All requests completed gracefully")
        except asyncio.TimeoutError:
            async with self._lock:
                remaining = self.active_requests
            logger.warning(f"Shutdown timeout, {remaining} requests still active")
    
    @property
    async def is_healthy(self) -> bool:
        """Check if server is accepting requests."""
        async with self._lock:
            return not self.shutdown_requested


# Global shutdown manager
shutdown = GracefulShutdown()

# Shared HTTP client
http_client: httpx.AsyncClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global http_client
    
    # ===== STARTUP =====
    logger.info("Starting up...")
    
    # Create shared HTTP client
    http_client = httpx.AsyncClient(timeout=30.0)
    logger.info("HTTP client created")
    
    # Set up signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    
    def handle_signal(sig):
        logger.info(f"Received signal {sig}")
        asyncio.create_task(shutdown.initiate_shutdown())
    
    # Register signal handlers (Unix only)
    try:
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda s=sig: handle_signal(s))
        logger.info("Signal handlers registered")
    except NotImplementedError:
        # Windows doesn't support add_signal_handler
        logger.warning("Signal handlers not available on this platform")
    
    logger.info("Startup complete!")
    
    yield
    
    # ===== SHUTDOWN =====
    logger.info("Shutting down...")
    
    # Initiate graceful shutdown if not already done
    await shutdown.initiate_shutdown()
    
    # Wait for active requests to complete
    logger.info("Waiting for active requests to complete...")
    await shutdown.wait_for_completion(timeout=30.0)
    
    # Close HTTP client
    if http_client:
        await http_client.aclose()
        logger.info("HTTP client closed")
    
    # Flush any remaining logs
    logger.info("Shutdown complete!")


app = FastAPI(lifespan=lifespan)


# Middleware to track requests and reject during shutdown
class ShutdownMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Allow health checks during shutdown
        if request.url.path == "/health":
            return await call_next(request)
        
        try:
            await shutdown.request_started()
        except RuntimeError:
            return JSONResponse(
                status_code=503,
                content={"detail": "Server is shutting down"},
                headers={"Retry-After": "30"}
            )
        
        try:
            response = await call_next(request)
            return response
        finally:
            await shutdown.request_finished()


app.add_middleware(ShutdownMiddleware)


# Endpoints
@app.get("/health")
async def health():
    """Health check - reports shutdown status."""
    is_healthy = await shutdown.is_healthy
    
    if not is_healthy:
        return JSONResponse(
            status_code=503,
            content={
                "status": "shutting_down",
                "message": "Server is gracefully shutting down"
            }
        )
    
    return {"status": "healthy"}


@app.post("/v1/chat")
async def chat():
    """Example endpoint that simulates work."""
    # Simulate LLM call
    await asyncio.sleep(2)
    return {"response": "Hello!"}


@app.get("/admin/shutdown")
async def trigger_shutdown():
    """Trigger graceful shutdown (for testing)."""
    asyncio.create_task(shutdown.initiate_shutdown())
    return {"message": "Shutdown initiated"}


# Run with: uvicorn exercise_3_19_5_solution:app --host 0.0.0.0 --port 8000

# Testing:
# Terminal 1: Start the server
#   uvicorn exercise_3_19_5_solution:app --host 0.0.0.0 --port 8000
#
# Terminal 2: Send a slow request
#   curl -X POST http://localhost:8000/v1/chat &
#
# Terminal 2: Immediately trigger shutdown
#   curl http://localhost:8000/admin/shutdown
#
# Or send SIGTERM:
#   kill -TERM <pid>
#
# Observe:
# - New requests get 503 response
# - In-progress request completes
# - Server shuts down after request finishes
