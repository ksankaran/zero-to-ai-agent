# From: Zero to AI Agent, Chapter 7, Section 7.3
# File: exercise_1_7_3_solution.py

"""
Exercise 1 Solution: Trace the Flow
Understanding how LLMs process text from input to output.
"""

from typing import List, Dict, Tuple


def trace_prompt_flow(prompt: str = "The weather today is"):
    """
    Trace how an LLM processes a prompt through each stage.
    
    Args:
        prompt: The input prompt to trace
    """
    
    print("=" * 70)
    print("EXERCISE 1: TRACING LLM PROMPT FLOW")
    print("=" * 70)
    print(f"\nPrompt: '{prompt}'")
    print("=" * 70)
    
    # Step 1: Tokenization
    trace_tokenization(prompt)
    
    # Step 2: Pattern Recognition
    trace_pattern_activation(prompt)
    
    # Step 3: Likely Completions
    trace_completions(prompt)
    
    # Step 4: Missing Information
    trace_missing_info(prompt)
    
    # Step 5: Complete Flow Visualization
    visualize_complete_flow(prompt)


def trace_tokenization(prompt: str):
    """Trace the tokenization process."""
    
    print("\n📝 STEP 1: TOKENIZATION")
    print("-" * 50)
    
    # Simulated tokenization (actual varies by model)
    tokens = ["The", " weather", " today", " is"]
    token_ids = [464, 1969, 1651, 318]  # Example token IDs
    
    print("Text → Tokens → Numbers:")
    print(f"'{prompt}'")
    print("    ↓")
    print(f"Tokens: {tokens}")
    print("    ↓")
    print(f"Token IDs: {token_ids}")
    
    print("\n💡 Key Points:")
    print("• Each token represents a piece of text")
    print("• Common words are single tokens")
    print("• Spaces often included in tokens")
    print("• Model has ~50,000 possible tokens")
    
    # Show position encoding
    print("\n📍 Position Encoding Added:")
    for i, token in enumerate(tokens):
        print(f"  Position {i}: '{token}' + position_embedding[{i}]")


def trace_pattern_activation(prompt: str):
    """Trace which patterns might activate."""
    
    print("\n🧠 STEP 2: PATTERN ACTIVATION")
    print("-" * 50)
    
    patterns = {
        "Weather Discussion": {
            "strength": 0.95,
            "triggers": ["weather", "today"],
            "associations": ["sunny", "cloudy", "rainy", "temperature", "forecast"]
        },
        "Time Reference": {
            "strength": 0.7,
            "triggers": ["today"],
            "associations": ["current", "now", "this morning", "this afternoon"]
        },
        "Incomplete Sentence": {
            "strength": 0.9,
            "triggers": ["is" + "incomplete"],
            "associations": ["continuation needed", "descriptive phrase expected"]
        },
        "News/Report Style": {
            "strength": 0.6,
            "triggers": ["The", "weather"],
            "associations": ["formal tone", "informative", "descriptive"]
        }
    }
    
    print("Patterns Recognized (via Attention Mechanism):")
    
    for pattern_name, pattern_info in patterns.items():
        print(f"\n🎯 {pattern_name}")
        print(f"   Activation Strength: {pattern_info['strength']:.1%}")
        print(f"   Triggered by: {', '.join(pattern_info['triggers'])}")
        print(f"   Associates with: {', '.join(pattern_info['associations'][:3])}...")
    
    print("\n💡 Attention Scores (simplified):")
    attention_matrix = [
        ["The", "weather", "today", "is"],
        [0.1, 0.3, 0.2, 0.1],  # "The" attends to...
        [0.2, 0.8, 0.4, 0.3],  # "weather" attends to...
        [0.1, 0.5, 0.7, 0.2],  # "today" attends to...
        [0.3, 0.6, 0.5, 0.9],  # "is" attends to...
    ]
    
    print("\nWord relationships (attention weights):")
    for i, word in enumerate(attention_matrix[0]):
        print(f"  '{word}' strongly attends to:", end=" ")
        weights = [attention_matrix[j+1][i] for j in range(4)]
        max_idx = weights.index(max(weights))
        print(f"'{attention_matrix[0][max_idx]}'")


