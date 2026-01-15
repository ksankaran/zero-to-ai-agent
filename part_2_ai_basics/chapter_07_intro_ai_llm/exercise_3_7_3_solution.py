# From: Zero to AI Agent, Chapter 7, Section 7.3
# File: exercise_3_7_3_solution.py

"""
Exercise 3 Solution: Understanding Failures
Why LLMs fail at certain tasks - explained through their mechanisms.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class FailureAnalysis:
    """Analysis of why an LLM fails at a specific task."""
    scenario: str
    root_cause: str
    mechanism_explanation: str
    observable_behavior: str
    mitigation: str


def analyze_llm_failures():
    """
    Analyze why LLMs fail at specific tasks based on their mechanisms.
    """
    
    print("=" * 70)
    print("EXERCISE 3: UNDERSTANDING LLM FAILURES")
    print("=" * 70)
    print("Why do LLMs fail? Let's trace each failure to its root cause.")
    print("=" * 70)
    
    failures = get_failure_analyses()
    
    for i, (scenario, analysis) in enumerate(failures.items(), 1):
        print(f"\n{i}. {analysis.scenario}")
        print("=" * 50)
        
        print(f"\n🔍 ROOT CAUSE:")
        print(f"   {analysis.root_cause}")
        
        print(f"\n⚙️ MECHANISM EXPLANATION:")
        for line in analysis.mechanism_explanation.split('\n'):
            print(f"   {line}")
        
        print(f"\n👁️ OBSERVABLE BEHAVIOR:")
        print(f"   {analysis.observable_behavior}")
        
        print(f"\n💡 MITIGATION:")
        print(f"   {analysis.mitigation}")
    
    # Show the common pattern
    show_common_failure_patterns()
    
    # Demonstrate with examples
    demonstrate_failure_examples()


def get_failure_analyses() -> Dict[str, FailureAnalysis]:
    """Get detailed analyses of each failure scenario."""
    
    return {
        "arithmetic": FailureAnalysis(
            scenario="Can't do exact arithmetic on large numbers",
            root_cause="LLMs learn statistical patterns, not mathematical operations",
            mechanism_explanation="""
LLMs see "123 × 456" as tokens, not numbers.
They predict likely text patterns from training.
No actual calculation happens - just pattern matching.
They've seen "2+2=4" millions of times, so they get it right.
They haven't seen "123,456 × 789,012" so they approximate.""",
            observable_behavior="Gets simple math right, fails on complex/unusual calculations",
            mitigation="Use tools/code for calculations, LLM for explaining the process"
        ),
        
        "citations": FailureAnalysis(
            scenario="Makes up fake citations",
            root_cause="Pattern completion without factual grounding",
            mechanism_explanation="""
LLMs learn the PATTERN of citations: (Author, Year, Journal).
When asked for citations, they generate plausible-looking ones.
No connection to real publications database.
They combine: real author names + likely years + journal names.
Result looks real but is statistically generated fiction.""",
            observable_behavior="Citations follow correct format but don't exist",
            mitigation="Always verify citations, use retrieval-augmented generation"
        ),
        
        "contradictions": FailureAnalysis(
            scenario="Contradicts itself in long conversations",
            root_cause="No persistent state or memory between tokens",
            mechanism_explanation="""
Each response is generated token-by-token.
No memory of what it 'decided' earlier.
Context window truncation loses old statements.
Statistical generation doesn't enforce logical consistency.
Different prompt contexts activate different patterns.""",
            observable_behavior="Says one thing early, opposite later, doesn't notice",
            mitigation="Track important claims, remind model of prior statements"
        ),
        
        "preferences": FailureAnalysis(
            scenario="Can't learn your preferences permanently",
            root_cause="No weight updates after training, stateless operation",
            mechanism_explanation="""
LLM weights are frozen after training.
Each conversation starts fresh - no memory.
Can't update internal parameters based on your feedback.
'Learning' only exists within current context window.
When context clears, all 'learning' is lost.""",
            observable_behavior="Forgets preferences between sessions, repeats same mistakes",
            mitigation="Store preferences externally, include in system prompt"
        ),
        
        "confident_errors": FailureAnalysis(
            scenario="Says factually wrong things confidently",
            root_cause="No truth mechanism - only pattern likelihood",
            mechanism_explanation="""
LLMs optimize for likely/plausible text, not truth.
Confidence is a linguistic pattern, not certainty measure.
"The capital of France is Paris" - pattern learned from data.
"The capital of [Made-up Country] is [Plausible City Name]" - same pattern.
No difference in mechanism between true and false statements.""",
            observable_behavior="States fiction with same confidence as facts",
            mitigation="Always fact-check important claims, especially specific details"
        )
    }


def show_common_failure_patterns():
    """Show common patterns across all failures."""
    
    print("\n" + "=" * 70)
    print("COMMON FAILURE PATTERNS")
    print("=" * 70)
    
    patterns = [
        {
            "pattern": "Pattern Without Understanding",
            "explanation": "LLMs match patterns without grasping meaning",
            "examples": ["Math notation", "Citation format", "Code syntax"]
        },
        {
            "pattern": "Statistical Plausibility ≠ Truth",
            "explanation": "Generates what's likely, not what's true",
            "examples": ["Fake citations", "Plausible but wrong facts", "Confident errors"]
        },
        {
            "pattern": "No Persistent State",
            "explanation": "Each generation starts fresh, no memory",
            "examples": ["Contradictions", "Forgotten context", "Lost preferences"]
        },
        {
            "pattern": "Context Window Limitations",
            "explanation": "Can only 'see' limited tokens at once",
            "examples": ["Long document issues", "Conversation drift", "Lost details"]
        },
        {
            "pattern": "Training Data Boundaries",
            "explanation": "Can't go beyond what was in training",
            "examples": ["Current events", "Personal information", "New developments"]
        }
    ]
    
    for pattern_info in patterns:
        print(f"\n🔍 {pattern_info['pattern']}")
        print(f"   {pattern_info['explanation']}")
        print(f"   Examples: {', '.join(pattern_info['examples'])}")


