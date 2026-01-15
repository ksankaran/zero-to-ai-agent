# From: Zero to AI Agent, Chapter 7, Section 7.7
# File: token_cost_calculator.py

"""
Understanding token costs and calculating API expenses.
Essential for building cost-effective AI applications.
"""

from typing import Dict, Optional
from datetime import datetime


def understand_token_pricing():
    """
    Tokens are the currency of LLMs - understand how they work
    """
    
    # Approximate token counts for common text
    examples = {
        "Hello": 1,  # 1 token
        "Hello, world!": 4,  # 4 tokens (Hello | , | world | !)
        "The quick brown fox": 4,  # Common words = 1 token each
        "Anthropomorphization": 3,  # Uncommon words split up
        "👍": 1,  # Emojis usually 1-2 tokens
        "import numpy as np": 5,  # Code tokens
        "def calculate_cost():": 6,  # Function definitions
        "https://example.com": 4,  # URLs split into parts
    }
    
    # Token estimation rules of thumb
    print("Token Estimation Rules:")
    print("• 1 token ≈ 4 characters in English")
    print("• 1 token ≈ ¾ words")
    print("• 100 tokens ≈ 75 words")
    print("• 1 page of text ≈ 500 tokens")
    print("• 1 conversation turn ≈ 50-200 tokens")
    print("\nExamples:")
    for text, tokens in examples.items():
        print(f"  '{text}' = ~{tokens} tokens")
    
    return examples


def calculate_cost(input_tokens: int, output_tokens: int, model: str = "gpt-3.5-turbo") -> Optional[Dict]:
    """
    Calculate actual costs for different models
    
    Args:
        input_tokens: Number of input/prompt tokens
        output_tokens: Number of output/completion tokens
        model: Model name
    
    Returns:
        Dictionary with cost breakdown or None if model not found
    """
    
    # Prices per 1K tokens (as of 2024 - check provider docs for current prices)
    pricing = {
        # OpenAI Models
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-4-32k": {"input": 0.06, "output": 0.12},
        
        # Anthropic Models
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-2.1": {"input": 0.008, "output": 0.024},
        
        # Google Models
        "gemini-pro": {"input": 0.000125, "output": 0.000375},
        "gemini-pro-vision": {"input": 0.000125, "output": 0.000375},
        
        # Other Models
        "llama-2-70b": {"input": 0.001, "output": 0.001},  # Via Replicate
        "mixtral-8x7b": {"input": 0.0005, "output": 0.0005},  # Via Replicate
    }
    
    if model not in pricing:
        print(f"Warning: Model '{model}' not in pricing database")
        return None
    
    # Calculate costs
    input_cost = (input_tokens / 1000) * pricing[model]["input"]
    output_cost = (output_tokens / 1000) * pricing[model]["output"]
    total_cost = input_cost + output_cost
    
    # Cost per 1K tokens (weighted average)
    total_tokens = input_tokens + output_tokens
    cost_per_1k = total_cost / (total_tokens / 1000) if total_tokens > 0 else 0
    
    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "cost_per_1k_tokens": cost_per_1k,
        "breakdown": f"${input_cost:.6f} (input) + ${output_cost:.6f} (output)"
    }


def estimate_tokens(text: str) -> int:
    """
    Estimate token count from text
    
    Args:
        text: Text to estimate
    
    Returns:
        Estimated token count
    """
    # Rule of thumb: 1 token ≈ 4 characters or ¾ words
    char_estimate = len(text) / 4
    word_estimate = len(text.split()) * 4 / 3
    
    # Use average of both methods
    return int((char_estimate + word_estimate) / 2)


