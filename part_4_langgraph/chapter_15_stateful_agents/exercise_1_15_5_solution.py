# From: Zero to AI Agent, Chapter 15, Section 15.5
# File: exercise_1_15_5_solution.py

"""
Smart retry decorator with configurable policy and metadata.
"""

from dataclasses import dataclass, field
from functools import wraps
from datetime import datetime
import time
import random

@dataclass
class RetryPolicy:
    """Configurable retry behavior."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    retryable_exceptions: tuple = (ConnectionError, TimeoutError)

@dataclass 
class RetryResult:
    """Metadata about retry attempts."""
    success: bool
    value: any = None
    attempts: int = 0
    errors: list = field(default_factory=list)
    total_wait_time: float = 0.0

def smart_retry(policy: RetryPolicy = None):
    """
    Decorator with configurable policy and metadata return.
    
    Returns RetryResult with both the value and retry metadata.
    """
    if policy is None:
        policy = RetryPolicy()
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs) -> RetryResult:
            result = RetryResult(success=False)
            
            for attempt in range(policy.max_attempts):
                result.attempts = attempt + 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                try:
                    value = func(*args, **kwargs)
                    result.success = True
                    result.value = value
                    print(f"  [{timestamp}] Attempt {attempt + 1}: Success ✓")
                    return result
                    
                except policy.retryable_exceptions as e:
                    result.errors.append({"attempt": attempt + 1, "error": str(e)})
                    print(f"  [{timestamp}] Attempt {attempt + 1}: {e}")
                    
                    if attempt < policy.max_attempts - 1:
                        delay = min(policy.base_delay * (2 ** attempt), policy.max_delay)
                        delay += random.uniform(0, delay * 0.1)
                        result.total_wait_time += delay
                        print(f"  [{timestamp}] Waiting {delay:.1f}s before retry...")
                        time.sleep(delay)
                        
                except Exception as e:
                    # Non-retryable exception - fail immediately
                    result.errors.append({"attempt": attempt + 1, "error": str(e), "retryable": False})
                    print(f"  [{timestamp}] Non-retryable error: {e}")
                    return result
            
            return result
        return wrapper
    return decorator

# Demo
def flaky_operation():
    """Fails 70% of the time."""
    if random.random() < 0.7:
        raise ConnectionError("Service unavailable")
    return "Success!"

# Apply smart retry
aggressive_policy = RetryPolicy(max_attempts=5, base_delay=0.5)

@smart_retry(policy=aggressive_policy)
def reliable_operation():
    return flaky_operation()

print("=== Smart Retry Demo ===\n")

for i in range(3):
    print(f"Run {i + 1}:")
    result = reliable_operation()
    print(f"  Result: {'✓' if result.success else '✗'}")
    print(f"  Attempts: {result.attempts}, Wait time: {result.total_wait_time:.1f}s\n")