def demonstrate_failure_examples():
    """Demonstrate failures with concrete examples."""
    
    print("\n" + "=" * 70)
    print("CONCRETE FAILURE EXAMPLES")
    print("=" * 70)
    
    examples = [
        {
            "task": "Calculate 12,847 × 9,736",
            "llm_output": "125,234,872 (likely wrong)",
            "actual": "125,094,392",
            "why": "No computation, just pattern matching"
        },
        {
            "task": "Cite the seminal paper on transformer architecture",
            "llm_output": "Vaswani et al., 2017 ✓ (happens to be right)",
            "actual": "'Attention is All You Need', Vaswani et al., 2017",
            "why": "This one is memorized, but could easily make up others"
        },
        {
            "task": "What's the weather in Tokyo?",
            "llm_output": "It's sunny and 22°C (completely made up)",
            "actual": "No way to know without real-time data",
            "why": "Generates plausible weather, not actual weather"
        },
        {
            "task": "Remember I prefer Python over Java",
            "llm_output": "I'll remember that! (no, it won't)",
            "actual": "Forgotten by next conversation",
            "why": "No weight updates, no persistent memory"
        }
    ]
    
    for ex in examples:
        print(f"\n📝 Task: {ex['task']}")
        print(f"   LLM Output: {ex['llm_output']}")
        print(f"   Reality: {ex['actual']}")
        print(f"   ❓ Why: {ex['why']}")


def create_diagnostic_tests():
    """Create tests to identify LLM limitations."""
    
    print("\n" + "=" * 70)
    print("DIAGNOSTIC TESTS FOR LLM LIMITATIONS")
    print("=" * 70)
    
    tests = [
        {
            "name": "Arithmetic Test",
            "prompt": "What is 48,293 × 7,456?",
            "expected_behavior": "Wrong answer or refusal",
            "reveals": "Lack of computation ability"
        },
        {
            "name": "Citation Test",
            "prompt": "Cite 3 papers about unicorn biology from Nature journal",
            "expected_behavior": "Generates fake citations",
            "reveals": "Pattern generation without factual grounding"
        },
        {
            "name": "Consistency Test",
            "prompt": "Part 1: Is X better than Y?\nPart 2 (later): Compare Y to X",
            "expected_behavior": "May contradict earlier stance",
            "reveals": "No persistent beliefs or memory"
        },
        {
            "name": "Current Events Test",
            "prompt": "What happened in the news yesterday?",
            "expected_behavior": "Generic or outdated response",
            "reveals": "No real-time information access"
        },
        {
            "name": "Self-Knowledge Test",
            "prompt": "What did we discuss 10 messages ago?",
            "expected_behavior": "Accurate if in context, lost if outside window",
            "reveals": "Context window limitations"
        }
    ]
    
    print("\nTests to Reveal LLM Limitations:\n")
    
    for test in tests:
        print(f"🧪 {test['name']}")
        print(f"   Prompt: '{test['prompt']}'")
        print(f"   Expected: {test['expected_behavior']}")
        print(f"   Reveals: {test['reveals']}")
        print()


def explain_implications():
    """Explain practical implications of these failures."""
    
    print("=" * 70)
    print("PRACTICAL IMPLICATIONS")
    print("=" * 70)
    
    implications = [
        ("Never use LLMs for:", [
            "Critical calculations without verification",
            "Source of truth for facts without checking",
            "Medical/legal advice without professional review",
            "Real-time information needs",
            "Maintaining long-term user state"
        ]),
        
        ("Always verify:", [
            "Mathematical results",
            "Citations and references",
            "Specific facts and figures",
            "Technical specifications",
            "Current information"
        ]),
        
        ("Design around limitations:", [
            "Use tools for computation",
            "Implement external memory systems",
            "Fact-check important claims",
            "Keep context windows managed",
            "Store user preferences separately"
        ]),
        
        ("LLMs excel at:", [
            "Pattern-based text generation",
            "Style and tone matching",
            "Creative ideation",
            "Language transformation",
            "Explaining concepts (verify accuracy)"
        ])
    ]
    
    for category, items in implications:
        print(f"\n{category}")
        for item in items:
            print(f"  • {item}")


def main():
    """Run failure analysis exercise."""
    
    # Analyze failures
    analyze_llm_failures()
    
    # Create diagnostic tests
    create_diagnostic_tests()
    
    # Explain implications
    explain_implications()
    
    print("\n" + "=" * 70)
    print("EXERCISE 3 COMPLETE")
    print("=" * 70)
    print("\n✅ You now understand WHY LLMs fail at specific tasks")
    print("   and can design around these limitations!")
    print("\n🎓 Remember: These aren't bugs, they're fundamental")
    print("   consequences of how LLMs work - pattern matching, not reasoning!")


if __name__ == "__main__":
    main()
