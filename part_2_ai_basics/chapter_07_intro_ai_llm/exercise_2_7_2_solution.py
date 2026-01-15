# From: Zero to AI Agent, Chapter 7, Section 7.2
# File: exercise_2_7_2_solution.py

"""
Exercise 2 Solution: Choosing the Right Parameters
Understanding when to use different temperature settings for various tasks.
"""

from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class ParameterProfile:
    """Profile for LLM parameters for different use cases."""
    temperature: Tuple[float, float]  # (min, max) range
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    reasoning: str


def get_parameter_profiles() -> Dict[str, ParameterProfile]:
    """
    Get recommended parameter profiles for different scenarios.
    
    Returns:
        Dictionary of scenario -> ParameterProfile
    """
    
    profiles = {
        "legal_contract": ParameterProfile(
            temperature=(0.0, 0.2),
            max_tokens=2000,
            top_p=0.1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            reasoning=(
                "Legal language requires precision and consistency. "
                "Low temperature ensures deterministic, formal output. "
                "Low top_p further restricts to most likely (standard) phrases."
            )
        ),
        
        "creative_story": ParameterProfile(
            temperature=(0.9, 1.2),
            max_tokens=1500,
            top_p=0.95,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            reasoning=(
                "Creative writing benefits from high randomness. "
                "High temperature enables unexpected word choices. "
                "Penalties reduce repetition and encourage variety."
            )
        ),
        
        "technical_translation": ParameterProfile(
            temperature=(0.1, 0.3),
            max_tokens=3000,
            top_p=0.3,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            reasoning=(
                "Technical translation needs accuracy over creativity. "
                "Low temperature maintains terminology consistency. "
                "No penalties to allow technical term repetition."
            )
        ),
        
        "product_descriptions": ParameterProfile(
            temperature=(0.7, 0.8),
            max_tokens=500,
            top_p=0.9,
            frequency_penalty=0.3,
            presence_penalty=0.2,
            reasoning=(
                "Product descriptions need variety but remain coherent. "
                "Moderate temperature balances creativity with clarity. "
                "Light penalties avoid repetitive phrases."
            )
        ),
        
        "code_generation": ParameterProfile(
            temperature=(0.0, 0.2),
            max_tokens=1000,
            top_p=0.1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            reasoning=(
                "Code must be syntactically correct and functional. "
                "Near-zero temperature ensures valid syntax. "
                "Low top_p sticks to common coding patterns."
            )
        ),
        
        "brainstorming": ParameterProfile(
            temperature=(0.8, 1.0),
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0.7,
            presence_penalty=0.7,
            reasoning=(
                "Brainstorming needs maximum diversity of ideas. "
                "High temperature encourages creative combinations. "
                "High penalties push for unique, varied suggestions."
            )
        ),
        
        "customer_service": ParameterProfile(
            temperature=(0.3, 0.5),
            max_tokens=300,
            top_p=0.7,
            frequency_penalty=0.2,
            presence_penalty=0.1,
            reasoning=(
                "Customer service needs consistent, helpful tone. "
                "Low-moderate temperature keeps responses professional. "
                "Some variation prevents robotic feel."
            )
        ),
        
        "data_extraction": ParameterProfile(
            temperature=(0.0, 0.1),
            max_tokens=500,
            top_p=0.1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            reasoning=(
                "Data extraction requires maximum accuracy. "
                "Near-zero temperature prevents hallucination. "
                "Deterministic output for consistent parsing."
            )
        ),
        
        "educational_content": ParameterProfile(
            temperature=(0.4, 0.6),
            max_tokens=1500,
            top_p=0.8,
            frequency_penalty=0.2,
            presence_penalty=0.1,
            reasoning=(
                "Educational content needs clarity with engagement. "
                "Moderate temperature keeps explanations interesting. "
                "Light penalties maintain term consistency."
            )
        ),
        
        "poetry_generation": ParameterProfile(
            temperature=(0.9, 1.3),
            max_tokens=500,
            top_p=0.95,
            frequency_penalty=0.6,
            presence_penalty=0.8,
            reasoning=(
                "Poetry thrives on unexpected word combinations. "
                "High temperature enables creative expression. "
                "Strong penalties encourage unique imagery."
            )
        )
    }
    
    return profiles


def analyze_exercise_scenarios():
    """Analyze the specific scenarios from Exercise 2."""
    
    print("=" * 70)
    print("EXERCISE 2 SOLUTIONS: CHOOSING THE RIGHT PARAMETERS")
    print("=" * 70)
    
    exercise_scenarios = [
        ("A. Writing legal contract language", "legal_contract"),
        ("B. Generating creative story ideas", "creative_story"),
        ("C. Translating technical documentation", "technical_translation"),
        ("D. Writing varied product descriptions", "product_descriptions"),
        ("E. Solving coding problems", "code_generation"),
        ("F. Brainstorming business names", "brainstorming"),
    ]
    
    profiles = get_parameter_profiles()
    
    for scenario_name, profile_key in exercise_scenarios:
        profile = profiles[profile_key]
        
        print(f"\n{scenario_name}")
        print("-" * 50)
        print(f"🌡️ Temperature: {profile.temperature[0]:.1f} - {profile.temperature[1]:.1f}")
        print(f"📊 Reasoning: {profile.reasoning}")
        
        # Additional recommendations
        if profile.temperature[1] < 0.3:
            print("⚡ Type: DETERMINISTIC - Prioritizes accuracy and consistency")
        elif profile.temperature[1] < 0.7:
            print("⚖️ Type: BALANCED - Mix of consistency and variety")
        else:
            print("🎨 Type: CREATIVE - Prioritizes novelty and diversity")


