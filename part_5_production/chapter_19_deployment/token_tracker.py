# From: Zero to AI Agent, Chapter 19, Section 19.6
# File: token_tracker.py
# Description: Track token usage and generate optimization insights

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TokenUsage:
    """Token usage for a single request."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float


class TokenTracker:
    """Track token usage and costs across requests."""
    
    # Cost per 1K tokens by model
    MODEL_COSTS = {
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    }
    
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.requests_by_model: Dict[str, Dict] = {}
    
    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost for a request."""
        costs = self.MODEL_COSTS.get(model, {"input": 0.01, "output": 0.03})
        input_cost = (prompt_tokens / 1000) * costs["input"]
        output_cost = (completion_tokens / 1000) * costs["output"]
        return input_cost + output_cost
    
    def record(self, model: str, prompt_tokens: int, completion_tokens: int) -> TokenUsage:
        """Record token usage from a request."""
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        
        if model not in self.requests_by_model:
            self.requests_by_model[model] = {
                "count": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "cost": 0.0
            }
        
        cost = self._calculate_cost(model, prompt_tokens, completion_tokens)
        
        self.requests_by_model[model]["count"] += 1
        self.requests_by_model[model]["prompt_tokens"] += prompt_tokens
        self.requests_by_model[model]["completion_tokens"] += completion_tokens
        self.requests_by_model[model]["cost"] += cost
        
        return TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            estimated_cost=cost
        )
    
    def get_report(self) -> dict:
        """Generate usage report."""
        total_cost = sum(m["cost"] for m in self.requests_by_model.values())
        
        return {
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens,
            "total_cost": round(total_cost, 4),
            "by_model": {
                model: {
                    **stats,
                    "cost": round(stats["cost"], 4)
                }
                for model, stats in self.requests_by_model.items()
            },
            "optimization_tips": self._get_tips()
        }
    
    def _get_tips(self) -> List[str]:
        """Generate optimization suggestions based on usage patterns."""
        tips = []
        
        # Check prompt/completion ratio
        if self.total_prompt_tokens > self.total_completion_tokens * 3:
            tips.append("High prompt-to-completion ratio. Consider shortening system prompts.")
        
        # Check for expensive model overuse
        for model, stats in self.requests_by_model.items():
            if "gpt-4" in model and "mini" not in model and stats["count"] > 100:
                tips.append(f"Heavy {model} usage ({stats['count']} requests). Consider routing simple queries to gpt-4o-mini.")
        
        # Check for long completions
        if self.total_completion_tokens > self.total_prompt_tokens:
            tips.append("Output tokens exceed input. Consider adding max_tokens limits.")
        
        # Check model diversity
        if len(self.requests_by_model) == 1 and list(self.requests_by_model.keys())[0] != "gpt-4o-mini":
            tips.append("Using only one model. Consider routing simple tasks to cheaper models.")
        
        if not tips:
            tips.append("Usage patterns look optimized! Keep monitoring for changes.")
        
        return tips


# Global tracker
tokens = TokenTracker()


# Example usage
if __name__ == "__main__":
    tracker = TokenTracker()
    
    # Simulate some requests
    tracker.record("gpt-4o-mini", prompt_tokens=100, completion_tokens=50)
    tracker.record("gpt-4o-mini", prompt_tokens=150, completion_tokens=80)
    tracker.record("gpt-4o", prompt_tokens=500, completion_tokens=200)
    tracker.record("gpt-4o", prompt_tokens=800, completion_tokens=300)
    tracker.record("gpt-4-turbo", prompt_tokens=1000, completion_tokens=500)
    
    import json
    print(json.dumps(tracker.get_report(), indent=2))
