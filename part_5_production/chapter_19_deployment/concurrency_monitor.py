# From: Zero to AI Agent, Chapter 19, Section 19.5
# File: concurrency_monitor.py
# Description: Track concurrent request metrics for monitoring

import asyncio
from typing import Dict


class ConcurrencyMonitor:
    """Track concurrent request metrics."""
    
    def __init__(self):
        self.active_requests = 0
        self.peak_concurrent = 0
        self.total_requests = 0
        self._lock = asyncio.Lock()
    
    async def request_started(self):
        """Call when a request starts processing."""
        async with self._lock:
            self.active_requests += 1
            self.total_requests += 1
            self.peak_concurrent = max(self.peak_concurrent, self.active_requests)
    
    async def request_finished(self):
        """Call when a request finishes processing."""
        async with self._lock:
            self.active_requests -= 1
    
    async def get_stats(self) -> Dict:
        """Get current concurrency statistics."""
        async with self._lock:
            return {
                "active_requests": self.active_requests,
                "peak_concurrent": self.peak_concurrent,
                "total_requests": self.total_requests
            }
    
    async def reset_peak(self):
        """Reset peak concurrent counter (useful for periodic monitoring)."""
        async with self._lock:
            self.peak_concurrent = self.active_requests


# Global instance
concurrency = ConcurrencyMonitor()


# Example usage with FastAPI
"""
from fastapi import FastAPI, Depends

@app.post("/v1/chat")
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    await concurrency.request_started()
    try:
        # ... process request ...
        result = await agent.ainvoke(...)
        return ChatResponse(...)
    finally:
        await concurrency.request_finished()

@app.get("/metrics")
async def get_metrics(api_key: str = Depends(verify_api_key)):
    return {
        "concurrency": await concurrency.get_stats(),
        "requests": await metrics.get_summary()
    }
"""


if __name__ == "__main__":
    async def simulate_requests():
        """Simulate concurrent requests to demonstrate the monitor."""
        
        async def fake_request(request_id: int, duration: float):
            await concurrency.request_started()
            try:
                print(f"Request {request_id} started. Stats: {await concurrency.get_stats()}")
                await asyncio.sleep(duration)
            finally:
                await concurrency.request_finished()
                print(f"Request {request_id} finished. Stats: {await concurrency.get_stats()}")
        
        # Simulate 5 concurrent requests
        await asyncio.gather(
            fake_request(1, 2.0),
            fake_request(2, 1.5),
            fake_request(3, 1.0),
            fake_request(4, 0.5),
            fake_request(5, 2.5),
        )
        
        print(f"\nFinal stats: {await concurrency.get_stats()}")
    
    asyncio.run(simulate_requests())
