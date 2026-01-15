# From: Zero to AI Agent, Chapter 9, Section 9.1
# File: exercise_3_9_1_solution.py

"""
Diagnose and fix problematic prompts
"""

def debug_prompt(bad_prompt, problem, diagnosis):
    """Analyze and fix a problematic prompt"""
    
    print(f"\n❌ BAD PROMPT: '{bad_prompt}'")
    print(f"   Problem: {problem}")
    print(f"   Diagnosis: {diagnosis}")
    print(f"✅ FIXED PROMPT:")
    print("-" * 40)

# Problem 1: "Explain AI" returns 10-page essay
debug_prompt(
    bad_prompt="Explain AI",
    problem="Returns 10-page essay",
    diagnosis="No constraints on length, audience, or focus"
)

fixed_1 = """Explain artificial intelligence to someone who has never studied computer science.
Use a real-world analogy and keep your explanation under 100 words.
Focus only on what AI does, not how it works technically."""

print(fixed_1)

# Problem 2: "Make this better: 'Hello world'" returns confused rambling
debug_prompt(
    bad_prompt="Make this better: 'Hello world'",
    problem="Confused rambling response",
    diagnosis="No context about what 'better' means or what the text is for"
)

fixed_2 = """Improve this Python print statement to be more welcoming for a beginner's first program:
Current: print('Hello world')

Make it:
1. More encouraging
2. Include the user's name (use input())
3. Add a welcome message
Show the improved code with comments."""

print(fixed_2)

# Problem 3: "Write code" returns random algorithm
debug_prompt(
    bad_prompt="Write code",
    problem="Returns random algorithm",
    diagnosis="No language, purpose, or requirements specified"
)

fixed_3 = """Write a Python function that validates email addresses.

Requirements:
- Check for @ symbol
- Check for domain extension (.com, .org, etc.)
- Return True if valid, False otherwise
- Include 3 test examples
Keep it simple - use only string methods, no regex."""

print(fixed_3)

# Problem 4: "Help with my project" returns generic advice
debug_prompt(
    bad_prompt="Help with my project",
    problem="Generic advice",
    diagnosis="No information about the project, the problem, or what help is needed"
)

fixed_4 = """I'm building a Todo list app in Python using Flask. I can create and display todos, 
but I need help implementing the delete functionality.

Current setup: Todos are stored in a list of dictionaries.
Problem: Not sure how to identify which todo to delete when user clicks delete button.

Please suggest:
1. How to uniquely identify each todo
2. How to handle the delete request in Flask
3. Simple code example"""

print(fixed_4)

# Problem 5: "Summarize this" without providing content
debug_prompt(
    bad_prompt="Summarize this",
    problem="Error - no content to summarize",
    diagnosis="Missing the actual content to be summarized"
)

fixed_5 = """Summarize this article about Python frameworks in 3 bullet points:

'Python offers several web frameworks for different needs. Flask is a lightweight framework 
perfect for small applications and learning. It gives developers flexibility but requires 
more setup. Django is a full-featured framework with everything built-in, ideal for large 
applications but with a steeper learning curve. FastAPI is modern and fast, designed for 
building APIs with automatic documentation. Each framework has its place: Flask for simplicity, 
Django for completeness, and FastAPI for modern API development.'"""

print(fixed_5)

def analyze_improvements():
    """Summary of what makes prompts better"""
    
    print("\n" + "=" * 50)
    print("KEY IMPROVEMENTS ACROSS ALL FIXES:")
    print("=" * 50)
    
    improvements = [
        "Added specific context about the situation",
        "Defined clear, measurable outcomes",
        "Set appropriate constraints (length, complexity, format)",
        "Specified the target audience or use case",
        "Provided necessary input data or examples",
        "Eliminated ambiguity in instructions"
    ]
    
    for i, improvement in enumerate(improvements, 1):
        print(f"{i}. {improvement}")

if __name__ == "__main__":
    analyze_improvements()