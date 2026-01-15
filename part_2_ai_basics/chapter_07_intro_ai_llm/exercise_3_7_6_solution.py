# Save as: exercise_3_7_6_solution.py
# From: Zero to AI Agent, Chapter 7, Section 7.6

"""
Exercise 3 Solution: Rate Limit Handler
Robust rate limit handler with automatic throttling and helpful feedback.
"""

import time
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum


class RateLimitStatus(Enum):
    """Status of rate limiting"""
    READY = "ready"
    THROTTLED = "throttled"
    WARNING = "warning"
    BLOCKED = "blocked"


@dataclass
class RequestRecord:
    """Record of a single request"""
    timestamp: datetime
    provider: str
    success: bool
    tokens: int = 0


class RobustRateLimitHandler:
    """
    Advanced rate limit handler that:
    - Tracks requests per minute for multiple providers
    - Automatically throttles when approaching limits
    - Provides helpful feedback about wait times
    - Works with any API provider
    """
    
    # Default limits for different providers (requests per minute, tokens per minute)
    DEFAULT_LIMITS = {
        "openai": {"rpm": 60, "tpm": 60000},
        "anthropic": {"rpm": 50, "tpm": 100000},
        "google": {"rpm": 60, "tpm": 1000000},
        "default": {"rpm": 30, "tpm": 50000}
    }
    
    def __init__(self, custom_limits: Dict[str, Dict[str, int]] = None, 
                 window_seconds: int = 60):
        """
        Initialize the rate limit handler
        
        Args:
            custom_limits: Custom rate limits per provider
            window_seconds: Time window for rate limiting (default 60 seconds)
        """
        self.limits = self.DEFAULT_LIMITS.copy()
        if custom_limits:
            self.limits.update(custom_limits)
        
        self.window_seconds = window_seconds
        
        # Track requests per provider
        self.requests: Dict[str, deque] = {}
        self.tokens: Dict[str, deque] = {}
        
        # Statistics
        self.total_requests: Dict[str, int] = {}
        self.total_throttled: Dict[str, int] = {}
        self.total_blocked: Dict[str, int] = {}
        
        # Initialize tracking for each provider
        for provider in self.limits:
            self._init_provider(provider)
    
    def _init_provider(self, provider: str):
        """Initialize tracking structures for a provider"""
        if provider not in self.requests:
            self.requests[provider] = deque()
            self.tokens[provider] = deque()
            self.total_requests[provider] = 0
            self.total_throttled[provider] = 0
            self.total_blocked[provider] = 0
    
    def _clean_old_records(self, provider: str):
        """Remove records older than the time window"""
        cutoff = datetime.now() - timedelta(seconds=self.window_seconds)
        
        # Clean requests
        while self.requests[provider] and self.requests[provider][0].timestamp < cutoff:
            self.requests[provider].popleft()
        
        # Clean tokens
        while self.tokens[provider] and self.tokens[provider][0][0] < cutoff:
            self.tokens[provider].popleft()
    
    def _get_provider_key(self, provider: str) -> str:
        """Get the provider key, falling back to default if not found"""
        if provider in self.limits:
            return provider
        return "default"
    
    def _calculate_usage(self, provider: str) -> Dict[str, Any]:
        """Calculate current usage for a provider"""
        self._clean_old_records(provider)
        
        limits = self.limits[provider]
        current_rpm = len(self.requests[provider])
        current_tpm = sum(t[1] for t in self.tokens[provider])
        
        rpm_percent = (current_rpm / limits["rpm"]) * 100
        tpm_percent = (current_tpm / limits["tpm"]) * 100
        max_usage = max(rpm_percent, tpm_percent)
        
        return {
            "current_rpm": current_rpm,
            "current_tpm": current_tpm,
            "rpm_percent": rpm_percent,
            "tpm_percent": tpm_percent,
            "max_usage": max_usage,
            "limits": limits
        }
    
    def get_status(self, provider: str) -> RateLimitStatus:
        """Get current rate limit status for a provider"""
        provider = self._get_provider_key(provider)
        self._init_provider(provider)
        
        usage = self._calculate_usage(provider)
        max_usage = usage["max_usage"]
        
        if max_usage >= 100:
            return RateLimitStatus.BLOCKED
        elif max_usage >= 80:
            return RateLimitStatus.WARNING
        elif max_usage >= 60:
            return RateLimitStatus.THROTTLED
        else:
            return RateLimitStatus.READY
    
    def check_and_wait(self, provider: str, estimated_tokens: int = 100) -> Dict[str, Any]:
        """
        Check rate limits and calculate wait time if necessary
        
        Args:
            provider: API provider name
            estimated_tokens: Estimated tokens for the request
        
        Returns:
            Dictionary with status and wait time information
        """
        provider = self._get_provider_key(provider)
        self._init_provider(provider)
        self._clean_old_records(provider)
        
        limits = self.limits[provider]
        current_rpm = len(self.requests[provider])
        current_tpm = sum(t[1] for t in self.tokens[provider])
        
        # Check if we would exceed limits
        would_exceed_rpm = current_rpm >= limits["rpm"]
        would_exceed_tpm = (current_tpm + estimated_tokens) > limits["tpm"]
        
        if would_exceed_rpm or would_exceed_tpm:
            # Calculate wait time
            if would_exceed_rpm and self.requests[provider]:
                oldest_request = self.requests[provider][0]
                wait_until = oldest_request.timestamp + timedelta(seconds=self.window_seconds)
                wait_seconds = (wait_until - datetime.now()).total_seconds()
                reason = f"Request limit ({limits['rpm']} req/{self.window_seconds}s)"
            elif self.tokens[provider]:
                oldest_token = self.tokens[provider][0]
                wait_until = oldest_token[0] + timedelta(seconds=self.window_seconds)
                wait_seconds = (wait_until - datetime.now()).total_seconds()
                reason = f"Token limit ({limits['tpm']} tokens/{self.window_seconds}s)"
            else:
                wait_seconds = 0.1
                reason = "Rate limit reached"
            
            wait_seconds = max(0, wait_seconds) + 0.1  # Add small buffer
            
            self.total_throttled[provider] += 1
            
            return {
                "status": RateLimitStatus.BLOCKED,
                "wait_seconds": wait_seconds,
                "reason": reason,
                "current_usage": {"rpm": current_rpm, "tpm": current_tpm},
                "limits": limits,
                "message": f"⏳ Rate limit reached: {reason}. Waiting {wait_seconds:.1f}s..."
            }
        
        # Check usage percentage for warnings
        rpm_percent = (current_rpm / limits["rpm"]) * 100
        tpm_percent = ((current_tpm + estimated_tokens) / limits["tpm"]) * 100
        max_usage = max(rpm_percent, tpm_percent)
        
        if max_usage >= 80:
            status = RateLimitStatus.WARNING
            message = f"⚠️ Approaching rate limit: {max_usage:.0f}% usage"
        elif max_usage >= 60:
            status = RateLimitStatus.THROTTLED
            message = f"🔄 Throttling recommended: {max_usage:.0f}% usage"
        else:
            status = RateLimitStatus.READY
            message = f"✅ Ready: {max_usage:.0f}% usage"
        
        return {
            "status": status,
            "wait_seconds": 0,
            "reason": None,
            "current_usage": {"rpm": current_rpm, "tpm": current_tpm},
            "limits": limits,
            "message": message
        }
    
    def record_request(self, provider: str, tokens_used: int, success: bool = True):
        """Record a completed request"""
        provider = self._get_provider_key(provider)
        self._init_provider(provider)
        
        now = datetime.now()
        
        self.requests[provider].append(RequestRecord(
            timestamp=now,
            provider=provider,
            success=success,
            tokens=tokens_used
        ))
        
        self.tokens[provider].append((now, tokens_used))
        self.total_requests[provider] += 1
    
    def wait_if_needed(self, provider: str, estimated_tokens: int = 100) -> float:
        """
        Wait if necessary to avoid rate limits
        
        Returns:
            Number of seconds waited
        """
        check_result = self.check_and_wait(provider, estimated_tokens)
        
        if check_result["wait_seconds"] > 0:
            print(check_result["message"])
            time.sleep(check_result["wait_seconds"])
            return check_result["wait_seconds"]
        
        if check_result["status"] in [RateLimitStatus.WARNING, RateLimitStatus.THROTTLED]:
            print(check_result["message"])
        
        return 0
    
    def get_statistics(self, provider: str = None) -> Dict[str, Any]:
        """Get detailed statistics for a provider or all providers"""
        if provider:
            providers = [self._get_provider_key(provider)]
        else:
            providers = list(self.limits.keys())
        
        stats = {}
        
        for p in providers:
            self._init_provider(p)
            self._clean_old_records(p)
            
            current_rpm = len(self.requests[p])
            current_tpm = sum(t[1] for t in self.tokens[p])
            limits = self.limits[p]
            
            rpm_percent = (current_rpm / limits["rpm"]) * 100 if limits["rpm"] > 0 else 0
            tpm_percent = (current_tpm / limits["tpm"]) * 100 if limits["tpm"] > 0 else 0
            
            # Calculate status without calling get_status to avoid redundant work
            max_usage = max(rpm_percent, tpm_percent)
            if max_usage >= 100:
                status = "blocked"
            elif max_usage >= 80:
                status = "warning"
            elif max_usage >= 60:
                status = "throttled"
            else:
                status = "ready"
            
            stats[p] = {
                "current_rpm": current_rpm,
                "current_tpm": current_tpm,
                "limit_rpm": limits["rpm"],
                "limit_tpm": limits["tpm"],
                "rpm_usage_percent": rpm_percent,
                "tpm_usage_percent": tpm_percent,
                "total_requests": self.total_requests[p],
                "times_throttled": self.total_throttled[p],
                "times_blocked": self.total_blocked[p],
                "status": status
            }
        
        return stats
    
    def display_dashboard(self):
        """Display a comprehensive rate limit dashboard"""
        stats = self.get_statistics()
        
        print("=" * 60)
        print("📊 RATE LIMIT DASHBOARD")
        print("=" * 60)
        
        for provider, data in stats.items():
            status_icons = {
                "ready": "✅",
                "throttled": "🔄", 
                "warning": "⚠️",
                "blocked": "❌"
            }
            icon = status_icons.get(data["status"], "❓")
            
            print(f"\n{icon} {provider.upper()}")
            print("-" * 40)
            
            rpm_bar = self._create_progress_bar(data["rpm_usage_percent"])
            print(f"Requests: {rpm_bar} {data['current_rpm']}/{data['limit_rpm']} ({data['rpm_usage_percent']:.0f}%)")
            
            tpm_bar = self._create_progress_bar(data["tpm_usage_percent"])
            print(f"Tokens:   {tpm_bar} {data['current_tpm']}/{data['limit_tpm']} ({data['tpm_usage_percent']:.0f}%)")
            
            print(f"\nTotal Requests: {data['total_requests']}")
            if data['times_throttled'] > 0:
                print(f"Times Throttled: {data['times_throttled']}")
    
    def _create_progress_bar(self, percent: float, width: int = 20) -> str:
        """Create a visual progress bar"""
        filled = int((percent / 100) * width)
        filled = min(filled, width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"


def rate_limited(provider: str, handler: RobustRateLimitHandler):
    """Decorator to add rate limiting to any function"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            handler.wait_if_needed(provider, estimated_tokens=100)
            try:
                result = func(*args, **kwargs)
                handler.record_request(provider, tokens_used=100, success=True)
                return result
            except Exception as e:
                handler.record_request(provider, tokens_used=0, success=False)
                raise e
        return wrapper
    return decorator


# Demo and testing
if __name__ == "__main__":
    print("Robust Rate Limit Handler Demo")
    print("=" * 60)
    
    # Create handler with LOW limits AND SHORT window for demo
    # Using 5-second window so we don't wait forever
    handler = RobustRateLimitHandler(
        custom_limits={"test": {"rpm": 5, "tpm": 500}},
        window_seconds=5  # Short window for demo purposes
    )
    
    print("\n🔍 Simulating API calls...")
    print("   (Using 5-second window with 5 requests/window limit)")
    print("-" * 40)
    
    for i in range(12):
        print(f"\nRequest {i+1}:")
        
        # Check and wait if needed
        wait_time = handler.wait_if_needed("test", estimated_tokens=100)
        if wait_time > 0:
            print(f"  ✓ Waited {wait_time:.1f}s, now proceeding...")
        
        # Simulate making the request
        print(f"  Making API call...")
        time.sleep(0.1)  # Simulate API call time
        
        # Record the request
        handler.record_request("test", tokens_used=100, success=True)
        
        # Show status
        stats = handler.get_statistics("test")["test"]
        print(f"  Status: {stats['status']} - RPM: {stats['current_rpm']}/{stats['limit_rpm']}")
    
    # Display final dashboard
    print("\n")
    handler.display_dashboard()
    
    print("\n" + "=" * 60)
    print("✅ Rate limiting demonstration complete!")
    print("\nFeatures demonstrated:")
    print("  • Automatic request tracking")
    print("  • Smart throttling when approaching limits")
    print("  • Helpful wait time feedback")
    print("  • Comprehensive statistics dashboard")
    print("  • Works with any API provider")
    print("\n💡 In production, use window_seconds=60 for real rate limits.")