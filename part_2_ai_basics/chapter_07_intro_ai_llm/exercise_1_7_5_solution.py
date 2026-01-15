# From: Zero to AI Agent, Chapter 7, Section 7.5
# File: exercise_1_7_5_solution.py

"""
Exercise 1 Solution: Cost Calculator
Calculate monthly costs for different providers based on usage patterns.
"""

from typing import Dict, List
from dataclasses import dataclass
import json


@dataclass
class Provider:
    """LLM Provider configuration."""
    name: str
    models: Dict[str, Dict[str, float]]  # model -> {input_cost, output_cost}
    free_tier: Dict[str, int]  # model -> free tokens
    rate_limits: Dict[str, int]  # model -> requests per minute


def create_cost_calculator():
    """Create a comprehensive cost calculator for LLM providers."""
    
    print("=" * 70)
    print("EXERCISE 1: LLM COST CALCULATOR")
    print("=" * 70)
    
    # Define providers
    providers = setup_providers()
    
    # Define usage scenarios
    scenarios = define_usage_scenarios()
    
    # Calculate costs for each scenario
    for scenario in scenarios:
        print(f"\n📊 Scenario: {scenario['name']}")
        print(f"   Daily messages: {scenario['daily_messages']}")
        print(f"   Avg input tokens: {scenario['avg_input_tokens']}")
        print(f"   Avg output tokens: {scenario['avg_output_tokens']}")
        print("-" * 50)
        
        for provider in providers:
            monthly_cost = calculate_monthly_cost(
                provider,
                scenario['daily_messages'],
                scenario['avg_input_tokens'],
                scenario['avg_output_tokens'],
                scenario['model_preference']
            )
            
            print(f"\n   {provider.name}:")
            for model, cost in monthly_cost.items():
                if cost > 0:
                    print(f"      {model}: ${cost:.2f}/month")


def setup_providers() -> List[Provider]:
    """Setup provider configurations with current pricing."""
    
    return [
        Provider(
            name="OpenAI",
            models={
                "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},  # per 1K tokens
                "gpt-4": {"input": 0.03, "output": 0.06},
                "gpt-4-turbo": {"input": 0.01, "output": 0.03}
            },
            free_tier={"gpt-3.5-turbo": 0},
            rate_limits={"gpt-3.5-turbo": 90, "gpt-4": 40}
        ),
        Provider(
            name="Anthropic",
            models={
                "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
                "claude-3-sonnet": {"input": 0.003, "output": 0.015},
                "claude-3-opus": {"input": 0.015, "output": 0.075}
            },
            free_tier={},
            rate_limits={"claude-3-haiku": 50, "claude-3-sonnet": 40}
        ),
        Provider(
            name="Google",
            models={
                "gemini-pro": {"input": 0.000125, "output": 0.000375},
                "gemini-ultra": {"input": 0.007, "output": 0.021}
            },
            free_tier={"gemini-pro": 60},  # free requests per minute
            rate_limits={"gemini-pro": 60}
        )
    ]


def define_usage_scenarios() -> List[Dict]:
    """Define different chatbot usage scenarios."""
    
    return [
        {
            "name": "Small Startup (Customer Support)",
            "daily_messages": 100,
            "avg_input_tokens": 150,
            "avg_output_tokens": 200,
            "model_preference": "cheapest"
        },
        {
            "name": "Medium Business (Sales Assistant)",
            "daily_messages": 500,
            "avg_input_tokens": 200,
            "avg_output_tokens": 300,
            "model_preference": "balanced"
        },
        {
            "name": "Enterprise (Technical Support)",
            "daily_messages": 2000,
            "avg_input_tokens": 300,
            "avg_output_tokens": 500,
            "model_preference": "quality"
        },
        {
            "name": "AI Coding Assistant",
            "daily_messages": 50,
            "avg_input_tokens": 500,
            "avg_output_tokens": 800,
            "model_preference": "quality"
        },
        {
            "name": "Content Generation Platform",
            "daily_messages": 1000,
            "avg_input_tokens": 100,
            "avg_output_tokens": 1000,
            "model_preference": "balanced"
        }
    ]


def calculate_monthly_cost(provider: Provider, daily_messages: int,
                          avg_input: int, avg_output: int, 
                          preference: str) -> Dict[str, float]:
    """Calculate monthly costs for a provider."""
    
    monthly_messages = daily_messages * 30
    total_input_tokens = monthly_messages * avg_input
    total_output_tokens = monthly_messages * avg_output
    
    costs = {}
    
    for model, pricing in provider.models.items():
        # Skip expensive models for "cheapest" preference
        if preference == "cheapest" and ("gpt-4" in model or "opus" in model):
            continue
        
        # Skip cheap models for "quality" preference  
        if preference == "quality" and ("haiku" in model or "gpt-3.5" in model):
            continue
        
        # Calculate cost
        input_cost = (total_input_tokens / 1000) * pricing["input"]
        output_cost = (total_output_tokens / 1000) * pricing["output"]
        total_cost = input_cost + output_cost
        
        costs[model] = total_cost
    
    return costs


