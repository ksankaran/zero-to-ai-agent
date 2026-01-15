# From: Zero to AI Agent, Chapter 19, Section 19.6
# File: response_cache.py
# Description: Simple in-memory cache for LLM responses

import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict


class ResponseCache:
    """Simple in-memory cache for LLM responses."""
    
    def __init__(self, ttl_hours: int = 24):
        self.cache: Dict[str, dict] = {}
        self.ttl = timedelta(hours=ttl_hours)
        self.hits = 0
        self.misses = 0
    
    def _make_key(self, message: str, model: str) -> str:
        """Create a cache key from message and model."""
        # Normalize the message
        normalized = message.lower().strip()
        content = f"{model}:{normalized}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, message: str, model: str) -> Optional[str]:
        """Get cached response if available."""
        key = self._make_key(message, model)
        
        if key in self.cache:
            entry = self.cache[key]
            # Check if still valid
            if datetime.now() - entry["created"] < self.ttl:
                self.hits += 1
                return entry["response"]
            else:
                # Expired, remove it
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, message: str, model: str, response: str):
        """Cache a response."""
        key = self._make_key(message, model)
        self.cache[key] = {
            "response": response,
            "created": datetime.now()
        }
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate_percent": round(hit_rate, 2),
            "cached_responses": len(self.cache),
            "estimated_savings": f"${self.hits * 0.002:.4f}"  # Rough estimate
        }
    
    def clear_expired(self):
        """Remove expired entries."""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now - entry["created"] >= self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
        return len(expired_keys)


# Global cache instance
response_cache = ResponseCache(ttl_hours=24)


# Example usage
if __name__ == "__main__":
    cache = ResponseCache(ttl_hours=1)
    
    # First request - cache miss
    result = cache.get("What is Python?", "gpt-4o-mini")
    print(f"First request (should be None): {result}")
    
    # Store response
    cache.set("What is Python?", "gpt-4o-mini", "Python is a programming language...")
    
    # Second request - cache hit
    result = cache.get("What is Python?", "gpt-4o-mini")
    print(f"Second request (should be cached): {result[:50]}...")
    
    # Different model - cache miss
    result = cache.get("What is Python?", "gpt-4o")
    print(f"Different model (should be None): {result}")
    
    print(f"\nStats: {cache.get_stats()}")
