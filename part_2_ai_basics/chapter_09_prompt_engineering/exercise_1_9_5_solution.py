# From: Zero to AI Agent, Chapter 9, Section 9.5
# File: exercise_1_9_5_solution.py

"""
Iterate a terrible prompt to excellence
"""

# Starting prompt: "Make this better"
# This is about as vague as it gets!

iteration_log = []

# Iteration 1: Add basic context
iteration_1 = {
    "version": "v1",
    "prompt": "Make this better",
    "test_results": {
        "email": "No idea what to improve - 2/10",
        "code": "No context about language or issue - 1/10",  
        "essay": "Better how? Grammar? Content? - 2/10"
    },
    "average_score": 1.7,
    "learned": "Completely ambiguous - AI has no idea what 'this' is or what 'better' means"
}

# Iteration 2: Specify what we're improving
iteration_2 = {
    "version": "v2",
    "prompt": "Improve this text",
    "test_results": {
        "email": "Still unclear what kind of improvement - 4/10",
        "code": "Treats code as text, tries to fix grammar - 3/10",
        "essay": "Makes random improvements - 4/10"
    },
    "average_score": 3.7,
    "learned": "Need to specify the type of content and improvement desired"
}

# Iteration 3: Add content type and improvement type
iteration_3 = {
    "version": "v3", 
    "prompt": "Improve the clarity and professionalism of this business email",
    "test_results": {
        "email": "Much better! Knows the context - 7/10",
        "code": "N/A - prompt now email-specific",
        "essay": "N/A - prompt now email-specific"
    },
    "average_score": 7.0,
    "learned": "Specificity dramatically improves results, but need format guidance"
}

# Iteration 4: Add structure and constraints
iteration_4 = {
    "version": "v4",
    "prompt": """Improve this business email for clarity and professionalism.

Requirements:
- Keep the main message intact
- Maintain friendly but professional tone  
- Keep length within 20% of original
- Fix any grammar or spelling errors""",
    "test_results": {
        "email_casual": "Perfect balance of friendly and professional - 8.5/10",
        "email_angry": "Diplomatically rewritten, great - 9/10",
        "email_confused": "Clarified beautifully - 8.5/10"
    },
    "average_score": 8.7,
    "learned": "Constraints help maintain intent while improving quality"
}

# Iteration 5: Add role and format for consistency
iteration_5_final = {
    "version": "v5",
    "prompt": """You are a professional business communication expert.

Improve this business email for clarity and professionalism.

Requirements:
- Preserve the core message and intent
- Use professional but approachable tone
- Keep length within 20% of original
- Correct grammar, spelling, and punctuation
- Maintain any specific requests or action items

Provide:
1. The improved email
2. Brief note on key changes made (2-3 bullets)""",
    "test_results": {
        "email_casual": "Excellent transformation with helpful notes - 9.5/10",
        "email_angry": "Professionally redirected, changes explained - 9.5/10",
        "email_confused": "Crystal clear, great explanation - 9.5/10"
    },
    "average_score": 9.5,
    "learned": "Role + requirements + output format = consistent excellence"
}

# Display iteration journey
if __name__ == "__main__":
    print("PROMPT ITERATION JOURNEY")
    print("="*50)
    print(f"Starting prompt: 'Make this better'")
    print(f"Starting score: 1.7/10")
    print(f"\nFinal prompt: [Comprehensive business email improver]")
    print(f"Final score: 9.5/10")
    print(f"\nImprovement: {9.5 - 1.7:.1f} points (458% increase)")
    
    print("\n\nKEY LEARNINGS:")
    print("1. Vague instructions produce vague results")
    print("2. Specifying content type focuses the task")  
    print("3. Clear requirements prevent unwanted changes")
    print("4. Role setting improves consistency")
    print("5. Structured output format ensures completeness")