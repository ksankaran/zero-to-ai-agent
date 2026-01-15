# From: Zero to AI Agent, Chapter 12, Section 12.6
# File: exercise_3_12_6_solution.py

import time
from datetime import datetime, timedelta
from collections import deque
import json

class ResilientAPIClient:
    """API client with rate limiting, backoff, circuit breaker, and caching."""
    
    def __init__(self):
        # Rate limiting
        self.calls_per_minute = 10
        self.call_times = deque()
        
        # Circuit breaker
        self.consecutive_failures = 0
        self.max_failures = 5
        self.circuit_open = False
        self.circuit_open_until = None
        
        # Cache
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        
        # Logging
        self.logs = []
    
    def _log(self, message: str, level: str = "INFO"):
        """Add to log."""
        entry = {
            "time": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self.logs.append(entry)
        print(f"[{level}] {message}")
    
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limit."""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        # Remove old calls
        while self.call_times and self.call_times[0] < one_minute_ago:
            self.call_times.popleft()
        
        return len(self.call_times) < self.calls_per_minute
    
    def _check_circuit(self) -> bool:
        """Check if circuit breaker allows request."""
        if not self.circuit_open:
            return True
        
        if datetime.now() >= self.circuit_open_until:
            self.circuit_open = False
            self.consecutive_failures = 0
            self._log("Circuit breaker reset")
            return True
        
        return False
    
    def call_api(self, endpoint: str, params: dict = None) -> str:
        """Make API call with all resilience features."""
        
        # 1. Check circuit breaker
        if not self._check_circuit():
            wait_seconds = (self.circuit_open_until - datetime.now()).seconds
            return f"Error: Circuit breaker open. Try again in {wait_seconds} seconds"
        
        # 2. Check cache
        cache_key = f"{endpoint}:{json.dumps(params or {})}"
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            if datetime.now() - cached_time < timedelta(seconds=self.cache_duration):
                self._log(f"Cache hit for {endpoint}")
                return f"[CACHED] {cached_result}"
        
        # 3. Check rate limit
        if not self._check_rate_limit():
            self._log("Rate limit exceeded", "WARNING")
            return "Error: Rate limit exceeded. Maximum 10 calls per minute"
        
        # 4. Make API call with exponential backoff
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Record call time
                self.call_times.append(datetime.now())
                
                # Simulate API call (30% failure rate)
                import random
                if random.random() < 0.3:
                    raise Exception("API error")
                
                # Success!
                result = f"API Response: {endpoint} with {params}"
                
                # Update cache
                self.cache[cache_key] = (datetime.now(), result)
                
                # Reset failure counter
                self.consecutive_failures = 0
                
                self._log(f"Successful API call to {endpoint}")
                return result
                
            except Exception as e:
                self.consecutive_failures += 1
                
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = 2 ** attempt
                    self._log(f"Attempt {attempt + 1} failed, waiting {wait_time}s", "WARNING")
                    time.sleep(wait_time)
                else:
                    # Final failure
                    self._log(f"All attempts failed for {endpoint}", "ERROR")
                    
                    # Check circuit breaker
                    if self.consecutive_failures >= self.max_failures:
                        self.circuit_open = True
                        self.circuit_open_until = datetime.now() + timedelta(seconds=30)
                        self._log("Circuit breaker opened for 30 seconds", "ERROR")
                    
                    return f"Error: API call failed after {max_retries} attempts"
    
    def get_stats(self) -> str:
        """Get client statistics."""
        return f"""
API Client Statistics
====================
Rate limit: {len(self.call_times)}/{self.calls_per_minute} calls/min
Circuit: {'OPEN' if self.circuit_open else 'CLOSED'}
Consecutive failures: {self.consecutive_failures}
Cache entries: {len(self.cache)}
Log entries: {len(self.logs)}
"""

# Test the resilient client
print("RESILIENT API CLIENT TEST")
print("=" * 50)

client = ResilientAPIClient()

# Test various scenarios
for i in range(15):  # More than rate limit
    result = client.call_api("test/endpoint", {"id": i})
    print(f"Call {i+1}: {result[:50]}...")
    
    # Show stats every 5 calls
    if i % 5 == 4:
        print(client.get_stats())
