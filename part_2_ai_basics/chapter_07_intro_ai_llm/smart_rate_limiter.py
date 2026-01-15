# From: Zero to AI Agent, Chapter 7, Section 7.7
# File: smart_rate_limiter.py

"""
Intelligent rate limiting that maximizes throughput while respecting limits.
Includes user feedback and statistics tracking.
"""

import time
from collections import deque
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional


class RateLimitTypes:
    """Different types of rate limits you'll encounter"""
    
    def __init__(self):
        self.limits = {
            "requests_per_minute": "How many API calls you can make",
            "tokens_per_minute": "How much text you can process", 
            "requests_per_day": "Daily quota (free tiers)",
            "concurrent_requests": "Parallel calls allowed",
            "tokens_per_request": "Max size of single request"
        }
    
    def show_provider_limits(self) -> Dict:
        """Real limits from major providers (as of 2024)"""
        
        limits = {
            "OpenAI GPT-3.5": {
                "tier_1": {"rpm": 3, "tpm": 40000, "max_tokens": 4096},
                "tier_2": {"rpm": 60, "tpm": 60000, "max_tokens": 4096},
                "tier_3": {"rpm": 500, "tpm": 160000, "max_tokens": 4096}
            },
            "OpenAI GPT-4": {
                "tier_1": {"rpm": 3, "tpm": 10000, "max_tokens": 8192},
                "tier_2": {"rpm": 20, "tpm": 40000, "max_tokens": 8192},
                "tier_3": {"rpm": 120, "tpm": 300000, "max_tokens": 8192}
            },
            "Anthropic Claude": {
                "default": {"rpm": 50, "tpm": 100000, "max_tokens": 200000},
                "scale": {"rpm": 1000, "tpm": 2000000, "max_tokens": 200000}
            },
            "Google Gemini": {
                "free": {"rpm": 60, "rpd": 1500, "tpm": 1000000},
                "paid": {"rpm": 360, "rpd": 30000, "tpm": 4000000}
            }
        }
        
        return limits
    
    def print_limits(self):
        """Display provider limits in a readable format"""
        limits = self.show_provider_limits()
        
        print("="*60)
        print("PROVIDER RATE LIMITS")
        print("="*60)
        
        for provider, tiers in limits.items():
            print(f"\n📊 {provider}:")
            for tier, limits in tiers.items():
                print(f"  {tier}:")
                for key, value in limits.items():
                    if key == "rpm":
                        print(f"    Requests/min: {value}")
                    elif key == "tpm":
                        print(f"    Tokens/min: {value:,}")
                    elif key == "rpd":
                        print(f"    Requests/day: {value:,}")
                    elif key == "max_tokens":
                        print(f"    Max tokens: {value:,}")


