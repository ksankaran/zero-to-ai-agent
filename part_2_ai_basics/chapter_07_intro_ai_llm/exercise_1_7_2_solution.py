# From: Zero to AI Agent, Chapter 7, Section 7.2
# File: exercise_1_7_2_solution.py

"""
Exercise 1 Solution: Token Estimation
Understanding token counting for different types of text.
"""

import math


def estimate_tokens(text: str, method: str = "average") -> int:
    """
    Estimate token count for text using different methods.
    
    Args:
        text: Text to estimate tokens for
        method: Estimation method ('chars', 'words', or 'average')
    
    Returns:
        Estimated token count
    """
    if method == "chars":
        # Method 1: ~4 characters per token
        return math.ceil(len(text) / 4)
    elif method == "words":
        # Method 2: ~3/4 words per token (or 4/3 tokens per word)
        word_count = len(text.split())
        return math.ceil(word_count * 4 / 3)
    else:  # average
        # Use average of both methods for better accuracy
        char_estimate = len(text) / 4
        word_estimate = len(text.split()) * 4 / 3
        return math.ceil((char_estimate + word_estimate) / 2)


def analyze_tokenization_examples():
    """Analyze token counts for various text examples."""
    
    examples = [
        ("Hello, world!", "Simple greeting"),
        ("The quick brown fox jumps over the lazy dog.", "Pangram"),
        ("def calculate_sum(a, b): return a + b", "Python function"),
        ("https://www.example.com/path/to/page", "URL"),
        ("user@example.com", "Email address"),
        ("The year 2024 marks an important milestone.", "Text with numbers"),
        ("🎉 Emojis are fun! 🚀", "Text with emojis"),
        ("import numpy as np\nimport pandas as pd", "Python imports"),
    ]
    
    print("=" * 70)
    print("TOKEN ESTIMATION EXAMPLES")
    print("=" * 70)
    print()
    
    for text, description in examples:
        char_tokens = estimate_tokens(text, "chars")
        word_tokens = estimate_tokens(text, "words")
        avg_tokens = estimate_tokens(text, "average")
        
        print(f"Text: {text}")
        print(f"Description: {description}")
        print(f"Length: {len(text)} chars, {len(text.split())} words")
        print(f"Token estimates:")
        print(f"  By characters: ~{char_tokens} tokens")
        print(f"  By words: ~{word_tokens} tokens")
        print(f"  Average: ~{avg_tokens} tokens")
        print("-" * 50)
    
    # Exercise specific examples
    print("\n" + "=" * 70)
    print("EXERCISE 1 SOLUTIONS")
    print("=" * 70)
    
    exercise_texts = [
        ("Hello, world!", 3, 4),
        ("The quick brown fox jumps over the lazy dog.", 10, 11),
        (" ".join(["word"] * 200), 267, 270),  # 200-word email simulation
        ("def calculate_sum(a, b): return a + b", 12, 15),
    ]
    
    for text, min_expected, max_expected in exercise_texts:
        if len(text) > 50:
            display_text = f"{text[:47]}..."
        else:
            display_text = text
            
        estimated = estimate_tokens(text)
        
        print(f"\nText: '{display_text}'")
        print(f"Estimated tokens: {estimated}")
        print(f"Expected range: {min_expected}-{max_expected} tokens")
        
        if min_expected <= estimated <= max_expected:
            print("✅ Estimate within expected range!")
        else:
            print(f"⚠️ Estimate outside expected range")
    
    # Special case: Estimate for entire section
    section_words = 2800  # Approximate word count of section
    section_tokens = math.ceil(section_words * 4 / 3)
    print(f"\nEntire section (~{section_words} words): ~{section_tokens} tokens")


def demonstrate_tokenization_patterns():
    """Show common tokenization patterns."""
    
    print("\n" + "=" * 70)
    print("COMMON TOKENIZATION PATTERNS")
    print("=" * 70)
    
    patterns = {
        "Single words": [
            ("cat", 1),
            ("running", 1),
            ("extraordinary", 2),  # Longer uncommon words may split
        ],
        "Numbers": [
            ("42", 1),
            ("3.14159", 2),  # Decimals often split
            ("1,000,000", 3),  # Formatted numbers split more
        ],
        "Punctuation": [
            ("Hello!", 2),  # Word + punctuation
            ("Hi, there!", 4),  # Each punctuation typically separate
        ],
        "Code": [
            ("print()", 3),  # Function calls
            ("if x > 5:", 6),  # Conditionals
            ("list_comp = [x**2 for x in range(10)]", 15),  # Complex code
        ],
        "Special characters": [
            ("hello@world", 3),
            ("user_name", 2),
            ("kebab-case", 3),
        ]
    }
    
    for category, examples in patterns.items():
        print(f"\n{category}:")
        for text, typical_tokens in examples:
            estimated = estimate_tokens(text)
            print(f"  '{text}' → typically {typical_tokens} tokens (estimated: {estimated})")


def token_cost_calculator(token_count: int, model: str = "gpt-3.5-turbo") -> float:
    """
    Calculate API cost based on token count.
    
    Args:
        token_count: Number of tokens
        model: Model name for pricing
    
    Returns:
        Estimated cost in dollars
    """
    # Simplified pricing (as of 2024, check current prices)
    pricing = {
        "gpt-3.5-turbo": 0.002,  # $0.002 per 1K tokens
        "gpt-4": 0.06,  # $0.06 per 1K tokens
        "claude-3-haiku": 0.0015,  # $0.0015 per 1K tokens
    }
    
    price_per_1k = pricing.get(model, 0.002)
    cost = (token_count / 1000) * price_per_1k
    
    return cost


def main():
    """Run all token estimation demonstrations."""
    
    # Basic token analysis
    analyze_tokenization_examples()
    
    # Show patterns
    demonstrate_tokenization_patterns()
    
    # Cost calculation example
    print("\n" + "=" * 70)
    print("TOKEN COST EXAMPLES")
    print("=" * 70)
    
    conversation_tokens = 1000
    for model in ["gpt-3.5-turbo", "gpt-4", "claude-3-haiku"]:
        cost = token_cost_calculator(conversation_tokens, model)
        print(f"{model}: {conversation_tokens} tokens = ${cost:.4f}")
    
    # Practical tip
    print("\n💡 PRACTICAL TIPS:")
    print("• Use token counting to estimate costs BEFORE making API calls")
    print("• Different models may tokenize the same text differently")
    print("• Code and URLs often use more tokens than expected")
    print("• Consider token limits when designing prompts")
    print("• Reserve tokens for the response when calculating input limits")


if __name__ == "__main__":
    main()
