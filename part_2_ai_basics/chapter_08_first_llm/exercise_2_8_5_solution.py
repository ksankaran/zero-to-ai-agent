# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: exercise_2_8_5_solution.py

"""Track API response times"""

import time
from datetime import datetime

class ResponseTimer:
    """Monitor API response performance"""
    
    def __init__(self):
        self.response_times = []
        self.slow_threshold = 2.0  # seconds
    
    def start(self):
        """Start timing"""
        return time.time()
    
    def end(self, start_time):
        """End timing and record"""
        elapsed = time.time() - start_time
        self.response_times.append({
            'time': elapsed,
            'timestamp': datetime.now().isoformat()
        })
        return elapsed
    
    def is_slow(self, response_time):
        """Check if response was slow"""
        return response_time > self.slow_threshold
    
    def get_average(self):
        """Get average response time"""
        if not self.response_times:
            return 0
        return sum(r['time'] for r in self.response_times) / len(self.response_times)
    
    def get_stats(self):
        """Get timing statistics"""
        if not self.response_times:
            return "No timing data yet"
        
        times = [r['time'] for r in self.response_times]
        return {
            'average': self.get_average(),
            'min': min(times),
            'max': max(times),
            'total_calls': len(times),
            'slow_calls': sum(1 for t in times if t > self.slow_threshold)
        }
    
    def format_stats(self):
        """Format stats for display"""
        stats = self.get_stats()
        if isinstance(stats, str):
            return stats
        
        return f"""⏱️ Response Time Stats:
  Average: {stats['average']:.2f}s
  Fastest: {stats['min']:.2f}s
  Slowest: {stats['max']:.2f}s
  Total calls: {stats['total_calls']}
  Slow calls: {stats['slow_calls']}"""
