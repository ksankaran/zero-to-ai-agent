# From: AI Agents Book - Chapter 13, Section 13.7
# File: memory_cache.py

from datetime import datetime, timedelta


class CachedMemoryStore:
    """Cache frequently accessed conversations for performance."""
    
    def __init__(self, cache_duration_minutes=15):
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self.cache = {}  # session_id -> (timestamp, messages)
        self.hits = 0
        self.misses = 0
    
    def get_messages(self, session_id):
        """Get messages with caching."""
        # Check cache first
        if session_id in self.cache:
            timestamp, messages = self.cache[session_id]
            if datetime.now() - timestamp < self.cache_duration:
                self.hits += 1
                return messages
        
        # Cache miss - load from database
        self.misses += 1
        messages = self._load_from_db(session_id)
        self.cache[session_id] = (datetime.now(), messages)
        return messages
    
    def _load_from_db(self, session_id):
        """Load from actual storage (implement per your backend)."""
        # Placeholder - implement actual database loading
        return []
    
    def invalidate_cache(self, session_id):
        """Clear cache for a session."""
        if session_id in self.cache:
            del self.cache[session_id]
    
    def clear_expired(self):
        """Remove expired cache entries."""
        now = datetime.now()
        expired = [
            sid for sid, (timestamp, _) in self.cache.items()
            if now - timestamp >= self.cache_duration
        ]
        for sid in expired:
            del self.cache[sid]
        return len(expired)
    
    def get_stats(self):
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.2%}",
            "cached_sessions": len(self.cache)
        }


# Usage
if __name__ == "__main__":
    cache = CachedMemoryStore(cache_duration_minutes=15)
    
    # Simulate access pattern
    for _ in range(5):
        cache.get_messages("user_123")  # First is miss, rest are hits
    
    cache.get_messages("user_456")  # New user, cache miss
    
    print("Cache stats:", cache.get_stats())
