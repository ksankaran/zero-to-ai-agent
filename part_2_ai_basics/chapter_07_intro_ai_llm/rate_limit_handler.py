# From: Zero to AI Agent, Chapter 7, Section 7.6
# File: rate_limit_handler.py

"""
Robust rate limit handling with exponential backoff for AI API calls.
Prevents hitting rate limits and handles them gracefully when they occur.
"""

import time
import random
from typing import Callable, Any, Optional, Dict
from datetime import datetime, timedelta
from collections import deque
import functools


def retry_with_exponential_backoff(
    func: Callable = None,
    initial_delay: float = 1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 5,
    max_delay: float = 60
):
    """
    Decorator to retry a function with exponential backoff.
    Perfect for handling rate limits and transient failures.
    
    Args:
        func: Function to retry (used when called as decorator)
        initial_delay: Starting delay in seconds
        exponential_base: Multiplier for each retry
        jitter: Add randomness to prevent thundering herd
        max_retries: Maximum number of retry attempts
        max_delay: Maximum delay between retries
    
    Usage:
        @retry_with_exponential_backoff(max_retries=3)
        def make_api_call():
            # Your API call here
            pass
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            num_retries = 0
            delay = initial_delay
            
            while num_retries < max_retries:
                try:
                    # Try to execute the function
                    return f(*args, **kwargs)
                
                except Exception as e:
                    error_str = str(e).lower()
                    
                    # Check if it's a rate limit error
                    if any(indicator in error_str for indicator in 
                           ["rate_limit", "rate limit", "429", "too many requests"]):
                        
                        if num_retries < max_retries - 1:
                            # Calculate delay with exponential backoff
                            actual_delay = min(delay, max_delay)
                            
                            # Add jitter if requested
                            if jitter:
                                actual_delay += random.uniform(0, 1)
                            
                            print(f"⏳ Rate limited. Waiting {actual_delay:.1f} seconds...")
                            print(f"   Retry {num_retries + 1}/{max_retries}")
                            
                            time.sleep(actual_delay)
                            
                            # Increase delay for next retry
                            delay *= exponential_base
                            num_retries += 1
                        else:
                            print(f"❌ Max retries ({max_retries}) exceeded")
                            raise
                    else:
                        # Not a rate limit error, re-raise immediately
                        raise e
            
            # Should never reach here, but just in case
            raise Exception(f"Maximum retries ({max_retries}) exceeded")
        
        return wrapper
    
    # Handle both @retry_with_exponential_backoff and @retry_with_exponential_backoff()
    if func is None:
        return decorator
    else:
        return decorator(func)


class RateLimitTracker:
    """
    Track API calls and implement client-side rate limiting
    to prevent hitting server rate limits.
    """
    
    def __init__(self, max_requests_per_minute: int = 50):
        """
        Initialize rate limit tracker
        
        Args:
            max_requests_per_minute: Maximum requests allowed per minute
        """
        self.max_rpm = max_requests_per_minute
        self.request_times = deque()
        self.total_requests = 0
        self.total_throttled = 0
    
    def can_make_request(self) -> bool:
        """Check if we can make a request without exceeding limits"""
        self._clean_old_requests()
        return len(self.request_times) < self.max_rpm
    
    def wait_if_needed(self) -> float:
        """
        Wait if necessary to avoid rate limits.
        Returns the number of seconds waited.
        """
        self._clean_old_requests()
        
        if len(self.request_times) >= self.max_rpm:
            # Calculate how long to wait
            oldest_request = self.request_times[0]
            wait_until = oldest_request + timedelta(minutes=1)
            wait_seconds = (wait_until - datetime.now()).total_seconds()
            
            if wait_seconds > 0:
                print(f"⏳ Approaching rate limit ({self.max_rpm} req/min)")
                print(f"   Waiting {wait_seconds:.1f} seconds...")
                time.sleep(wait_seconds + 0.1)  # Add small buffer
                self.total_throttled += 1
                return wait_seconds
        
        return 0
    
    def record_request(self):
        """Record that a request was made"""
        self.request_times.append(datetime.now())
        self.total_requests += 1
    
    def _clean_old_requests(self):
        """Remove requests older than 1 minute from tracking"""
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        
        while self.request_times and self.request_times[0] < one_minute_ago:
            self.request_times.popleft()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current rate limit statistics"""
        self._clean_old_requests()
        
        return {
            "requests_in_last_minute": len(self.request_times),
            "max_requests_per_minute": self.max_rpm,
            "available_requests": self.max_rpm - len(self.request_times),
            "total_requests": self.total_requests,
            "times_throttled": self.total_throttled,
            "current_usage_percent": (len(self.request_times) / self.max_rpm) * 100
        }
    
    def reset(self):
        """Reset all tracking"""
        self.request_times.clear()
        self.total_requests = 0
        self.total_throttled = 0