def create_detailed_calculator():
    """Create a detailed cost calculation class."""
    
    print("\n" + "=" * 70)
    print("DETAILED COST CALCULATOR IMPLEMENTATION")
    print("=" * 70)
    
    code = '''
class LLMCostCalculator:
    """Comprehensive LLM cost calculator with optimization suggestions."""
    
    def __init__(self):
        self.providers = self._load_provider_data()
        self.usage_history = []
    
    def calculate_cost(self, provider: str, model: str, 
                      input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a single request."""
        pricing = self.providers[provider]["models"][model]
        input_cost = (input_tokens / 1000) * pricing["input_per_1k"]
        output_cost = (output_tokens / 1000) * pricing["output_per_1k"]
        return input_cost + output_cost
    
    def estimate_monthly_budget(self, usage_pattern: Dict) -> Dict:
        """Estimate monthly budget across providers."""
        results = {}
        
        for provider in self.providers:
            provider_costs = {}
            
            for model in self.providers[provider]["models"]:
                daily_cost = 0
                
                for interaction in usage_pattern["daily_interactions"]:
                    cost = self.calculate_cost(
                        provider, model,
                        interaction["input_tokens"],
                        interaction["output_tokens"]
                    )
                    daily_cost += cost * interaction["frequency"]
                
                provider_costs[model] = {
                    "daily": daily_cost,
                    "monthly": daily_cost * 30,
                    "yearly": daily_cost * 365
                }
            
            results[provider] = provider_costs
        
        return results
    
    def optimize_costs(self, current_usage: Dict) -> List[Dict]:
        """Provide cost optimization recommendations."""
        recommendations = []
        
        # Analyze current spending
        current_cost = self.calculate_current_cost(current_usage)
        
        # Check for cheaper alternatives
        if current_usage["model"] == "gpt-4":
            gpt35_cost = self.calculate_with_model("gpt-3.5-turbo", current_usage)
            if gpt35_cost < current_cost * 0.5:
                recommendations.append({
                    "action": "Switch to GPT-3.5-Turbo for simple tasks",
                    "savings": f"${(current_cost - gpt35_cost):.2f}/month",
                    "impact": "Minimal for non-complex tasks"
                })
        
        # Check for batching opportunities
        if current_usage["requests_per_day"] > 100:
            recommendations.append({
                "action": "Batch similar requests together",
                "savings": "10-20% on token usage",
                "impact": "Slightly delayed responses"
            })
        
        # Check for caching opportunities
        if current_usage["unique_queries_ratio"] < 0.7:
            recommendations.append({
                "action": "Implement response caching",
                "savings": f"{(1 - current_usage['unique_queries_ratio']) * 100:.0f}%",
                "impact": "Instant responses for repeated queries"
            })
        
        return recommendations
    
    def compare_providers(self, usage_scenario: Dict) -> pd.DataFrame:
        """Create comparison table for providers."""
        comparison = []
        
        for provider in self.providers:
            for model in self.providers[provider]["models"]:
                row = {
                    "Provider": provider,
                    "Model": model,
                    "Monthly Cost": self.calculate_monthly(provider, model, usage_scenario),
                    "Rate Limit": self.providers[provider]["rate_limits"].get(model),
                    "Context Window": self.providers[provider]["context_windows"].get(model),
                    "Best For": self.providers[provider]["best_for"].get(model)
                }
                comparison.append(row)
        
        return pd.DataFrame(comparison).sort_values("Monthly Cost")

# Usage Example
calculator = LLMCostCalculator()

usage = {
    "daily_interactions": [
        {"type": "simple_query", "frequency": 50, "input_tokens": 100, "output_tokens": 150},
        {"type": "complex_analysis", "frequency": 10, "input_tokens": 500, "output_tokens": 800},
        {"type": "code_generation", "frequency": 5, "input_tokens": 300, "output_tokens": 600}
    ]
}

budget = calculator.estimate_monthly_budget(usage)
print(f"OpenAI GPT-3.5: ${budget['OpenAI']['gpt-3.5-turbo']['monthly']:.2f}/month")
print(f"Anthropic Claude-3-Haiku: ${budget['Anthropic']['claude-3-haiku']['monthly']:.2f}/month")

recommendations = calculator.optimize_costs(current_usage)
for rec in recommendations:
    print(f"💡 {rec['action']}: Save {rec['savings']}")
    '''
    
    print(code)


def show_cost_optimization_strategies():
    """Show various cost optimization strategies."""
    
    print("\n" + "=" * 70)
    print("COST OPTIMIZATION STRATEGIES")
    print("=" * 70)
    
    strategies = [
        {
            "strategy": "Model Downgrading",
            "description": "Use cheaper models when possible",
            "savings": "50-90%",
            "example": "GPT-4 → GPT-3.5-Turbo for simple tasks"
        },
        {
            "strategy": "Response Caching",
            "description": "Cache common queries",
            "savings": "20-40%",
            "example": "FAQ responses, repeated calculations"
        },
        {
            "strategy": "Prompt Optimization",
            "description": "Shorter, more efficient prompts",
            "savings": "10-30%",
            "example": "Remove unnecessary context, use abbreviations"
        },
        {
            "strategy": "Batch Processing",
            "description": "Combine multiple requests",
            "savings": "15-25%",
            "example": "Process 10 items in one call vs 10 calls"
        },
        {
            "strategy": "Hybrid Approach",
            "description": "Mix expensive and cheap models",
            "savings": "30-50%",
            "example": "GPT-3.5 filters, GPT-4 for complex only"
        }
    ]
    
    for s in strategies:
        print(f"\n💰 {s['strategy']}")
        print(f"   Description: {s['description']}")
        print(f"   Potential Savings: {s['savings']}")
        print(f"   Example: {s['example']}")


def main():
    """Run cost calculator exercise."""
    
    # Basic calculator
    create_cost_calculator()
    
    # Detailed implementation
    create_detailed_calculator()
    
    # Optimization strategies
    show_cost_optimization_strategies()
    
    print("\n" + "=" * 70)
    print("EXERCISE 1 COMPLETE")
    print("=" * 70)
    print("\n✅ You can now calculate and optimize LLM costs!")


if __name__ == "__main__":
    main()