def trace_completions(prompt: str):
    """Trace likely completions and their probabilities."""
    
    print("\n🎲 STEP 3: LIKELY COMPLETIONS")
    print("-" * 50)
    
    # Simulated next token probabilities
    completions = [
        ("sunny", 0.15, "Common weather descriptor"),
        ("cloudy", 0.12, "Common weather descriptor"),
        ("beautiful", 0.10, "Positive descriptor"),
        ("rainy", 0.08, "Weather condition"),
        ("cold", 0.07, "Temperature descriptor"),
        ("perfect", 0.06, "Positive descriptor"),
        ("expected", 0.05, "Forecast language"),
        ("unpredictable", 0.04, "Weather characteristic"),
        ("[other]", 0.33, "Long tail of possibilities")
    ]
    
    print("Next Token Probability Distribution:")
    print("(After softmax transformation)")
    
    for token, prob, category in completions[:8]:
        bar_length = int(prob * 100)
        bar = "█" * bar_length
        print(f"  {token:15} {prob:5.1%} {bar:20} ({category})")
    
    print(f"\n🎰 Sampling Process (at temperature=0.7):")
    print("1. Apply temperature scaling to logits")
    print("2. Convert to probabilities via softmax")
    print("3. Sample from distribution")
    print("4. Selected: 'sunny' (example)")
    
    # Show how temperature affects distribution
    print("\n🌡️ Temperature Effects:")
    temps = [
        (0.0, "Deterministic: Always pick 'sunny' (highest prob)"),
        (0.5, "Conservative: Mostly 'sunny' or 'cloudy'"),
        (1.0, "Balanced: Natural probability distribution"),
        (1.5, "Creative: More uniform, unexpected choices possible")
    ]
    
    for temp, desc in temps:
        print(f"  T={temp}: {desc}")


def trace_missing_info(prompt: str):
    """Identify missing information the LLM doesn't have."""
    
    print("\n❓ STEP 4: MISSING INFORMATION ANALYSIS")
    print("-" * 50)
    
    missing = [
        {
            "info": "Actual Current Date",
            "impact": "Cannot know what 'today' refers to",
            "llm_behavior": "Will complete generically or assume"
        },
        {
            "info": "Geographic Location",
            "impact": "No specific location for weather",
            "llm_behavior": "May describe generic/typical weather"
        },
        {
            "info": "Real-time Weather Data",
            "impact": "No access to actual weather conditions",
            "llm_behavior": "Will generate plausible but fictional weather"
        },
        {
            "info": "User's Intent",
            "impact": "Unclear if asking or stating",
            "llm_behavior": "Will assume most likely continuation"
        },
        {
            "info": "Desired Format",
            "impact": "Formal report? Casual chat?",
            "llm_behavior": "Will use most common style from training"
        }
    ]
    
    print("Information the LLM DOESN'T Have:")
    
    for item in missing:
        print(f"\n❌ {item['info']}")
        print(f"   Impact: {item['impact']}")
        print(f"   LLM Behavior: {item['llm_behavior']}")
    
    print("\n⚠️ Result: LLM will generate statistically plausible")
    print("         but not factually accurate weather description")


def visualize_complete_flow(prompt: str):
    """Visualize the complete processing flow."""
    
    print("\n🔄 COMPLETE PROCESSING FLOW")
    print("=" * 70)
    
    flow = """
    "The weather today is"
           ↓
    [1] TOKENIZATION
    [The] [weather] [today] [is]
           ↓
    [2] EMBEDDING
    Vector representations in 768D space
           ↓
    [3] ATTENTION LAYERS (×12)
    Each token attends to others
    Patterns emerge: "weather report"
           ↓
    [4] PATTERN RECOGNITION
    - Weather description context ✓
    - Incomplete sentence ✓
    - Present tense ✓
           ↓
    [5] NEXT TOKEN PREDICTION
    Probability distribution over vocabulary
    Top choices: sunny(15%), cloudy(12%), beautiful(10%)
           ↓
    [6] SAMPLING (temperature=0.7)
    Selected: "sunny"
           ↓
    [7] APPEND & REPEAT
    "The weather today is sunny"
           ↓
    Continue until stop token or limit
           ↓
    [8] OUTPUT
    "The weather today is sunny and pleasant, 
     with temperatures reaching..."
    """
    
    print(flow)
    
    print("\n🎯 KEY INSIGHTS:")
    print("• LLM doesn't 'know' the weather - it predicts likely text")
    print("• Each step is mathematical transformation, not understanding")
    print("• Quality depends on training patterns, not real-time data")
    print("• Confident output ≠ factual accuracy")


def demonstrate_variations():
    """Show how slight changes affect the flow."""
    
    print("\n🔀 PROMPT VARIATIONS")
    print("=" * 70)
    
    variations = [
        ("The weather today is", "Generic completion expected"),
        ("The weather today in Tokyo is", "Location-specific patterns activate"),
        ("The weather forecast for today is", "Shifts to prediction language"),
        ("Today's weather is", "Less formal, same meaning"),
        ("The weather today will be", "Future tense changes predictions")
    ]
    
    print("How small changes affect processing:\n")
    
    for variant, effect in variations:
        print(f"📝 '{variant}'")
        print(f"   → {effect}")
    
    print("\n💡 Each variation activates slightly different patterns,")
    print("   leading to different completion probabilities!")


def main():
    """Run the complete tracing exercise."""
    
    # Main exercise
    trace_prompt_flow("The weather today is")
    
    # Show variations
    demonstrate_variations()
    
    # Summary
    print("\n" + "=" * 70)
    print("EXERCISE 1 COMPLETE")
    print("=" * 70)
    print("\n✅ You've traced a prompt through the entire LLM pipeline!")
    print("   From text → tokens → patterns → predictions → output")
    print("\n🎓 Remember: LLMs are sophisticated pattern matchers,")
    print("   not weather services or fact databases!")


if __name__ == "__main__":
    main()
