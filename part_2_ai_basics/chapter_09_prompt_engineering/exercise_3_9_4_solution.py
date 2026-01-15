# From: Zero to AI Agent, Chapter 9, Section 9.4
# File: exercise_3_9_4_solution.py

"""
Transform vague prompts using appropriate patterns
"""

# Original 1: "Tell me about databases"
# Issues: Too vague, no audience, no structure
# Patterns: Role + Simplifier + Output Format

optimized_1 = """
You are a database architect explaining to a junior developer 
who knows Python but has never used databases.

Explain databases with this structure:

WHAT: Database in one simple sentence

WHY: Problem databases solve that Python lists don't

TYPES: 3 main types with one-line descriptions:
1. Relational: [description]
2. NoSQL: [description]  
3. In-Memory: [description]

EXAMPLE: Real-world analogy

NEXT STEP: Most important thing to learn first
"""

# Original 2: "Fix my code"
# Issues: No code, no error, no context
# Patterns: Chain-of-Thought + Recipe Pattern

optimized_2 = """
Debug this Python function that should calculate average but returns 0:

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total + num  # Bug here
    return total / len(numbers)

Error: calculate_average([10, 20, 30]) returns 0

Debug step by step:
1. Identify the bug (line and issue)
2. Explain why this causes the error
3. Show corrected code
4. How to prevent this mistake
5. Test to verify the fix
"""

# Original 3: "Write something creative"
# Issues: No genre, format, length, audience
# Patterns: Persona + Constraint + Output Format

optimized_3 = """
You are a witty sci-fi writer like Douglas Adams.

Write a creative piece:
- Format: Amazon product review
- Product: Time machine
- Length: Exactly 100 words
- Tone: Humorous with genuine concerns

Structure:
TITLE: [Clever title]
RATING: [X of 5 stars]
REVIEW: [100-word review]
PROS: [2 unexpected benefits]
CONS: [2 hilarious drawbacks]
"""

# Original 4: "Explain AI"
# Issues: No audience, too broad, no focus
# Patterns: Role + Alternative Approaches + Constraint

optimized_4 = """
You are a tech journalist for general audience.

Explain AI in exactly 3 paragraphs:

Paragraph 1: What AI is (kitchen analogy)
Paragraph 2: What AI does today (3 daily examples)
Paragraph 3: What AI cannot do (2 limitations)

Constraints:
- No technical jargon
- Each paragraph exactly 3 sentences
- Include one surprising fact
"""

# Original 5: "Help me decide"
# Issues: No context, options, criteria
# Patterns: Alternative Approaches + Reflection + Output Format

optimized_5 = """
Help me decide: Python or JavaScript as first language?

Context: Beginner, wants web development, 2 hours daily

PYTHON:
- Learning curve: [1-10]
- Time to first project: [weeks]
- Web dev path: [description]
- Job prospects: [demand]

JAVASCRIPT:
- Learning curve: [1-10]
- Time to first project: [weeks]
- Web dev path: [description]
- Job prospects: [demand]

RECOMMENDATION: [choice]
REASONING: [3 bullets]
FIRST WEEK PLAN: [days 1-7]
SUCCESS METRIC: [how to measure progress]
"""

if __name__ == "__main__":
    print("Prompt Optimization Results:")
    print("✓ Specificity: Vague → Precise")
    print("✓ Structure: None → Clear format")
    print("✓ Context: Missing → Complete")
    print("✓ Output: Unpredictable → Controlled")
    print("✓ Usefulness: Low → High")