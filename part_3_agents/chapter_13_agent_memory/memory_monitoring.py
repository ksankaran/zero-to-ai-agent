# From: AI Agents Book - Chapter 13, Section 13.7
# File: memory_monitoring.py

from datetime import datetime


class MemoryMonitor:
    """Track memory system health and performance metrics."""
    
    def __init__(self):
        self.metrics = {
            "total_conversations": 0,
            "total_messages": 0,
            "avg_conversation_length": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "storage_operations": 0,
            "errors": 0,
        }
        self.start_time = datetime.now()
    
    def log_conversation(self, message_count):
        """Log a conversation."""
        self.metrics["total_conversations"] += 1
        self.metrics["total_messages"] += message_count
        self._update_average()
    
    def _update_average(self):
        """Update average conversation length."""
        if self.metrics["total_conversations"] > 0:
            self.metrics["avg_conversation_length"] = (
                self.metrics["total_messages"] / self.metrics["total_conversations"]
            )
    
    def log_access(self, session_id, is_cache_hit):
        """Log memory access pattern."""
        if is_cache_hit:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1
    
    def log_storage_operation(self):
        """Log a storage operation."""
        self.metrics["storage_operations"] += 1
    
    def log_error(self):
        """Log an error."""
        self.metrics["errors"] += 1
    
    def get_cache_hit_rate(self):
        """Calculate cache effectiveness."""
        total = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        if total == 0:
            return 0
        return self.metrics["cache_hits"] / total
    
    def get_uptime(self):
        """Get time since monitoring started."""
        return datetime.now() - self.start_time
    
    def get_report(self):
        """Generate memory system report."""
        return {
            **self.metrics,
            "cache_hit_rate": f"{self.get_cache_hit_rate():.2%}",
            "uptime": str(self.get_uptime()),
            "timestamp": datetime.now().isoformat(),
        }
    
    def reset(self):
        """Reset all metrics."""
        self.__init__()


# Usage
if __name__ == "__main__":
    monitor = MemoryMonitor()
    
    # Simulate activity
    monitor.log_conversation(message_count=10)
    monitor.log_conversation(message_count=5)
    monitor.log_access("user_123", is_cache_hit=True)
    monitor.log_access("user_456", is_cache_hit=False)
    monitor.log_access("user_123", is_cache_hit=True)
    monitor.log_storage_operation()
    
    print("Memory System Report:")
    report = monitor.get_report()
    for key, value in report.items():
        print(f"  {key}: {value}")
