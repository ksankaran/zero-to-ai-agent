# From: Zero to AI Agent, Chapter 19, Section 19.5
# File: concurrency_limiter.py

import asyncio
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

# Maximum concurrent LLM calls
MAX_CONCURRENT_REQUESTS = 50

# Semaphore to limit concurrency
llm_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def verify_api_key():
    """Mock API key verification."""
    return "test-api-key"


@app.post("/v1/chat")
async def chat(message: str, api_key: str = Depends(verify_api_key)):
    """Chat endpoint with concurrency limiting."""
    # Wait for a slot (or fail fast if queue is too long)
    try:
        async with asyncio.timeout(5):  # Wait max 5 seconds for a slot
            async with llm_semaphore:
                # Simulate LLM call
                await asyncio.sleep(2)
                return {"response": f"Echo: {message}"}
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=503,
            detail="Server is busy. Please try again."
        )


# Concurrency monitor
class ConcurrencyMonitor:
    """Track concurrent request metrics."""
    
    def __init__(self):
        self.active_requests = 0
        self.peak_concurrent = 0
        self._lock = asyncio.Lock()
    
    async def request_started(self):
        async with self._lock:
            self.active_requests += 1
            self.peak_concurrent = max(self.peak_concurrent, self.active_requests)
    
    async def request_finished(self):
        async with self._lock:
            self.active_requests -= 1
    
    async def get_stats(self):
        async with self._lock:
            return {
                "active_requests": self.active_requests,
                "peak_concurrent": self.peak_concurrent
            }


concurrency = ConcurrencyMonitor()


@app.post("/v1/chat_monitored")
async def chat_monitored(message: str, api_key: str = Depends(verify_api_key)):
    """Chat endpoint with concurrency monitoring."""
    await concurrency.request_started()
    try:
        async with asyncio.timeout(5):
            async with llm_semaphore:
                await asyncio.sleep(2)
                return {"response": f"Echo: {message}"}
    except asyncio.TimeoutError:
        raise HTTPException(status_code=503, detail="Server is busy")
    finally:
        await concurrency.request_finished()


@app.get("/metrics/concurrency")
async def get_concurrency_metrics(api_key: str = Depends(verify_api_key)):
    """Get concurrency statistics."""
    return await concurrency.get_stats()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
