# From: Zero to AI Agent, Chapter 19, Section 19.5
# File: thread_safe_metrics.py
# Description: Metrics collector safe for concurrent access using asyncio.Lock

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    conversation_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    success: bool = True
    duration_ms: int = 0


class ThreadSafeMetricsCollector:
    """Metrics collector safe for concurrent access."""
    
    def __init__(self, max_requests: int = 1000):
        self.requests: List[RequestMetrics] = []
        self.max_requests = max_requests
        self._lock = asyncio.Lock()
    
    async def record_request(self, metrics: RequestMetrics):
        """Record a request with proper locking."""
        async with self._lock:
            self.requests.append(metrics)
            # Trim old requests to prevent memory growth
            if len(self.requests) > self.max_requests:
                self.requests = self.requests[-self.max_requests:]
    
    async def get_summary(self) -> Dict:
        """Get summary statistics with proper locking."""
        async with self._lock:
            if not self.requests:
                return {"message": "No requests yet"}
            
            total = len(self.requests)
            successful = sum(1 for r in self.requests if r.success)
            
            # Calculate average duration for completed requests
            completed = [r for r in self.requests if r.duration_ms > 0]
            avg_duration = sum(r.duration_ms for r in completed) / len(completed) if completed else 0
            
            return {
                "total_requests": total,
                "successful_requests": successful,
                "success_rate": round(successful / total * 100, 2),
                "average_duration_ms": round(avg_duration, 2)
            }


# Global instance for use across the application
metrics = ThreadSafeMetricsCollector()


# Example usage with FastAPI endpoint
async def example_usage():
    """Demonstrates how to use the metrics collector."""
    from datetime import datetime
    
    # Record a successful request
    start = datetime.now()
    # ... process request ...
    end = datetime.now()
    
    await metrics.record_request(RequestMetrics(
        conversation_id="conv-123",
        start_time=start,
        end_time=end,
        success=True,
        duration_ms=int((end - start).total_seconds() * 1000)
    ))
    
    # Get summary
    summary = await metrics.get_summary()
    print(summary)


if __name__ == "__main__":
    asyncio.run(example_usage())