class APIRateLimiter:
    """
    Complete rate limiting solution for API calls with
    provider-specific limits and automatic throttling.
    """
    
    # Default rate limits for different providers (requests per minute)
    DEFAULT_LIMITS = {
        "openai": {
            "gpt-3.5-turbo": 60,
            "gpt-4": 20,
            "default": 50
        },
        "anthropic": {
            "default": 50
        },
        "google": {
            "free": 60,
            "paid": 360,
            "default": 60
        }
    }
    
    def __init__(self):
        """Initialize rate limiters for different providers"""
        self.trackers = {}
        self.last_errors = {}
    
    def get_tracker(self, provider: str, model: str = None) -> RateLimitTracker:
        """Get or create a rate limit tracker for a specific provider/model"""
        key = f"{provider}:{model}" if model else provider
        
        if key not in self.trackers:
            # Get appropriate limit
            provider_limits = self.DEFAULT_LIMITS.get(provider, {"default": 50})
            
            if model and model in provider_limits:
                limit = provider_limits[model]
            else:
                limit = provider_limits.get("default", 50)
            
            self.trackers[key] = RateLimitTracker(limit)
        
        return self.trackers[key]
    
    @retry_with_exponential_backoff(max_retries=3)
    def make_api_call(self, provider: str, api_function: Callable, 
                      model: str = None, **kwargs) -> Any:
        """
        Make an API call with rate limiting and retry logic
        
        Args:
            provider: Name of the API provider
            api_function: The actual API function to call
            model: Optional model name for provider-specific limits
            **kwargs: Arguments to pass to the API function
        
        Returns:
            The result of the API call
        """
        tracker = self.get_tracker(provider, model)
        
        # Wait if approaching rate limit
        wait_time = tracker.wait_if_needed()
        
        # Record the request
        tracker.record_request()
        
        try:
            # Make the actual API call
            result = api_function(**kwargs)
            
            # Clear any previous errors for this provider
            if provider in self.last_errors:
                del self.last_errors[provider]
            
            return result
            
        except Exception as e:
            # Record the error
            self.last_errors[provider] = {
                "error": str(e),
                "time": datetime.now(),
                "model": model
            }
            raise
    
    def get_all_stats(self) -> Dict[str, Dict]:
        """Get statistics for all tracked providers"""
        stats = {}
        
        for key, tracker in self.trackers.items():
            stats[key] = tracker.get_stats()
            
            # Add error info if available
            provider = key.split(":")[0]
            if provider in self.last_errors:
                error_info = self.last_errors[provider]
                time_since_error = (datetime.now() - error_info["time"]).total_seconds()
                stats[key]["last_error"] = {
                    "message": error_info["error"][:100],  # Truncate long errors
                    "seconds_ago": round(time_since_error, 1)
                }
        
        return stats
    
    def display_status(self):
        """Display current rate limit status for all providers"""
        print("=" * 60)
        print("RATE LIMIT STATUS")
        print("=" * 60)
        
        stats = self.get_all_stats()
        
        if not stats:
            print("No API calls tracked yet")
            return
        
        for key, stat in stats.items():
            provider_model = key.replace(":", " - ")
            usage_bar = self._create_usage_bar(stat["current_usage_percent"])
            
            print(f"\n{provider_model}:")
            print(f"  Usage: {usage_bar} {stat['current_usage_percent']:.0f}%")
            print(f"  Requests: {stat['requests_in_last_minute']}/{stat['max_requests_per_minute']}")
            print(f"  Available: {stat['available_requests']}")
            
            if "last_error" in stat:
                print(f"  ⚠️ Last error: {stat['last_error']['seconds_ago']}s ago")
    
    def _create_usage_bar(self, percent: float, width: int = 20) -> str:
        """Create a visual progress bar for usage"""
        filled = int((percent / 100) * width)
        bar = "█" * filled + "░" * (width - filled)
        
        # Color coding (would need terminal colors in real implementation)
        if percent < 50:
            return f"[{bar}]"  # Green
        elif percent < 80:
            return f"[{bar}]"  # Yellow
        else:
            return f"[{bar}]"  # Red


# Example usage functions
def demo_rate_limiting():
    """Demonstrate rate limiting in action"""
    
    print("Rate Limiting Demo")
    print("=" * 60)
    
    # Create a rate limiter
    limiter = APIRateLimiter()
    
    # Simulate API calls
    def mock_api_call(message: str):
        """Simulate an API call"""
        # Random chance of rate limit error for demo
        if random.random() < 0.1:
            raise Exception("Rate limit exceeded (429)")
        return f"Response to: {message}"
    
    # Make several calls
    for i in range(5):
        try:
            result = limiter.make_api_call(
                provider="openai",
                api_function=mock_api_call,
                model="gpt-3.5-turbo",
                message=f"Test message {i+1}"
            )
            print(f"✅ Call {i+1}: Success")
        except Exception as e:
            print(f"❌ Call {i+1}: {e}")
        
        time.sleep(0.5)  # Small delay between calls
    
    # Show statistics
    print("\n")
    limiter.display_status()


if __name__ == "__main__":
    # Run the demonstration
    demo_rate_limiting()
    
    print("\n" + "=" * 60)
    print("💡 Rate Limiting Best Practices:")
    print("=" * 60)
    print("1. Always implement client-side rate limiting")
    print("2. Use exponential backoff for retries")
    print("3. Add jitter to prevent thundering herd")
    print("4. Track statistics to optimize usage")
    print("5. Set conservative limits to avoid surprises")
    print("6. Monitor and alert on repeated failures")