class SmartRateLimiter:
    """
    Intelligent rate limiting that maximizes throughput
    """
    
    def __init__(self, requests_per_minute: int = 60, tokens_per_minute: int = 40000):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute: RPM limit
            tokens_per_minute: TPM limit
        """
        self.rpm_limit = requests_per_minute
        self.tpm_limit = tokens_per_minute
        
        # Track request times and token counts
        self.request_times = deque()
        self.token_counts = deque()
        
        # Statistics
        self.total_wait_time = 0
        self.total_requests = 0
        self.total_tokens = 0
        self.rate_limit_hits = 0
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text
        
        Args:
            text: Text to estimate
        
        Returns:
            Estimated token count
        """
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4
    
    def can_proceed(self, estimated_tokens: int) -> Tuple[bool, Optional[str]]:
        """
        Check if we can make a request now
        
        Args:
            estimated_tokens: Estimated tokens for the request
        
        Returns:
            Tuple of (can_proceed, reason_if_not)
        """
        current_time = datetime.now()
        minute_ago = current_time - timedelta(minutes=1)
        
        # Clean old entries
        while self.request_times and self.request_times[0] < minute_ago:
            self.request_times.popleft()
            if self.token_counts:
                self.token_counts.popleft()
        
        # Check request limit
        if len(self.request_times) >= self.rpm_limit:
            return False, f"Request limit reached ({self.rpm_limit} RPM)"
        
        # Check token limit
        current_tokens = sum(self.token_counts)
        if current_tokens + estimated_tokens > self.tpm_limit:
            return False, f"Token limit reached ({self.tpm_limit} TPM)"
        
        return True, None
    
    def wait_if_needed(self, estimated_tokens: int) -> float:
        """
        Smart waiting with user feedback
        
        Args:
            estimated_tokens: Estimated tokens for the request
        
        Returns:
            Number of seconds waited
        """
        total_waited = 0
        
        while True:
            can_proceed, reason = self.can_proceed(estimated_tokens)
            
            if can_proceed:
                break
            
            self.rate_limit_hits += 1
            
            # Calculate optimal wait time
            if self.request_times:
                oldest_request = self.request_times[0]
                wait_until = oldest_request + timedelta(minutes=1)
                wait_seconds = (wait_until - datetime.now()).total_seconds()
                
                if wait_seconds > 0:
                    # Provide helpful feedback
                    current_rpm = len(self.request_times)
                    current_tpm = sum(self.token_counts)
                    
                    print(f"\n⏳ Rate limit: {reason}")
                    print(f"   Current usage: {current_rpm}/{self.rpm_limit} RPM, {current_tpm:,}/{self.tpm_limit:,} TPM")
                    print(f"   Waiting {wait_seconds:.1f} seconds...")
                    print(f"   (Request #{self.total_requests + 1})")
                    
                    # Show progress bar for long waits
                    if wait_seconds > 5:
                        self._show_wait_progress(wait_seconds)
                    else:
                        time.sleep(wait_seconds)
                    
                    total_waited += wait_seconds
                    self.total_wait_time += wait_seconds
            else:
                # Should not happen, but safety check
                time.sleep(1)
                total_waited += 1
        
        return total_waited
    
    def _show_wait_progress(self, wait_seconds: float):
        """Show progress bar while waiting"""
        intervals = 20
        interval_time = wait_seconds / intervals
        
        for i in range(intervals):
            progress = (i + 1) / intervals
            bar_length = 30
            filled = int(bar_length * progress)
            bar = "█" * filled + "░" * (bar_length - filled)
            remaining = wait_seconds - (i * interval_time)
            print(f"\r   [{bar}] {remaining:.1f}s remaining", end="")
            time.sleep(interval_time)
        print("\r   ✅ Ready to proceed!                        ")
    
    def record_request(self, actual_tokens: int):
        """
        Record that a request was made
        
        Args:
            actual_tokens: Actual token count used
        """
        self.request_times.append(datetime.now())
        self.token_counts.append(actual_tokens)
        self.total_requests += 1
        self.total_tokens += actual_tokens
    
    def get_stats(self) -> Dict:
        """Get rate limiting statistics"""
        current_rpm = len(self.request_times)
        current_tpm = sum(self.token_counts)
        
        # Calculate efficiency
        if self.total_requests > 0:
            avg_wait = self.total_wait_time / self.total_requests
            efficiency = (self.total_requests / (self.total_requests + self.total_wait_time)) * 100
        else:
            avg_wait = 0
            efficiency = 100
        
        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "total_wait_time": f"{self.total_wait_time:.1f}s",
            "avg_wait_per_request": f"{avg_wait:.2f}s",
            "current_rpm": current_rpm,
            "current_tpm": current_tpm,
            "rpm_usage": f"{(current_rpm/self.rpm_limit)*100:.1f}%",
            "tpm_usage": f"{(current_tpm/self.tpm_limit)*100:.1f}%",
            "rate_limit_hits": self.rate_limit_hits,
            "efficiency": f"{efficiency:.1f}%"
        }
    
    def reset(self):
        """Reset all statistics"""
        self.request_times.clear()
        self.token_counts.clear()
        self.total_wait_time = 0
        self.total_requests = 0
        self.total_tokens = 0
        self.rate_limit_hits = 0


