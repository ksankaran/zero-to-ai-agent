# From: Zero to AI Agent, Chapter 7, Section 7.7
# File: cost_optimization.py

"""
Battle-tested strategies to minimize API costs while maintaining quality.
Includes model selection, caching, and batch processing.
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


def smart_model_selection(task_type: str, complexity: int, max_cost_per_request: float = 0.01) -> str:
    """
    Choose the cheapest model that can handle the task
    
    Args:
        task_type: Type of task (e.g., "qa", "code", "creative")
        complexity: Complexity score 1-10
        max_cost_per_request: Maximum acceptable cost
    
    Returns:
        Recommended model name
    """
    
    # Model capabilities and costs (prices as of 2024)
    model_capabilities = {
        "gemini-pro": {
            "cost_per_1k": 0.0005,  # Very cheap!
            "good_for": ["simple_qa", "basic_chat", "translations"],
            "complexity_score": 6,
            "speed": "fast",
            "context_window": 32000
        },
        "claude-3-haiku": {
            "cost_per_1k": 0.0015,
            "good_for": ["quick_responses", "high_volume", "summaries"],
            "complexity_score": 6,
            "speed": "very_fast",
            "context_window": 200000
        },
        "gpt-3.5-turbo": {
            "cost_per_1k": 0.002,
            "good_for": ["simple_qa", "basic_chat", "summaries", "simple_code"],
            "complexity_score": 7,
            "speed": "fast",
            "context_window": 16000
        },
        "claude-3-sonnet": {
            "cost_per_1k": 0.018,
            "good_for": ["complex_qa", "analysis", "creative", "code"],
            "complexity_score": 8,
            "speed": "medium",
            "context_window": 200000
        },
        "gpt-4": {
            "cost_per_1k": 0.09,
            "good_for": ["complex_reasoning", "code_generation", "analysis", "math"],
            "complexity_score": 10,
            "speed": "slow",
            "context_window": 128000
        },
        "claude-3-opus": {
            "cost_per_1k": 0.09,
            "good_for": ["complex_reasoning", "research", "long_documents"],
            "complexity_score": 10,
            "speed": "slow",
            "context_window": 200000
        }
    }
    
    # Task-specific recommendations
    task_models = {
        "simple_qa": ["gemini-pro", "claude-3-haiku", "gpt-3.5-turbo"],
        "code_generation": ["gpt-3.5-turbo", "claude-3-sonnet", "gpt-4"],
        "creative_writing": ["claude-3-sonnet", "gpt-4"],
        "data_analysis": ["gpt-3.5-turbo", "claude-3-sonnet", "gpt-4"],
        "translation": ["gemini-pro", "gpt-3.5-turbo"],
        "summarization": ["claude-3-haiku", "gpt-3.5-turbo"],
    }
    
    # Get suitable models for task
    suitable_models = task_models.get(task_type, list(model_capabilities.keys()))
    
    # Filter by complexity
    candidates = []
    for model in suitable_models:
        if model in model_capabilities:
            model_info = model_capabilities[model]
            if model_info["complexity_score"] >= min(complexity, 10):
                candidates.append((model, model_info))
    
    # Sort by cost
    candidates.sort(key=lambda x: x[1]["cost_per_1k"])
    
    # Return cheapest suitable model
    if candidates:
        selected = candidates[0][0]
        print(f"📊 Model Selection:")
        print(f"   Task: {task_type} (complexity: {complexity}/10)")
        print(f"   Selected: {selected}")
        print(f"   Cost: ${candidates[0][1]['cost_per_1k']:.4f}/1K tokens")
        print(f"   Alternatives considered: {[c[0] for c in candidates[1:3]]}")
        return selected
    
    # Default fallback
    return "gpt-3.5-turbo"


class ResponseCache:
    """
    Cache responses to avoid repeated API calls
    Saves money by reusing previous responses
    """
    
    def __init__(self, cache_duration_hours: int = 24, max_cache_size: int = 1000):
        """
        Initialize cache
        
        Args:
            cache_duration_hours: How long to keep cached responses
            max_cache_size: Maximum number of cached items
        """
        self.cache = {}
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.max_cache_size = max_cache_size
        
        # Statistics
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_saved = 0.0
        self.bytes_saved = 0
    
    def _get_cache_key(self, prompt: str, model: str = "default", temperature: float = 0.7) -> str:
        """Generate unique cache key"""
        content = f"{prompt}_{model}_{temperature}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> Optional[Any]:
        """
        Try to get cached response
        
        Args:
            prompt: The prompt to look up
            model: Model name
            temperature: Temperature setting
        
        Returns:
            Cached response or None
        """
        key = self._get_cache_key(prompt, model, temperature)
        
        if key in self.cache:
            entry = self.cache[key]
            # Check if still valid
            if datetime.now() - entry["timestamp"] < self.cache_duration:
                self.cache_hits += 1
                self.total_saved += entry["cost"]
                self.bytes_saved += len(str(entry["response"]))
                
                # Update access time for LRU
                entry["last_accessed"] = datetime.now()
                
                print(f"💰 Cache hit! Saved ${entry['cost']:.4f}")
                return entry["response"]
            else:
                # Expired, remove it
                del self.cache[key]
        
        self.cache_misses += 1
        return None
    
    def set(self, prompt: str, response: Any, cost: float, model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """
        Cache a response
        
        Args:
            prompt: The prompt
            response: The response to cache
            cost: Cost of this API call
            model: Model name
            temperature: Temperature setting
        """
        # Check cache size
        if len(self.cache) >= self.max_cache_size:
            self._evict_oldest()
        
        key = self._get_cache_key(prompt, model, temperature)
        self.cache[key] = {
            "response": response,
            "timestamp": datetime.now(),
            "last_accessed": datetime.now(),
            "cost": cost,
            "model": model
        }
    
    def _evict_oldest(self):
        """Remove least recently used item"""
        if not self.cache:
            return
        
        # Find least recently accessed
        oldest_key = min(self.cache.keys(), 
                        key=lambda k: self.cache[k]["last_accessed"])
        del self.cache[oldest_key]
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / max(1, total_requests)) * 100
        
        # Calculate cache value
        cache_value = sum(entry["cost"] for entry in self.cache.values())
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "total_saved": f"${self.total_saved:.2f}",
            "bytes_saved": f"{self.bytes_saved:,}",
            "cache_size": len(self.cache),
            "cache_value": f"${cache_value:.2f}"
        }
    
    def clear_expired(self):
        """Remove expired entries"""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.cache.items()
            if now - entry["timestamp"] >= self.cache_duration
        ]
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)


def batch_process_efficiently(items: List[str], batch_size: int = 10) -> Dict:
    """
    Process multiple items in single API calls when possible
    
    Args:
        items: List of items to process
        batch_size: Items per API call
    
    Returns:
        Results and cost information
    """
    
    total_cost = 0
    results = []
    api_calls = 0
    
    print(f"\n📦 Batch Processing {len(items)} items")
    print(f"   Batch size: {batch_size}")
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        api_calls += 1
        
        # Combine into single prompt
        combined_prompt = "Process each item separately and number the responses:\n\n"
        for j, item in enumerate(batch, 1):
            combined_prompt += f"{j}. {item}\n"
        
        # Estimate cost (simplified)
        estimated_tokens = len(combined_prompt) // 4 + (100 * len(batch))  # Assume 100 tokens per response
        batch_cost = (estimated_tokens / 1000) * 0.002  # GPT-3.5 pricing
        total_cost += batch_cost
        
        print(f"   Batch {api_calls}: {len(batch)} items, ~{estimated_tokens} tokens, ${batch_cost:.4f}")
        
        # Simulate processing
        batch_results = [f"Processed: {item}" for item in batch]
        results.extend(batch_results)
    
    # Calculate savings
    individual_cost = len(items) * ((150 / 1000) * 0.002)  # If processed individually
    savings = individual_cost - total_cost
    savings_percent = (savings / individual_cost) * 100
    
    print(f"\n💰 Batch Processing Results:")
    print(f"   Items processed: {len(items)}")
    print(f"   API calls made: {api_calls}")
    print(f"   Total cost: ${total_cost:.4f}")
    print(f"   Cost if individual: ${individual_cost:.4f}")
    print(f"   Saved: ${savings:.4f} ({savings_percent:.1f}%)")
    
    return {
        "results": results,
        "total_cost": total_cost,
        "api_calls": api_calls,
        "savings": savings
    }


class CostOptimizer:
    """
    Comprehensive cost optimization manager
    """
    
    def __init__(self, daily_budget: float = 10.0):
        """
        Initialize cost optimizer
        
        Args:
            daily_budget: Maximum daily spending
        """
        self.daily_budget = daily_budget
        self.cache = ResponseCache()
        self.model_usage = {}
        self.optimization_stats = {
            "cache_savings": 0,
            "model_downgrades": 0,
            "batch_savings": 0
        }
    
    def optimize_request(self, prompt: str, task_type: str = "simple_qa") -> Dict:
        """
        Optimize a request for cost
        
        Args:
            prompt: The prompt to process
            task_type: Type of task
        
        Returns:
            Optimization recommendations
        """
        recommendations = {}
        
        # 1. Check cache first
        cached = self.cache.get(prompt)
        if cached:
            self.optimization_stats["cache_savings"] += 1
            recommendations["use_cache"] = True
            recommendations["cached_response"] = cached
            return recommendations
        
        # 2. Estimate complexity
        complexity = self._estimate_complexity(prompt)
        
        # 3. Select optimal model
        model = smart_model_selection(task_type, complexity)
        recommendations["model"] = model
        
        # 4. Check if we should batch
        recommendations["can_batch"] = len(prompt) < 500  # Short enough to batch
        
        # 5. Suggest optimizations
        if complexity < 5:
            recommendations["optimizations"] = [
                "Consider using cheaper model",
                "Enable aggressive caching",
                "Batch with similar requests"
            ]
        
        return recommendations
    
    def _estimate_complexity(self, prompt: str) -> int:
        """Estimate task complexity from prompt"""
        complexity = 3  # Base complexity
        
        # Increase for certain keywords
        complex_keywords = ["analyze", "explain", "compare", "debug", "optimize", "create"]
        for keyword in complex_keywords:
            if keyword in prompt.lower():
                complexity += 2
        
        # Increase for length
        if len(prompt) > 500:
            complexity += 2
        if len(prompt) > 1000:
            complexity += 2
        
        # Cap at 10
        return min(complexity, 10)
    
    def get_optimization_report(self) -> str:
        """Generate optimization report"""
        cache_stats = self.cache.get_stats()
        
        report = []
        report.append("="*60)
        report.append("COST OPTIMIZATION REPORT")
        report.append("="*60)
        
        report.append("\n📊 Cache Performance:")
        for key, value in cache_stats.items():
            report.append(f"   {key}: {value}")
        
        report.append("\n💰 Savings:")
        report.append(f"   From caching: ${self.cache.total_saved:.2f}")
        report.append(f"   From batching: ${self.optimization_stats['batch_savings']:.2f}")
        report.append(f"   Model downgrades: {self.optimization_stats['model_downgrades']}")
        
        report.append("\n💡 Recommendations:")
        if cache_stats["cache_hits"] < cache_stats["cache_misses"]:
            report.append("   • Increase cache duration or size")
        report.append("   • Batch similar requests together")
        report.append("   • Use cheaper models for simple tasks")
        
        return "\n".join(report)


def demonstrate_optimization():
    """Demonstrate cost optimization techniques"""
    
    print("="*60)
    print("COST OPTIMIZATION DEMONSTRATION")
    print("="*60)
    
    # 1. Model Selection
    print("\n1️⃣ SMART MODEL SELECTION")
    print("-" * 40)
    
    tasks = [
        ("What is 2+2?", "simple_qa", 2),
        ("Write a Python function to sort a list", "code_generation", 6),
        ("Explain quantum computing in detail", "complex_qa", 9)
    ]
    
    for prompt, task_type, complexity in tasks:
        print(f"\nPrompt: '{prompt[:50]}...'")
        model = smart_model_selection(task_type, complexity)
    
    # 2. Caching
    print("\n2️⃣ RESPONSE CACHING")
    print("-" * 40)
    
    cache = ResponseCache()
    
    # Simulate repeated requests
    prompts = [
        "What is Python?",
        "Explain AI",
        "What is Python?",  # Duplicate
        "How does ML work?",
        "What is Python?"   # Another duplicate
    ]
    
    for prompt in prompts:
        cached = cache.get(prompt)
        if not cached:
            # Simulate API call
            print(f"📤 API call for: '{prompt}'")
            cache.set(prompt, f"Response to: {prompt}", cost=0.002)
        else:
            print(f"💰 Using cached response for: '{prompt}'")
    
    print(f"\nCache stats: {cache.get_stats()}")
    
    # 3. Batch Processing
    print("\n3️⃣ BATCH PROCESSING")
    print("-" * 40)
    
    items = [f"Item {i}" for i in range(25)]
    batch_process_efficiently(items, batch_size=5)
    
    # 4. Complete Optimization
    print("\n4️⃣ COMPLETE OPTIMIZATION")
    print("-" * 40)
    
    optimizer = CostOptimizer(daily_budget=5.0)
    
    test_prompts = [
        ("Hello", "simple_qa"),
        ("Write a complex algorithm", "code_generation"),
        ("Hello", "simple_qa"),  # Duplicate - should cache
        ("Analyze this data", "data_analysis")
    ]
    
    for prompt, task in test_prompts:
        print(f"\n📝 Request: '{prompt}'")
        recommendations = optimizer.optimize_request(prompt, task)
        
        if recommendations.get("use_cache"):
            print("   ✅ Using cached response!")
        else:
            print(f"   📊 Recommended model: {recommendations.get('model')}")
            print(f"   📦 Can batch: {recommendations.get('can_batch')}")
    
    print("\n" + optimizer.get_optimization_report())


if __name__ == "__main__":
    demonstrate_optimization()
