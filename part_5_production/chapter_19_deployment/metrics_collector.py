# From: Zero to AI Agent, Chapter 19, Section 19.4
# File: metrics_collector.py

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import threading


@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    conversation_id: str
    start_time: datetime
    end_time: datetime = None
    tokens_used: int = 0
    model: str = "gpt-3.5-turbo"
    success: bool = True
    error_message: str = None
    
    @property
    def duration_ms(self) -> int:
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds() * 1000)
        return 0


class MetricsCollector:
    """Collect and summarize agent metrics."""
    
    def __init__(self, max_requests: int = 1000):
        self.requests: List[RequestMetrics] = []
        self.max_requests = max_requests
        self._lock = threading.Lock()
    
    def record_request(self, metrics: RequestMetrics):
        """Record a completed request."""
        with self._lock:
            self.requests.append(metrics)
            # Keep only last N requests in memory
            if len(self.requests) > self.max_requests:
                self.requests = self.requests[-self.max_requests:]
    
    def get_summary(self) -> Dict:
        """Get summary statistics."""
        with self._lock:
            if not self.requests:
                return {"message": "No requests recorded yet"}
            
            total = len(self.requests)
            successful = sum(1 for r in self.requests if r.success)
            total_tokens = sum(r.tokens_used for r in self.requests)
            durations = [r.duration_ms for r in self.requests if r.success]
            
            return {
                "total_requests": total,
                "successful_requests": successful,
                "failed_requests": total - successful,
                "success_rate": round(successful / total * 100, 2),
                "total_tokens": total_tokens,
                "avg_duration_ms": round(sum(durations) / len(durations)) if durations else 0,
                "estimated_cost_usd": round(total_tokens * 0.002 / 1000, 4)
            }


# Global metrics collector instance
metrics = MetricsCollector()


# Example usage
if __name__ == "__main__":
    # Simulate some requests
    for i in range(5):
        m = RequestMetrics(
            conversation_id=f"conv-{i}",
            start_time=datetime.now(),
        )
        m.end_time = datetime.now()
        m.tokens_used = 100 + i * 50
        m.success = i != 2  # One failure
        metrics.record_request(m)
    
    print(metrics.get_summary())
