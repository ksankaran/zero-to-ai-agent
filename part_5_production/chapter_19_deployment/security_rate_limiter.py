# Save as: security_rate_limiter.py
"""
Security-focused rate limiter with abuse detection.
Goes beyond simple rate limiting to detect and ban abusive clients.
"""

from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends
import asyncio


class SecurityRateLimiter:
    """
    Rate limiter with abuse detection.
    
    Features:
    - Per-minute rate limiting
    - Burst detection (too many requests in short window)
    - Automatic banning after repeated violations
    - Auto-unban after cooldown period
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_limit: int = 10,
        ban_threshold: int = 5,
        ban_duration_seconds: int = 3600  # 1 hour
    ):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit  # Max requests in 10 seconds
        self.ban_threshold = ban_threshold  # Violations before ban
        self.ban_duration = ban_duration_seconds
        
        self.requests: dict = defaultdict(list)
        self.violations: dict = defaultdict(int)
        self.banned: set = set()
        self._lock = asyncio.Lock()
    
    async def check(self, identifier: str) -> tuple[bool, str]:
        """
        Check if request is allowed.
        
        Args:
            identifier: API key, user ID, or IP address
            
        Returns:
            (allowed, reason) tuple
        """
        async with self._lock:
            now = datetime.now()
            
            # Check if banned
            if identifier in self.banned:
                return False, "Temporarily banned due to abuse"
            
            # Clean old requests
            minute_ago = now - timedelta(minutes=1)
            ten_seconds_ago = now - timedelta(seconds=10)
            
            self.requests[identifier] = [
                t for t in self.requests[identifier] if t > minute_ago
            ]
            
            # Check burst limit (last 10 seconds)
            recent = sum(1 for t in self.requests[identifier] if t > ten_seconds_ago)
            if recent >= self.burst_limit:
                self.violations[identifier] += 1
                if self.violations[identifier] >= self.ban_threshold:
                    self.banned.add(identifier)
                    # Auto-unban after duration
                    asyncio.create_task(self._unban_later(identifier, self.ban_duration))
                    return False, "Banned for excessive requests"
                return False, "Burst limit exceeded"
            
            # Check minute limit
            if len(self.requests[identifier]) >= self.requests_per_minute:
                return False, "Rate limit exceeded"
            
            # Allow request
            self.requests[identifier].append(now)
            return True, "OK"
    
    async def _unban_later(self, identifier: str, seconds: int):
        """Unban an identifier after a delay."""
        await asyncio.sleep(seconds)
        self.banned.discard(identifier)
        self.violations[identifier] = 0
    
    def get_status(self, identifier: str) -> dict:
        """Get rate limit status for an identifier."""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        recent_requests = len([
            t for t in self.requests[identifier] if t > minute_ago
        ])
        
        return {
            "identifier": identifier[:8] + "...",
            "requests_last_minute": recent_requests,
            "limit": self.requests_per_minute,
            "remaining": self.requests_per_minute - recent_requests,
            "violations": self.violations[identifier],
            "banned": identifier in self.banned,
        }
    
    def get_all_bans(self) -> list:
        """Get list of all currently banned identifiers."""
        return list(self.banned)


# FastAPI integration
app = FastAPI(title="Rate Limited API")
rate_limiter = SecurityRateLimiter()


async def get_api_key(api_key: str = None) -> str:
    """Extract API key from request."""
    # In production, get from header
    return api_key or "anonymous"


@app.post("/v1/chat")
async def chat(message: str, api_key: str = Depends(get_api_key)):
    """Chat endpoint with security rate limiting."""
    
    # Check rate limit by API key
    allowed, reason = await rate_limiter.check(api_key)
    if not allowed:
        raise HTTPException(status_code=429, detail=reason)
    
    # Process request...
    return {"response": f"Processed: {message}"}


@app.get("/v1/rate-limit-status")
async def rate_limit_status(api_key: str = Depends(get_api_key)):
    """Check your rate limit status."""
    return rate_limiter.get_status(api_key)


# Demo and testing
if __name__ == "__main__":
    import asyncio
    
    async def demo():
        print("Security Rate Limiter Demo")
        print("=" * 50)
        
        limiter = SecurityRateLimiter(
            requests_per_minute=10,
            burst_limit=3,
            ban_threshold=2,
            ban_duration_seconds=10  # Short for demo
        )
        
        test_key = "test-api-key-123"
        
        # Normal requests
        print("\n1. Normal requests (should all pass):")
        for i in range(5):
            allowed, reason = await limiter.check(test_key)
            status = "✅" if allowed else "❌"
            print(f"   Request {i+1}: {status} {reason}")
            await asyncio.sleep(0.5)
        
        # Burst requests (should trigger burst limit)
        print("\n2. Burst requests (should hit burst limit):")
        for i in range(5):
            allowed, reason = await limiter.check(test_key)
            status = "✅" if allowed else "❌"
            print(f"   Request {i+1}: {status} {reason}")
            # No delay - burst!
        
        # Show status
        status = limiter.get_status(test_key)
        print(f"\n3. Status: {status}")
        
        # More bursts to trigger ban
        print("\n4. More bursts (should trigger ban):")
        await asyncio.sleep(11)  # Wait for burst window to reset
        for i in range(5):
            allowed, reason = await limiter.check(test_key)
            status = "✅" if allowed else "❌"
            print(f"   Request {i+1}: {status} {reason}")
        
        # Check banned status
        final_status = limiter.get_status(test_key)
        print(f"\n5. Final status: {final_status}")
        print(f"   Banned identifiers: {limiter.get_all_bans()}")
        
        # Wait for unban
        print("\n6. Waiting for auto-unban (10 seconds)...")
        await asyncio.sleep(11)
        
        allowed, reason = await limiter.check(test_key)
        status = "✅" if allowed else "❌"
        print(f"   After cooldown: {status} {reason}")
    
    asyncio.run(demo())
