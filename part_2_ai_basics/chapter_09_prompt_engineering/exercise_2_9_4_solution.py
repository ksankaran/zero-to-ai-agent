# From: Zero to AI Agent, Chapter 9, Section 9.4
# File: exercise_2_9_4_solution.py

"""
Combine multiple patterns effectively
"""

# Combination 1: CoT + Role + Format for business problem
business_combo = """
You are a seasoned business analyst with 15 years retail experience.

A clothing store's revenue dropped 30% last quarter. 
Let's think through this step by step.

STEP 1: Data Gathering
What to examine: [key metrics]
Why it matters: [explanation]

STEP 2: Hypothesis Formation
• Hypothesis 1: [cause] - Evidence: [support]
• Hypothesis 2: [cause] - Evidence: [support]
• Hypothesis 3: [cause] - Evidence: [support]

STEP 3: Root Cause Analysis
Most likely cause: [conclusion]
Reasoning: [step-by-step logic]

STEP 4: Recommended Solution
PRIMARY ACTION: [one recommendation]
Supporting actions: [2-3 bullets]
Expected outcome: [measurable]
Timeline: [timeframe]

CONFIDENCE: [1-10] with explanation
"""

# Combination 2: Persona + Simplifier + Constraint for teaching
teaching_combo = """
You are Ms. Frizzle from Magic School Bus - enthusiastic and fun!

Explain how the internet works.

Level 1 - For 7-year-old (exactly 3 sentences):
[Use playground analogies only]

Level 2 - For 12-year-old (exactly 5 sentences):
[Can mention computers, keep it fun]

Level 3 - For 16-year-old (exactly 7 sentences):
[Basic technical terms OK, stay enthusiastic]

Stay in character - make it an adventure!
"""

# Combination 3: Alternative + Reflection + Format for decision
decision_combo = """
Help me choose a first programming language.

Context: Beginner, interested in web dev, 2 hours daily.

OPTION 1: Python
Strengths: [3 advantages for beginners]
Weaknesses: [2 limitations]
Success likelihood: [percentage]

OPTION 2: JavaScript
Strengths: [3 advantages for beginners]
Weaknesses: [2 limitations]
Success likelihood: [percentage]

OPTION 3: Scratch
Strengths: [3 advantages for beginners]
Weaknesses: [2 limitations]
Success likelihood: [percentage]

RECOMMENDATION: [choice with reason]

CRITICAL REFLECTION:
1. What assumptions am I making?
2. What could change this recommendation?
3. What did I potentially overlook?
4. Confidence: [1-10] because: [reason]
"""

if __name__ == "__main__":
    print("Pattern Combinations:")
    print("1. Business: CoT + Role + Format")
    print("   Synergy: Expertise + Analysis + Structure")
    print("2. Teaching: Persona + Simplifier + Constraint")
    print("   Synergy: Engagement + Accessibility + Focus")
    print("3. Decision: Alternative + Reflection + Format")
    print("   Synergy: Options + Depth + Comparability")