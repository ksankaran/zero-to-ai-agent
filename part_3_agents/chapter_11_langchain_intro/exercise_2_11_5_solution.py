# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: exercise_2_11_5_solution.py

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import time
from collections import deque
import statistics

load_dotenv()

class SpeedOptimizedAssistant:
    def __init__(self):
        # Initialize models
        self.models = {
            "gpt-3.5-turbo": {
                "instance": ChatOpenAI(model="gpt-3.5-turbo"),
                "response_times": deque(maxlen=10),  # Keep last 10 times
                "failures": 0,
                "total_calls": 0
            },
            "gpt-4": {
                "instance": ChatOpenAI(model="gpt-4"),
                "response_times": deque(maxlen=10),
                "failures": 0,
                "total_calls": 0
            },
            "llama2": {
                "instance": Ollama(model="llama2"),
                "response_times": deque(maxlen=10),
                "failures": 0,
                "total_calls": 0
            }
        }
        
        # Performance thresholds
        self.timeout_seconds = 10
        self.max_failures = 3
    
    def measure_response_time(self, model_name, prompt):
        """Measure how long a model takes to respond"""
        model_data = self.models[model_name]
        model = model_data["instance"]
        
        start = time.time()
        try:
            response = model.invoke(prompt)
            elapsed = time.time() - start
            
            # Record success
            model_data["response_times"].append(elapsed)
            model_data["total_calls"] += 1
            
            # Extract content
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            return {
                "success": True,
                "time": elapsed,
                "content": content
            }
            
        except Exception as e:
            elapsed = time.time() - start
            model_data["failures"] += 1
            model_data["total_calls"] += 1
            
            return {
                "success": False,
                "time": elapsed,
                "error": str(e)
            }
    
    def get_fastest_available(self):
        """Get the fastest available model"""
        available_models = []
        
        for name, data in self.models.items():
            # Skip models with too many failures
            if data["failures"] >= self.max_failures:
                continue
            
            # Calculate average response time
            if data["response_times"]:
                avg_time = statistics.mean(data["response_times"])
                available_models.append((name, avg_time))
            else:
                # No data yet, assume reasonable default
                default_times = {
                    "gpt-3.5-turbo": 1.0,
                    "gpt-4": 3.0,
                    "llama2": 2.0
                }
                available_models.append((name, default_times.get(name, 5.0)))
        
        if not available_models:
            return None
        
        # Sort by speed
        available_models.sort(key=lambda x: x[1])
        return available_models[0][0]
    
    def chat_with_fallback(self, prompt):
        """Chat with automatic fallback to slower models"""
        
        # Try fastest model first
        fastest = self.get_fastest_available()
        if not fastest:
            return "No models available!"
        
        print(f"⚡ Using {fastest} (fastest available)")
        
        # Try primary model
        result = self.measure_response_time(fastest, prompt)
        
        if result["success"]:
            print(f"✅ Response in {result['time']:.2f}s")
            return result["content"]
        
        # Fallback to other models
        print(f"❌ {fastest} failed, trying fallbacks...")
        
        for name, data in sorted(self.models.items(), 
                                 key=lambda x: len(x[1]["response_times"])):
            if name == fastest:
                continue
            
            print(f"🔄 Trying {name}...")
            result = self.measure_response_time(name, prompt)
            
            if result["success"]:
                print(f"✅ Fallback successful in {result['time']:.2f}s")
                return result["content"]
        
        return "All models failed!"
    
    def get_statistics(self):
        """Get performance statistics"""
        stats = {}
        
        for name, data in self.models.items():
            if data["response_times"]:
                stats[name] = {
                    "average_time": statistics.mean(data["response_times"]),
                    "median_time": statistics.median(data["response_times"]),
                    "min_time": min(data["response_times"]),
                    "max_time": max(data["response_times"]),
                    "success_rate": ((data["total_calls"] - data["failures"]) / 
                                   data["total_calls"] * 100) if data["total_calls"] > 0 else 0,
                    "total_calls": data["total_calls"]
                }
            else:
                stats[name] = {
                    "average_time": None,
                    "success_rate": 0,
                    "total_calls": 0
                }
        
        return stats
    
    def optimize_for_speed(self):
        """Reorder models based on actual performance"""
        stats = self.get_statistics()
        
        recommendations = []
        for name, stat in stats.items():
            if stat["average_time"] is not None:
                score = stat["average_time"] * (1 + (100 - stat["success_rate"]) / 100)
                recommendations.append((name, score))
        
        recommendations.sort(key=lambda x: x[1])
        
        if recommendations:
            return f"Recommended order: {' -> '.join([r[0] for r in recommendations])}"
        return "Not enough data for optimization"

# Test the speed optimizer
def demo_speed_optimizer():
    optimizer = SpeedOptimizedAssistant()
    
    queries = [
        "What is 2+2?",
        "Explain the meaning of life",
        "Write a haiku about speed",
        "What's the capital of France?",
        "Describe quantum computing"
    ]
    
    print("⚡ Speed-Optimized Assistant Demo")
    print("="*60)
    
    for query in queries:
        print(f"\n❓ Query: {query}")
        response = optimizer.chat_with_fallback(query)
        print(f"📝 Response: {response[:100]}...")
    
    # Show statistics
    print("\n" + "="*60)
    print("📊 PERFORMANCE STATISTICS:")
    
    stats = optimizer.get_statistics()
    for model, data in stats.items():
        print(f"\n{model}:")
        if data["average_time"]:
            print(f"  Average: {data['average_time']:.2f}s")
            print(f"  Range: {data['min_time']:.2f}s - {data['max_time']:.2f}s")
            print(f"  Success: {data['success_rate']:.1f}%")
            print(f"  Calls: {data['total_calls']}")
    
    # Get optimization recommendation
    print("\n💡 Optimization:")
    print(optimizer.optimize_for_speed())

if __name__ == "__main__":
    demo_speed_optimizer()