def demonstrate_temperature_effects():
    """Show how temperature affects output."""
    
    print("\n" + "=" * 70)
    print("TEMPERATURE EFFECTS DEMONSTRATION")
    print("=" * 70)
    
    prompt = "Complete this sentence: The future of AI is"
    
    temperature_examples = [
        (0.0, [
            "The future of AI is bright and full of potential.",
            "The future of AI is bright and full of potential.",  # Same!
            "The future of AI is bright and full of potential.",  # Same!
        ]),
        (0.5, [
            "The future of AI is promising and transformative.",
            "The future of AI is full of exciting possibilities.",
            "The future of AI is both exciting and challenging.",
        ]),
        (1.0, [
            "The future of AI is like a kaleidoscope of possibilities.",
            "The future of AI is unwritten, waiting for bold innovators.",
            "The future of AI is a symphony yet to be composed.",
        ]),
        (1.5, [
            "The future of AI is pizza-shaped with quantum sprinkles.",
            "The future of AI is dancing on moonbeams of silicon dreams.",
            "The future of AI is yesterday's tomorrow singing backwards.",
        ])
    ]
    
    print(f"\nPrompt: '{prompt}'")
    
    for temp, outputs in temperature_examples:
        print(f"\n🌡️ Temperature: {temp}")
        print("Possible outputs:")
        for i, output in enumerate(outputs, 1):
            print(f"  {i}. {output}")
        
        if temp == 0.0:
            print("  Note: Deterministic - same output every time")
        elif temp < 0.5:
            print("  Note: Conservative - safe, predictable choices")
        elif temp < 1.0:
            print("  Note: Balanced - good variety while coherent")
        else:
            print("  Note: Wild - may produce nonsense")


def parameter_decision_tree():
    """Interactive parameter selection guide."""
    
    print("\n" + "=" * 70)
    print("PARAMETER SELECTION DECISION TREE")
    print("=" * 70)
    
    questions = [
        ("Does the output need to be factually accurate?", {
            "yes": ("temp", 0.0, 0.3),
            "no": ("next", 1)
        }),
        ("Is creativity more important than consistency?", {
            "yes": ("temp", 0.8, 1.2),
            "no": ("next", 2)
        }),
        ("Will users see multiple outputs (need variety)?", {
            "yes": ("temp", 0.5, 0.8),
            "no": ("temp", 0.2, 0.5)
        })
    ]
    
    print("\nQuick Temperature Selection Guide:")
    print("\n1. Does the output need to be factually accurate?")
    print("   YES → Use 0.0-0.3 (data extraction, translation, code)")
    print("   NO  → Continue to question 2")
    
    print("\n2. Is creativity more important than consistency?")
    print("   YES → Use 0.8-1.2 (stories, brainstorming, poetry)")
    print("   NO  → Continue to question 3")
    
    print("\n3. Will users see multiple outputs (need variety)?")
    print("   YES → Use 0.5-0.8 (product descriptions, content generation)")
    print("   NO  → Use 0.2-0.5 (customer service, explanations)")


def best_practices():
    """Show best practices for parameter selection."""
    
    print("\n" + "=" * 70)
    print("BEST PRACTICES FOR PARAMETER SELECTION")
    print("=" * 70)
    
    practices = [
        ("Start Conservative", 
         "Begin with lower temperature and increase if needed"),
        
        ("Test Systematically", 
         "Try 3-5 different temperatures with same prompt"),
        
        ("Consider Your Audience", 
         "B2B → lower temp, B2C → moderate temp, Creative → higher temp"),
        
        ("Use Temperature with Top-p", 
         "Temperature=0.8 + top_p=0.9 often better than temp=1.0 alone"),
        
        ("Adjust for Model Size", 
         "Larger models handle higher temperatures better"),
        
        ("Document Your Choices", 
         "Record which parameters work for which use cases"),
        
        ("Monitor Over Time", 
         "Model updates may require parameter adjustments"),
    ]
    
    for i, (practice, description) in enumerate(practices, 1):
        print(f"\n{i}. {practice}")
        print(f"   {description}")
    
    print("\n" + "=" * 70)
    print("💡 GOLDEN RULE: There's no perfect temperature!")
    print("   Test with your specific use case and adjust based on results.")
    print("=" * 70)


def main():
    """Run all parameter selection demonstrations."""
    
    # Exercise solutions
    analyze_exercise_scenarios()
    
    # Show temperature effects
    demonstrate_temperature_effects()
    
    # Decision guide
    parameter_decision_tree()
    
    # Best practices
    best_practices()


if __name__ == "__main__":
    main()
