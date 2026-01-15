# From: Zero to AI Agent, Chapter 11, Section 11.7
# File: exercise_2_11_7_solution.py

import time
from datetime import datetime
from collections import deque
import statistics

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "llm_calls": deque(maxlen=100),
            "chain_executions": deque(maxlen=100),
            "prompt_formatting": deque(maxlen=100),
            "memory_operations": deque(maxlen=100),
            "tool_calls": deque(maxlen=100)
        }
        
        self.slow_threshold = {
            "llm_calls": 2.0,
            "chain_executions": 3.0,
            "prompt_formatting": 0.1,
            "memory_operations": 0.5,
            "tool_calls": 1.0
        }
        
        self.alerts = []
    
    def measure(self, component_type, func, *args, **kwargs):
        """Measure execution time of a component"""
        start = time.time()
        
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            
            # Record metric
            self.metrics[component_type].append({
                "time": elapsed,
                "timestamp": datetime.now(),
                "success": True
            })
            
            # Check for slowness
            if elapsed > self.slow_threshold[component_type]:
                self.alert_slowdown(component_type, elapsed)
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start
            self.metrics[component_type].append({
                "time": elapsed,
                "timestamp": datetime.now(),
                "success": False,
                "error": str(e)
            })
            raise
    
    def alert_slowdown(self, component_type, time_taken):
        """Alert on performance degradation"""
        alert = {
            "timestamp": datetime.now(),
            "component": component_type,
            "time": time_taken,
            "threshold": self.slow_threshold[component_type],
            "severity": "warning" if time_taken < self.slow_threshold[component_type] * 2 else "critical"
        }
        
        self.alerts.append(alert)
        print(f"⚠️ PERFORMANCE ALERT: {component_type} took {time_taken:.2f}s (threshold: {self.slow_threshold[component_type]}s)")
    
    def get_statistics(self, component_type):
        """Get performance statistics for a component"""
        if component_type not in self.metrics or not self.metrics[component_type]:
            return None
        
        times = [m["time"] for m in self.metrics[component_type] if m["success"]]
        
        if not times:
            return None
        
        return {
            "component": component_type,
            "count": len(times),
            "avg": statistics.mean(times),
            "median": statistics.median(times),
            "min": min(times),
            "max": max(times),
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0
        }
    
    def identify_bottlenecks(self):
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        for component_type in self.metrics:
            stats = self.get_statistics(component_type)
            if stats and stats["avg"] > self.slow_threshold[component_type]:
                bottlenecks.append({
                    "component": component_type,
                    "avg_time": stats["avg"],
                    "severity": "high" if stats["avg"] > self.slow_threshold[component_type] * 2 else "medium"
                })
        
        return sorted(bottlenecks, key=lambda x: x["avg_time"], reverse=True)
    
    def suggest_optimizations(self):
        """Suggest optimizations based on metrics"""
        suggestions = []
        bottlenecks = self.identify_bottlenecks()
        
        for bottleneck in bottlenecks:
            component = bottleneck["component"]
            
            if component == "llm_calls":
                suggestions.append({
                    "component": component,
                    "suggestion": "Consider using GPT-3.5-turbo instead of GPT-4 for faster response",
                    "potential_improvement": "50-70% faster"
                })
            elif component == "chain_executions":
                suggestions.append({
                    "component": component,
                    "suggestion": "Break complex chains into simpler steps",
                    "potential_improvement": "20-30% faster"
                })
            elif component == "memory_operations":
                suggestions.append({
                    "component": component,
                    "suggestion": "Use ConversationSummaryMemory for long conversations",
                    "potential_improvement": "40-60% faster"
                })
        
        return suggestions
    
    def display_dashboard(self):
        """Display performance dashboard"""
        print("\n" + "="*60)
        print("📊 PERFORMANCE MONITOR DASHBOARD")
        print("="*60)
        
        # Component statistics
        print("\n⏱️ Component Performance:")
        for component_type in self.metrics:
            stats = self.get_statistics(component_type)
            if stats:
                print(f"\n  {component_type}:")
                print(f"    Calls: {stats['count']}")
                print(f"    Avg: {stats['avg']:.3f}s")
                print(f"    Min/Max: {stats['min']:.3f}s / {stats['max']:.3f}s")
        
        # Bottlenecks
        bottlenecks = self.identify_bottlenecks()
        if bottlenecks:
            print("\n🚨 Bottlenecks:")
            for b in bottlenecks:
                print(f"  {b['component']}: {b['avg_time']:.3f}s ({b['severity']} severity)")
        
        # Optimizations
        suggestions = self.suggest_optimizations()
        if suggestions:
            print("\n💡 Optimization Suggestions:")
            for s in suggestions:
                print(f"  {s['component']}:")
                print(f"    {s['suggestion']}")
                print(f"    Expected: {s['potential_improvement']}")
        
        # Recent alerts
        if self.alerts:
            print(f"\n⚠️ Recent Alerts ({len(self.alerts)} total):")
            for alert in self.alerts[-3:]:
                print(f"  [{alert['timestamp'].strftime('%H:%M:%S')}] {alert['component']}: {alert['time']:.2f}s")
        
        print("\n" + "="*60)

# Demo usage
if __name__ == "__main__":
    monitor = PerformanceMonitor()
    
    # Simulate some measurements
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Measure LLM call
    llm = ChatOpenAI()
    monitor.measure("llm_calls", llm.invoke, "Test message")
    
    # Measure prompt formatting
    prompt = ChatPromptTemplate.from_template("Test: {input}")
    monitor.measure("prompt_formatting", prompt.format_messages, input="test")
    
    # Display results
    monitor.display_dashboard()
