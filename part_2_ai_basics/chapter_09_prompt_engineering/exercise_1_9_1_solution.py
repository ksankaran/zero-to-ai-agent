# From: Zero to AI Agent, Chapter 9, Section 9.1
# File: exercise_1_9_1_solution.py

"""
Transform bad prompts into effective ones using the five components
"""

# Bad Prompt 1: "Help with Python"
bad_prompt_1 = "Help with Python"

# Analysis: Missing all components - no role, context, specific task, format, or constraints

good_prompt_1 = """You are a patient Python tutor for beginners.

Context: I'm learning Python as my first programming language and have been studying for 2 weeks.

Task: Explain the difference between lists and tuples in Python.

Format: Provide:
1. A simple one-sentence definition of each
2. One practical example of when to use each
3. The key difference that matters most for beginners

Constraints: 
- Use everyday analogies, no technical jargon
- Keep the entire explanation under 150 words
- Focus on practical usage, not theory"""

# Bad Prompt 2: "Fix my code"
bad_prompt_2 = "Fix my code"

# Analysis: No code provided, no context about the error, no specific problem identified

good_prompt_2 = """You are a helpful debugging assistant.

Context: I'm building a simple calculator in Python. The addition function works but the division function crashes when the second number is zero.

Task: Review this division function and fix the error handling.

Code:
def divide(a, b):
    return a / b

Format: Provide:
1. The specific problem (one sentence)
2. The fixed code with comments
3. One additional improvement suggestion

Constraints:
- Keep the solution simple (beginner-level)
- Add clear error messages for users
- Explain why the fix prevents crashes"""

# Bad Prompt 3: "Write something about databases"
bad_prompt_3 = "Write something about databases"

# Analysis: Completely open-ended - could be technical, historical, practical, theoretical, etc.

good_prompt_3 = """You are a technical writer creating content for junior developers.

Context: Writing for bootcamp graduates who know Python but have never worked with databases.

Task: Write an introduction to why web applications need databases.

Format: Create a 3-paragraph introduction:
1. The problem databases solve (what happens without them?)
2. Real-world analogy comparing databases to something familiar
3. Three specific things databases enable in modern apps

Constraints:
- No SQL or technical terms yet
- Use examples from popular apps (Instagram, Amazon, etc.)
- Keep it under 200 words total
- Encouraging tone that builds confidence"""

def test_prompts():
    """Compare the prompts to see the difference"""
    
    print("PROMPT TRANSFORMATION EXAMPLES")
    print("=" * 50)
    
    prompts = [
        ("Help with Python", good_prompt_1),
        ("Fix my code", good_prompt_2),
        ("Write something about databases", good_prompt_3)
    ]
    
    for bad, good in prompts:
        print(f"\n❌ BAD: '{bad}'")
        print(f"   Missing: role, context, task, format, constraints")
        print(f"\n✅ GOOD: Includes all five components")
        print(f"   First line: {good.split('.')[0]}...")
        print("-" * 50)

if __name__ == "__main__":
    test_prompts()