class AdaptiveRateLimiter:
    """
    Advanced rate limiter that adapts to actual API responses
    """
    
    def __init__(self):
        """Initialize adaptive rate limiter"""
        self.limiters = {}  # One limiter per model
        self.performance_history = {}
        self.last_429_time = {}  # Track when we last hit 429 errors
    
    def get_limiter(self, model: str) -> SmartRateLimiter:
        """Get or create limiter for a specific model"""
        if model not in self.limiters:
            # Set conservative defaults, will adapt based on responses
            self.limiters[model] = SmartRateLimiter(
                requests_per_minute=30,  # Start conservative
                tokens_per_minute=30000
            )
        return self.limiters[model]
    
    def handle_response(self, model: str, success: bool, headers: Dict = None):
        """
        Adapt limits based on API response
        
        Args:
            model: Model name
            success: Whether request succeeded
            headers: Response headers (may contain rate limit info)
        """
        if not success:
            # Hit rate limit, back off
            if model in self.limiters:
                limiter = self.limiters[model]
                # Reduce limits by 20%
                limiter.rpm_limit = int(limiter.rpm_limit * 0.8)
                limiter.tpm_limit = int(limiter.tpm_limit * 0.8)
                self.last_429_time[model] = datetime.now()
                print(f"⚠️ Rate limit hit for {model}, reducing to {limiter.rpm_limit} RPM")
        
        elif headers:
            # Some APIs provide rate limit info in headers
            self._parse_rate_limit_headers(model, headers)
    
    def _parse_rate_limit_headers(self, model: str, headers: Dict):
        """Parse rate limit information from response headers"""
        # Example headers (varies by provider):
        # X-RateLimit-Limit-Requests
        # X-RateLimit-Remaining-Requests
        # X-RateLimit-Reset-Requests
        
        if "x-ratelimit-limit-requests" in headers:
            limit = int(headers["x-ratelimit-limit-requests"])
            if model in self.limiters:
                self.limiters[model].rpm_limit = limit
        
        if "x-ratelimit-remaining-requests" in headers:
            remaining = int(headers["x-ratelimit-remaining-requests"])
            # Could use this to optimize request timing
    
    def should_increase_limits(self, model: str) -> bool:
        """Check if we should try increasing limits"""
        if model not in self.last_429_time:
            return True
        
        # Wait at least 5 minutes after a 429 before increasing
        time_since_429 = datetime.now() - self.last_429_time[model]
        return time_since_429 > timedelta(minutes=5)
    
    def optimize_limits(self, model: str):
        """Gradually increase limits if no errors"""
        if self.should_increase_limits(model) and model in self.limiters:
            limiter = self.limiters[model]
            # Increase by 10%
            limiter.rpm_limit = min(int(limiter.rpm_limit * 1.1), 500)  # Cap at 500
            limiter.tpm_limit = min(int(limiter.tpm_limit * 1.1), 200000)  # Cap
            print(f"📈 Optimizing {model} limits to {limiter.rpm_limit} RPM")


def demonstrate_rate_limiting():
    """Demonstrate rate limiting in action"""
    
    print("="*60)
    print("SMART RATE LIMITING DEMONSTRATION")
    print("="*60)
    
    # Create rate limiter with low limits for demo
    limiter = SmartRateLimiter(requests_per_minute=5, tokens_per_minute=1000)
    
    print(f"\nLimits: {limiter.rpm_limit} RPM, {limiter.tpm_limit} TPM")
    print("-" * 40)
    
    # Simulate API calls
    prompts = [
        "Short prompt",
        "This is a medium length prompt with more tokens",
        "This is a much longer prompt that contains significantly more tokens and will use up more of our token budget",
        "Another short one",
        "Medium prompt here",
        "Final prompt"
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"\n📝 Request {i+1}: '{prompt[:30]}...'")
        
        # Estimate tokens
        estimated_tokens = limiter.estimate_tokens(prompt) * 10  # Multiply for demo
        print(f"   Estimated tokens: {estimated_tokens}")
        
        # Wait if needed
        wait_time = limiter.wait_if_needed(estimated_tokens)
        if wait_time == 0:
            print("   ✅ No wait needed")
        
        # Simulate API call
        print("   Making API call...")
        time.sleep(0.5)  # Simulate API latency
        
        # Record request
        actual_tokens = estimated_tokens + 50  # Simulate actual usage
        limiter.record_request(actual_tokens)
        print(f"   ✅ Complete! Used {actual_tokens} tokens")
    
    # Show statistics
    print("\n" + "="*60)
    print("RATE LIMITING STATISTICS")
    print("="*60)
    
    stats = limiter.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")


def demonstrate_adaptive_limiting():
    """Demonstrate adaptive rate limiting"""
    
    print("\n" + "="*60)
    print("ADAPTIVE RATE LIMITING DEMONSTRATION")
    print("="*60)
    
    adapter = AdaptiveRateLimiter()
    
    models = ["gpt-3.5-turbo", "gpt-4", "claude-3-haiku"]
    
    for model in models:
        print(f"\n🤖 Testing {model}")
        limiter = adapter.get_limiter(model)
        print(f"   Initial limits: {limiter.rpm_limit} RPM")
        
        # Simulate successful requests
        for i in range(3):
            adapter.handle_response(model, success=True)
        
        # Try to optimize
        adapter.optimize_limits(model)
        
        # Simulate rate limit hit
        adapter.handle_response(model, success=False)


if __name__ == "__main__":
    # Show provider limits
    rate_types = RateLimitTypes()
    rate_types.print_limits()
    
    # Demonstrate smart rate limiting
    print("\n")
    demonstrate_rate_limiting()
    
    # Demonstrate adaptive rate limiting
    demonstrate_adaptive_limiting()
