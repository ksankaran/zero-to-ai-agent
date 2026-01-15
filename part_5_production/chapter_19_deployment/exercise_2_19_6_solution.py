# From: Zero to AI Agent, Chapter 19, Section 19.6
# File: exercise_2_19_6_solution.py (semantic_cache.py)
# Description: Cache that uses embeddings for semantic similarity matching

import hashlib
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


@dataclass
class CacheEntry:
    """A cached response with its embedding."""
    message: str
    response: str
    embedding: List[float]
    created: datetime
    hits: int = 0


class SemanticCache:
    """Cache that matches semantically similar messages."""
    
    def __init__(
        self, 
        ttl_hours: int = 24,
        similarity_threshold: float = 0.92,
        max_entries: int = 1000
    ):
        self.ttl = timedelta(hours=ttl_hours)
        self.similarity_threshold = similarity_threshold
        self.max_entries = max_entries
        self.entries: List[CacheEntry] = []
        
        # Stats
        self.exact_hits = 0
        self.semantic_hits = 0
        self.misses = 0
        
        # OpenAI client for embeddings
        self.client = OpenAI()
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text string."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    
    def _find_similar(self, embedding: List[float]) -> Optional[Tuple[CacheEntry, float]]:
        """Find the most similar cached entry."""
        if not self.entries:
            return None
        
        best_match = None
        best_similarity = 0.0
        
        now = datetime.now()
        valid_entries = [e for e in self.entries if now - e.created < self.ttl]
        
        for entry in valid_entries:
            similarity = self._cosine_similarity(embedding, entry.embedding)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = entry
        
        if best_match and best_similarity >= self.similarity_threshold:
            return best_match, best_similarity
        
        return None
    
    def get(self, message: str) -> Optional[Tuple[str, float, bool]]:
        """
        Get cached response if available.
        
        Returns:
            Tuple of (response, similarity, is_exact_match) or None if not found
        """
        # Normalize message
        normalized = message.lower().strip()
        
        # Check for exact match first (faster)
        for entry in self.entries:
            if entry.message.lower().strip() == normalized:
                if datetime.now() - entry.created < self.ttl:
                    entry.hits += 1
                    self.exact_hits += 1
                    return entry.response, 1.0, True
        
        # Get embedding and find similar
        embedding = self._get_embedding(message)
        result = self._find_similar(embedding)
        
        if result:
            entry, similarity = result
            entry.hits += 1
            self.semantic_hits += 1
            return entry.response, similarity, False
        
        self.misses += 1
        return None
    
    def set(self, message: str, response: str):
        """Cache a response with its embedding."""
        embedding = self._get_embedding(message)
        
        entry = CacheEntry(
            message=message,
            response=response,
            embedding=embedding,
            created=datetime.now()
        )
        
        self.entries.append(entry)
        
        # Trim if over max entries (keep most recently used)
        if len(self.entries) > self.max_entries:
            self.entries = sorted(
                self.entries, 
                key=lambda e: (e.hits, e.created),
                reverse=True
            )[:self.max_entries]
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total_requests = self.exact_hits + self.semantic_hits + self.misses
        
        return {
            "total_entries": len(self.entries),
            "exact_hits": self.exact_hits,
            "semantic_hits": self.semantic_hits,
            "total_hits": self.exact_hits + self.semantic_hits,
            "misses": self.misses,
            "hit_rate_percent": round(
                (self.exact_hits + self.semantic_hits) / total_requests * 100, 2
            ) if total_requests > 0 else 0,
            "semantic_hit_rate_percent": round(
                self.semantic_hits / total_requests * 100, 2
            ) if total_requests > 0 else 0,
            "similarity_threshold": self.similarity_threshold,
            "top_cached": [
                {"message": e.message[:50], "hits": e.hits}
                for e in sorted(self.entries, key=lambda e: e.hits, reverse=True)[:5]
            ]
        }
    
    def clear_expired(self) -> int:
        """Remove expired entries. Returns count of removed entries."""
        now = datetime.now()
        original_count = len(self.entries)
        self.entries = [e for e in self.entries if now - e.created < self.ttl]
        return original_count - len(self.entries)


# Test the semantic cache
if __name__ == "__main__":
    cache = SemanticCache(similarity_threshold=0.90)
    
    # Seed some responses
    print("Seeding cache with sample responses...")
    cache.set("What is the weather like?", "I don't have access to real-time weather data.")
    cache.set("How do I create a Python list?", "Use square brackets: my_list = [1, 2, 3]")
    cache.set("What is machine learning?", "ML is a subset of AI that learns from data.")
    
    # Test similar queries
    test_queries = [
        "What is the weather like?",      # Exact match
        "How's the weather today?",        # Similar
        "What's the weather?",             # Similar
        "Tell me about the weather",       # Similar
        "How do I make a list in Python?", # Similar
        "Creating lists in Python",        # Similar
        "What is ML?",                     # Similar
        "Explain machine learning",        # Similar
        "What is quantum computing?",      # No match
    ]
    
    print("\n" + "=" * 60)
    print("Testing Semantic Cache")
    print("=" * 60)
    
    for query in test_queries:
        result = cache.get(query)
        if result:
            response, similarity, exact = result
            match_type = "EXACT" if exact else f"SEMANTIC ({similarity:.2f})"
            print(f"\n[{match_type}] {query}")
            print(f"  → {response[:60]}...")
        else:
            print(f"\n[MISS] {query}")
    
    print("\n" + "=" * 60)
    print("Cache Stats")
    print("=" * 60)
    import json
    print(json.dumps(cache.get_stats(), indent=2))
