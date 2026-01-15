# From: Zero to AI Agent, Chapter 19, Section 19.5
# File: async_rate_limiter.py
# Description: Simple rate limiter for async code with per-key tracking

import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict


class AsyncRateLimiter:
    """Simple rate limiter for async code."""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self._lock = asyncio.Lock()
    
    async def is_allowed(self, key: str) -> bool:
        """Check if a request is allowed for the given key."""
        async with self._lock:
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)
            
            # Clean old requests
            self.requests[key] = [
                t for t in self.requests[key] if t > minute_ago
            ]
            
            # Check limit
            if len(self.requests[key]) >= self.requests_per_minute:
                return False
            
            # Record this request
            self.requests[key].append(now)
            return True
    
    async def get_retry_after(self, key: str) -> int:
        """Get seconds until next request is allowed."""
        async with self._lock:
            if not self.requests[key]:
                return 0
            
            oldest = min(self.requests[key])
            retry_at = oldest + timedelta(minutes=1)
            seconds = (retry_at - datetime.now()).total_seconds()
            return max(0, int(seconds))
    
    async def get_remaining(self, key: str) -> int:
        """Get remaining requests allowed for this key."""
        async with self._lock:
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)
            
            # Count recent requests
            recent = len([t for t in self.requests[key] if t > minute_ago])
            return max(0, self.requests_per_minute - recent)


# Example usage with FastAPI
"""
from fastapi import FastAPI, HTTPException, Depends

rate_limiter = AsyncRateLimiter(requests_per_minute=10)

@app.post("/v1/chat")
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    # Check rate limit
    if not await rate_limiter.is_allowed(api_key):
        retry_after = await rate_limiter.get_retry_after(api_key)
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(retry_after)}
        )
    
    # Process request...
    return {"response": "..."}
"""


if __name__ == "__main__":
    async def test_rate_limiter():
        limiter = AsyncRateLimiter(requests_per_minute=3)
        
        # Test rate limiting
        for i in range(5):
            allowed = await limiter.is_allowed("user-123")
            remaining = await limiter.get_remaining("user-123")
            print(f"Request {i+1}: allowed={allowed}, remaining={remaining}")
            
            if not allowed:
                retry_after = await limiter.get_retry_after("user-123")
                print(f"  Retry after: {retry_after} seconds")
    
    asyncio.run(test_rate_limiter())
