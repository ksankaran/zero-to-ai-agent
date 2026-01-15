# From: Zero to AI Agent, Chapter 9, Section 9.1
# File: exercise_2_9_1_solution.py

"""
Create three versions of the same prompt for different contexts
"""

base_code = """def calculate_price(amount, discount):
    return amount * (1 - discount)"""

# Context 1: Junior Developer Learning Exercise
learning_context_prompt = """You are a patient programming mentor teaching best practices.

Context: Reviewing code from a junior developer (3 months Python experience) who is learning 
through building projects. This is a practice exercise, not production code.

Review this function and provide educational feedback:
```python
def calculate_price(amount, discount):
    return amount * (1 - discount)
```

Focus on:
1. Explaining what the function does well
2. Suggesting one improvement for code clarity
3. Teaching one important concept related to this code
4. Encouraging continued learning

Keep feedback positive and constructive. Explain the 'why' behind any suggestions."""

# Context 2: Production E-commerce System  
production_context_prompt = """You are a senior engineer reviewing code for a production e-commerce system.

Context: This function processes millions of transactions daily for a payment platform. 
Security, accuracy, and error handling are critical. Any bug could cost real money.

Review this function for production deployment:
```python
def calculate_price(amount, discount):
    return amount * (1 - discount)
```

Identify:
1. Security vulnerabilities (input validation, type safety)
2. Edge cases that could cause failures
3. Missing error handling
4. Financial accuracy concerns (floating-point issues)
5. Required logging and monitoring

Be thorough - production code needs to handle every scenario."""

# Context 3: Code Competition (Optimization Focus)
competition_context_prompt = """You are a competitive programming expert reviewing code for performance.

Context: Code competition where execution speed and memory usage are scored. 
The function will be called millions of times with various inputs.

Review this function for competition optimization:
```python
def calculate_price(amount, discount):
    return amount * (1 - discount)
```

Analyze:
1. Time complexity and potential optimizations
2. Memory usage improvements
3. Mathematical optimizations
4. Edge cases that could slow execution
5. Alternative approaches for better performance

Focus purely on speed and efficiency, readability is secondary."""

def demonstrate_context_importance():
    """Show how context completely changes the review focus"""
    
    print("SAME CODE, THREE DIFFERENT CONTEXTS")
    print("=" * 50)
    print(f"Code being reviewed:\n{base_code}")
    print("=" * 50)
    
    contexts = [
        ("Learning Exercise", "Encouragement, teaching, basic improvements"),
        ("Production System", "Security, error handling, financial accuracy"),
        ("Competition", "Speed, memory, mathematical optimization")
    ]
    
    for name, focus in contexts:
        print(f"\n📍 Context: {name}")
        print(f"   Review Focus: {focus}")
        print("-" * 40)

if __name__ == "__main__":
    demonstrate_context_importance()