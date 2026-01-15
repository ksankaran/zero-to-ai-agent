# From: Zero to AI Agent, Chapter 7, Section 7.7
# File: chapter7_challenge_project.py

"""
Chapter 7 Challenge Project: Multi-Provider AI Assistant Hub
Build an AI assistant that intelligently switches between providers,
manages costs, and handles rate limits.
"""

import os
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from collections import deque


# =======================
# Configuration
# =======================

@dataclass
class ModelConfig:
    """Configuration for each model"""
    provider: str
    name: str
    input_cost_per_1k: float
    output_cost_per_1k: float
    rpm_limit: int
    tpm_limit: int
    complexity_score: int  # 1-10, how capable is this model
    context_window: int


class Provider(Enum):
    """Available providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"  
    GOOGLE = "google"
    LOCAL = "local"  # For Ollama or similar


class AssistantHub:
    """
    Your Multi-Provider AI Assistant Hub
    Implements everything from Chapter 7!
    """
    
    def __init__(self):
        """Initialize the assistant hub"""
        
        # Model configurations
        self.models = {
            "gpt-3.5-turbo": ModelConfig(
                provider="openai",
                name="gpt-3.5-turbo",
                input_cost_per_1k=0.0005,
                output_cost_per_1k=0.0015,
                rpm_limit=90,
                tpm_limit=90000,
                complexity_score=7,
                context_window=16000
            ),
            "gemini-pro": ModelConfig(
                provider="google",
                name="gemini-pro",
                input_cost_per_1k=0.000125,
                output_cost_per_1k=0.000375,
                rpm_limit=60,
                tpm_limit=1000000,
                complexity_score=6,
                context_window=32000
            ),
            "claude-3-haiku": ModelConfig(
                provider="anthropic",
                name="claude-3-haiku-20240307",
                input_cost_per_1k=0.00025,
                output_cost_per_1k=0.00125,
                rpm_limit=50,
                tpm_limit=100000,
                complexity_score=6,
                context_window=200000
            )
            # TODO: Add more models
        }
        
        # Initialize components
        self.cache = {}  # Simple cache implementation
        self.cache_duration = timedelta(hours=24)
        
        self.cost_tracker = {
            "total": 0.0,
            "by_model": {},
            "daily": {}
        }
        
        self.rate_limiters = {}  # One per model
        self.conversation_history = []
        self.available_providers = []
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_tokens": 0,
            "errors": 0
        }
        
        # Load API keys
        self._load_api_keys()
        
        # Initialize rate limiters
        self._init_rate_limiters()
    
    def _load_api_keys(self):
        """
        Load API keys from environment variables
        TODO: Implement secure key loading from Chapter 7.6
        """
        self.api_keys = {}
        
        # Try to load from environment
        if os.getenv("OPENAI_API_KEY"):
            self.api_keys["openai"] = os.getenv("OPENAI_API_KEY")
            self.available_providers.append("openai")
            print("✅ OpenAI API key loaded")
        
        if os.getenv("ANTHROPIC_API_KEY"):
            self.api_keys["anthropic"] = os.getenv("ANTHROPIC_API_KEY")
            self.available_providers.append("anthropic")
            print("✅ Anthropic API key loaded")
        
        if os.getenv("GOOGLE_API_KEY"):
            self.api_keys["google"] = os.getenv("GOOGLE_API_KEY")
            self.available_providers.append("google")
            print("✅ Google API key loaded")
        
        if not self.available_providers:
            print("⚠️ No API keys found! Set environment variables:")
            print("  OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY")
    
    def _init_rate_limiters(self):
        """Initialize rate limiters for each model"""
        for model_name, config in self.models.items():
            self.rate_limiters[model_name] = {
                "request_times": deque(),
                "token_counts": deque(),
                "last_request": None
            }
    
    def _estimate_complexity(self, prompt: str) -> int:
        """
        Estimate task complexity (1-10) based on prompt
        
        TODO: Improve this with better heuristics
        """
        complexity = 3  # Base complexity
        
        # Length-based estimation
        if len(prompt) > 500:
            complexity += 2
        if len(prompt) > 1000:
            complexity += 2
        
        # Keyword-based estimation
        complex_keywords = [
            "analyze", "explain in detail", "compare",
            "write code", "debug", "optimize", 
            "create", "design", "comprehensive"
        ]
        
        for keyword in complex_keywords:
            if keyword in prompt.lower():
                complexity += 1
        
        # Cap at 10
        return min(complexity, 10)
    
    def _select_model(self, prompt: str, max_cost: float = 0.01) -> Optional[str]:
        """
        Select the best model for the task
        
        TODO: Implement smart selection logic
        """
        complexity = self._estimate_complexity(prompt)
        
        # Filter models by availability and complexity
        candidates = []
        for model_name, config in self.models.items():
            if config.provider in self.available_providers:
                if config.complexity_score >= complexity:
                    # Estimate cost
                    estimated_tokens = len(prompt) // 4 + 200  # Input + output estimate
                    estimated_cost = (estimated_tokens / 1000) * (
                        config.input_cost_per_1k + config.output_cost_per_1k
                    )
                    
                    if estimated_cost <= max_cost:
                        candidates.append((model_name, estimated_cost))
        
        if not candidates:
            print("⚠️ No suitable model found within budget")
            return None
        
        # Sort by cost and return cheapest
        candidates.sort(key=lambda x: x[1])
        selected = candidates[0][0]
        
        print(f"📊 Selected model: {selected} (complexity: {complexity}/10)")
        return selected
    
    def _check_rate_limits(self, model: str, estimated_tokens: int) -> bool:
        """
        Check if we can make a request without hitting rate limits
        
        TODO: Implement rate limit checking
        """
        if model not in self.rate_limiters:
            return True
        
        config = self.models[model]
        limiter = self.rate_limiters[model]
        
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Clean old entries
        while limiter["request_times"] and limiter["request_times"][0] < minute_ago:
            limiter["request_times"].popleft()
            if limiter["token_counts"]:
                limiter["token_counts"].popleft()
        
        # Check limits
        if len(limiter["request_times"]) >= config.rpm_limit:
            print(f"⏳ Rate limit: {model} at {config.rpm_limit} RPM")
            return False
        
        current_tokens = sum(limiter["token_counts"])
        if current_tokens + estimated_tokens > config.tpm_limit:
            print(f"⏳ Token limit: {model} at {config.tpm_limit} TPM")
            return False
        
        return True
    
    def _get_cache_key(self, prompt: str, model: str) -> str:
        """Generate cache key"""
        content = f"{prompt}_{model}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _check_cache(self, prompt: str, model: str) -> Optional[Any]:
        """Check if response is cached"""
        key = self._get_cache_key(prompt, model)
        
        if key in self.cache:
            entry = self.cache[key]
            # Check if still valid
            if datetime.now() - entry["timestamp"] < self.cache_duration:
                self.stats["cache_hits"] += 1
                print(f"💰 Cache hit! Saved ${entry['cost']:.4f}")
                return entry["response"]
        
        self.stats["cache_misses"] += 1
        return None
    
    def _cache_response(self, prompt: str, model: str, response: str, cost: float):
        """Cache a response"""
        key = self._get_cache_key(prompt, model)
        self.cache[key] = {
            "response": response,
            "timestamp": datetime.now(),
            "cost": cost,
            "model": model
        }
    
    def _make_api_call(self, prompt: str, model: str) -> Optional[Dict]:
        """
        Make actual API call to the selected model
        
        TODO: Implement actual API calls for each provider
        """
        config = self.models[model]
        
        # Simulate API call for demo
        print(f"🔄 Making API call to {model}...")
        time.sleep(0.5)  # Simulate latency
        
        # TODO: Replace with actual API calls
        # if config.provider == "openai":
        #     response = self._call_openai(prompt, model)
        # elif config.provider == "anthropic":
        #     response = self._call_anthropic(prompt, model)
        # elif config.provider == "google":
        #     response = self._call_google(prompt, model)
        
        # Simulated response
        response = {
            "text": f"[Simulated response from {model}] This is a response to: {prompt[:50]}...",
            "tokens_used": len(prompt) // 4 + 150,
            "model": model
        }
        
        return response
    
    def _track_cost(self, model: str, tokens: int):
        """Track costs"""
        config = self.models[model]
        
        # Estimate input/output split (rough)
        input_tokens = tokens * 0.3
        output_tokens = tokens * 0.7
        
        cost = (
            (input_tokens / 1000) * config.input_cost_per_1k +
            (output_tokens / 1000) * config.output_cost_per_1k
        )
        
        # Update tracking
        self.cost_tracker["total"] += cost
        
        if model not in self.cost_tracker["by_model"]:
            self.cost_tracker["by_model"][model] = 0
        self.cost_tracker["by_model"][model] += cost
        
        today = str(datetime.now().date())
        if today not in self.cost_tracker["daily"]:
            self.cost_tracker["daily"][today] = 0
        self.cost_tracker["daily"][today] += cost
        
        return cost
    
    def _update_rate_limiter(self, model: str, tokens: int):
        """Update rate limiter after request"""
        if model in self.rate_limiters:
            limiter = self.rate_limiters[model]
            limiter["request_times"].append(datetime.now())
            limiter["token_counts"].append(tokens)
            limiter["last_request"] = datetime.now()
    
    def chat(self, user_input: str) -> str:
        """
        Main chat interface
        
        This is where everything comes together!
        """
        self.stats["total_requests"] += 1
        
        # Step 1: Select best model
        model = self._select_model(user_input)
        if not model:
            return "Sorry, no suitable model available within budget constraints."
        
        # Step 2: Check cache
        cached = self._check_cache(user_input, model)
        if cached:
            return cached
        
        # Step 3: Check rate limits
        estimated_tokens = len(user_input) // 4 + 200
        
        if not self._check_rate_limits(model, estimated_tokens):
            # Try fallback model
            print("🔄 Trying fallback model...")
            for fallback_model in self.models.keys():
                if fallback_model != model:
                    if self._check_rate_limits(fallback_model, estimated_tokens):
                        model = fallback_model
                        print(f"✅ Using fallback: {model}")
                        break
            else:
                return "Rate limits exceeded on all models. Please wait a moment."
        
        # Step 4: Make API call
        try:
            response = self._make_api_call(user_input, model)
            if not response:
                self.stats["errors"] += 1
                return "Failed to get response from API."
            
            response_text = response["text"]
            tokens_used = response["tokens_used"]
            
        except Exception as e:
            self.stats["errors"] += 1
            print(f"❌ API call failed: {e}")
            return f"Error: {str(e)}"
        
        # Step 5: Track costs
        cost = self._track_cost(model, tokens_used)
        print(f"💰 Cost: ${cost:.4f}")
        
        # Step 6: Update rate limiter
        self._update_rate_limiter(model, tokens_used)
        
        # Step 7: Cache response
        self._cache_response(user_input, model, response_text, cost)
        
        # Step 8: Update statistics
        self.stats["total_tokens"] += tokens_used
        
        # Step 9: Update conversation history (limit size)
        self.conversation_history.append({
            "timestamp": datetime.now(),
            "user": user_input,
            "assistant": response_text,
            "model": model,
            "cost": cost
        })
        
        # Keep only last 20 exchanges
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response_text
    
    def get_stats(self) -> Dict:
        """Generate statistics report"""
        
        cache_hit_rate = 0
        if self.stats["cache_hits"] + self.stats["cache_misses"] > 0:
            cache_hit_rate = (
                self.stats["cache_hits"] / 
                (self.stats["cache_hits"] + self.stats["cache_misses"])
            ) * 100
        
        stats = {
            "total_cost": f"${self.cost_tracker['total']:.4f}",
            "total_requests": self.stats["total_requests"],
            "total_tokens": self.stats["total_tokens"],
            "cache_hit_rate": f"{cache_hit_rate:.1f}%",
            "cache_hits": self.stats["cache_hits"],
            "cache_misses": self.stats["cache_misses"],
            "errors": self.stats["errors"],
            "cost_by_model": {
                model: f"${cost:.4f}"
                for model, cost in self.cost_tracker["by_model"].items()
            },
            "available_providers": self.available_providers,
            "conversation_length": len(self.conversation_history)
        }
        
        # Add today's cost
        today = str(datetime.now().date())
        if today in self.cost_tracker["daily"]:
            stats["today_cost"] = f"${self.cost_tracker['daily'][today]:.4f}"
        
        return stats
    
    def export_conversation(self, filename: str):
        """Export conversation history"""
        
        export_data = {
            "export_time": datetime.now().isoformat(),
            "statistics": self.get_stats(),
            "conversation": [
                {
                    "timestamp": conv["timestamp"].isoformat(),
                    "user": conv["user"],
                    "assistant": conv["assistant"],
                    "model": conv["model"],
                    "cost": conv["cost"]
                }
                for conv in self.conversation_history
            ],
            "total_cost": self.cost_tracker["total"]
        }
        
        with open(filename, "w") as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📁 Conversation exported to {filename}")


# ==================
# Challenge Functions
# ==================

def challenge_basic():
    """Basic Challenge: Get it working with one provider"""
    print("\n" + "="*60)
    print("BASIC CHALLENGE: Single Provider")
    print("="*60)
    
    hub = AssistantHub()
    
    if not hub.available_providers:
        print("❌ No API keys configured. Please set environment variables.")
        return
    
    # Test basic functionality
    test_prompts = [
        "What is Python?",
        "Explain recursion briefly",
        "What is Python?",  # Test cache
    ]
    
    for prompt in test_prompts:
        print(f"\n📝 User: {prompt}")
        response = hub.chat(prompt)
        print(f"🤖 Assistant: {response[:100]}...")
    
    # Check stats
    print("\n📊 Statistics:")
    stats = hub.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")


def challenge_intermediate():
    """Intermediate Challenge: Multi-provider with failover"""
    print("\n" + "="*60)
    print("INTERMEDIATE CHALLENGE: Multi-Provider with Caching")
    print("="*60)
    
    hub = AssistantHub()
    
    if len(hub.available_providers) < 2:
        print("⚠️ This challenge requires at least 2 API providers configured.")
        print("  Currently available:", hub.available_providers)
    
    # Test different complexity prompts
    test_prompts = [
        ("Hello!", "simple"),
        ("Explain machine learning", "medium"),
        ("Write a Python sorting algorithm", "complex"),
        ("Hello!", "simple"),  # Test cache
    ]
    
    for prompt, complexity in test_prompts:
        print(f"\n📝 User: {prompt} [{complexity}]")
        response = hub.chat(prompt)
        print(f"🤖 Response: {response[:100]}...")
    
    # Export conversation
    hub.export_conversation("intermediate_challenge.json")
    
    # Show final stats
    print("\n📊 Final Statistics:")
    stats = hub.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")


def challenge_advanced():
    """Advanced Challenge: Complete implementation"""
    print("\n" + "="*60)
    print("ADVANCED CHALLENGE: Full Feature Implementation")
    print("="*60)
    
    hub = AssistantHub()
    
    # Simulate a full conversation
    prompts = [
        "Hello!",  # Simple - should use cheap model
        "Explain quantum computing",  # Medium
        "Write Python code for binary search",  # Complex
        "What did I ask about first?",  # Tests memory
        "Hello!",  # Test cache again
        "Summarize our conversation",  # Tests context
    ]
    
    total_start_cost = hub.cost_tracker["total"]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'='*40}")
        print(f"Message {i}/{len(prompts)}")
        print(f"User: {prompt}")
        
        response = hub.chat(prompt)
        print(f"Assistant: {response[:150]}...")
        
        # Show incremental cost
        current_cost = hub.cost_tracker["total"]
        print(f"Total cost so far: ${current_cost:.4f}")
    
    # Final report
    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60)
    
    hub.export_conversation("advanced_challenge.json")
    
    final_stats = hub.get_stats()
    for key, value in final_stats.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")


def interactive_mode():
    """Interactive chat mode"""
    print("\n" + "="*60)
    print("INTERACTIVE MODE")
    print("="*60)
    print("Commands: 'quit', 'stats', 'export'")
    print("-"*60)
    
    hub = AssistantHub()
    
    if not hub.available_providers:
        print("❌ No API keys configured.")
        return
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'stats':
            print("\n📊 Current Statistics:")
            for key, value in hub.get_stats().items():
                print(f"  {key}: {value}")
            continue
        elif user_input.lower() == 'export':
            hub.export_conversation("interactive_export.json")
            continue
        elif not user_input:
            continue
        
        response = hub.chat(user_input)
        print(f"🤖 Assistant: {response}")
    
    # Final export
    hub.export_conversation("interactive_session.json")
    print("\n👋 Goodbye! Session exported to interactive_session.json")


# =======================
# Main Entry Point
# =======================

if __name__ == "__main__":
    print("="*60)
    print("CHAPTER 7 CHALLENGE PROJECT")
    print("Multi-Provider AI Assistant Hub")
    print("="*60)
    
    print("\nChoose your challenge level:")
    print("1. Basic - Single provider implementation")
    print("2. Intermediate - Multi-provider with caching")
    print("3. Advanced - Complete feature implementation")
    print("4. Interactive - Chat mode")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        challenge_basic()
    elif choice == "2":
        challenge_intermediate()
    elif choice == "3":
        challenge_advanced()
    elif choice == "4":
        interactive_mode()
    else:
        print("Invalid choice. Running basic challenge...")
        challenge_basic()