def calculate_real_world_costs():
    """
    Calculate costs for real-world scenarios
    """
    
    scenarios = {
        "Customer Service Bot": {
            "daily_conversations": 100,
            "messages_per_conversation": 10,
            "avg_input_tokens": 50,
            "avg_output_tokens": 100,
            "model": "gpt-3.5-turbo"
        },
        "Code Assistant": {
            "daily_conversations": 50,
            "messages_per_conversation": 1,
            "avg_input_tokens": 200,  # Code context
            "avg_output_tokens": 300,  # Generated code
            "model": "gpt-4"
        },
        "Content Generator": {
            "daily_conversations": 10,
            "messages_per_conversation": 1,
            "avg_input_tokens": 100,  # Prompt
            "avg_output_tokens": 800,  # Article
            "model": "claude-3-sonnet"
        },
        "Study Assistant": {
            "daily_conversations": 20,
            "messages_per_conversation": 15,
            "avg_input_tokens": 75,
            "avg_output_tokens": 150,
            "model": "gemini-pro"
        }
    }
    
    print("="*60)
    print("REAL-WORLD COST SCENARIOS (Monthly Estimates)")
    print("="*60)
    
    for name, scenario in scenarios.items():
        # Calculate daily usage
        daily_messages = scenario["daily_conversations"] * scenario["messages_per_conversation"]
        daily_input_tokens = daily_messages * scenario["avg_input_tokens"]
        daily_output_tokens = daily_messages * scenario["avg_output_tokens"]
        
        # Calculate costs
        cost_data = calculate_cost(
            daily_input_tokens, 
            daily_output_tokens, 
            scenario["model"]
        )
        
        if cost_data:
            daily_cost = cost_data["total_cost"]
            monthly_cost = daily_cost * 30
            yearly_cost = monthly_cost * 12
            
            print(f"\n📊 {name}:")
            print(f"  Model: {scenario['model']}")
            print(f"  Usage: {daily_messages} messages/day")
            print(f"  Tokens: {daily_input_tokens + daily_output_tokens:,} tokens/day")
            print(f"  Daily: ${daily_cost:.2f}")
            print(f"  Monthly: ${monthly_cost:.2f}")
            print(f"  Yearly: ${yearly_cost:.2f}")
            
            # Cost breakdown
            if monthly_cost > 100:
                print(f"  ⚠️ High cost! Consider optimization strategies")
            elif monthly_cost < 10:
                print(f"  ✅ Very affordable for this use case")


def compare_model_costs(prompt: str, expected_response_length: int = 200):
    """
    Compare costs across different models for the same task
    
    Args:
        prompt: The input prompt
        expected_response_length: Expected response in tokens
    """
    
    input_tokens = estimate_tokens(prompt)
    output_tokens = expected_response_length
    
    models = [
        "gemini-pro",      # Cheapest
        "claude-3-haiku",  # Fast & cheap
        "gpt-3.5-turbo",   # Popular choice
        "claude-3-sonnet", # Good balance
        "gpt-4",          # High quality
        "claude-3-opus",   # Top tier
    ]
    
    print("\n" + "="*60)
    print("MODEL COST COMPARISON")
    print(f"Prompt: {len(prompt)} chars (~{input_tokens} tokens)")
    print(f"Expected response: ~{output_tokens} tokens")
    print("="*60)
    
    results = []
    
    for model in models:
        cost_data = calculate_cost(input_tokens, output_tokens, model)
        if cost_data:
            results.append((model, cost_data["total_cost"]))
            print(f"\n{model}:")
            print(f"  Cost per call: ${cost_data['total_cost']:.6f}")
            print(f"  1,000 calls: ${cost_data['total_cost'] * 1000:.2f}")
            print(f"  10,000 calls: ${cost_data['total_cost'] * 10000:.2f}")
    
    # Show cheapest vs most expensive
    if results:
        results.sort(key=lambda x: x[1])
        cheapest = results[0]
        most_expensive = results[-1]
        
        print("\n" + "-"*60)
        print(f"💰 Cheapest: {cheapest[0]} (${cheapest[1]:.6f}/call)")
        print(f"💎 Most expensive: {most_expensive[0]} (${most_expensive[1]:.6f}/call)")
        print(f"📊 Price difference: {most_expensive[1]/cheapest[1]:.1f}x more expensive")


if __name__ == "__main__":
    # Demonstrate token understanding
    print("Understanding Tokens")
    print("-" * 60)
    understand_token_pricing()
    
    # Calculate real-world costs
    print("\n")
    calculate_real_world_costs()
    
    # Compare models
    sample_prompt = "Explain the concept of recursion in programming with an example"
    compare_model_costs(sample_prompt, expected_response_length=300)
    
    # Example: Calculate specific cost
    print("\n" + "="*60)
    print("Specific Cost Example")
    print("="*60)
    
    result = calculate_cost(500, 1500, "gpt-3.5-turbo")
    if result:
        print(f"Model: {result['model']}")
        print(f"Total tokens: {result['total_tokens']}")
        print(f"Total cost: ${result['total_cost']:.4f}")
        print(f"Breakdown: {result['breakdown']}")
