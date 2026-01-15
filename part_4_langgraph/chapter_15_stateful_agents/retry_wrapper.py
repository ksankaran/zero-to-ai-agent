# From: Zero to AI Agent, Chapter 15, Section 15.5
# File: retry_wrapper.py

"""
A reusable retry wrapper for agent nodes.
"""

import time
import random
from functools import wraps

def with_retry(max_attempts: int = 3, base_delay: float = 1.0):
    """
    Decorator that adds retry logic to any function.
    
    Usage:
        @with_retry(max_attempts=3)
        def my_flaky_function():
            # might fail sometimes
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    last_error = e
                    
                    # Don't retry on final attempt
                    if attempt == max_attempts - 1:
                        break
                    
                    # Calculate wait time
                    wait = base_delay * (2 ** attempt)
                    jitter = random.uniform(0, wait * 0.1)
                    
                    print(f"  ⚠️ Attempt {attempt + 1} failed: {e}")
                    print(f"  ⏳ Retrying in {wait + jitter:.1f}s...")
                    
                    time.sleep(wait + jitter)
            
            # All retries exhausted
            raise last_error
        
        return wrapper
    return decorator


# Demo usage
if __name__ == "__main__":
    import random
    
    @with_retry(max_attempts=3, base_delay=0.5)
    def flaky_api_call(query: str) -> str:
        """Simulates an API that fails 60% of the time."""
        if random.random() < 0.6:
            raise ConnectionError("Service temporarily unavailable")
        return f"Result for: {query}"
    
    print("=== Retry Wrapper Demo ===\n")
    
    for i in range(3):
        try:
            result = flaky_api_call(f"Query {i+1}")
            print(f"Success: {result}\n")
        except Exception as e:
            print(f"Final failure: {e}\n")
