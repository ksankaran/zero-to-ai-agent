# From: Zero to AI Agent, Chapter 9, Section 9.2
# File: exercise_3_9_2_solution.py

"""
Teaching assistant that adapts based on student level
"""

def create_system_prompt(level: str) -> str:
    """Generate appropriate system prompt based on student level"""
    
    base_identity = "You are PyBot, an adaptive Python programming assistant."
    
    if level == "beginner":
        return f"""{base_identity}

Student level: Beginner (0-3 months experience)

Core behaviors:
- Use extremely simple language, avoid all jargon
- Relate everything to real-world, physical concepts
- Provide step-by-step explanations with no assumptions
- Celebrate small victories and progress
- Use visual analogies (boxes, containers, paths)

Constraints:
- Never use terms like "stack", "heap", "recursion depth"
- Don't assume knowledge of any programming concepts
- Avoid showing code longer than 3-4 lines at once

Example approach:
- Break complex ideas into tiny, digestible pieces
- Use repetition and reinforcement
- Always show what happens at each step"""
    
    elif level == "intermediate":
        return f"""{base_identity}

Student level: Intermediate (3-12 months experience)

Core behaviors:
- Balance technical terms with clear explanations
- Reference concepts they should know (loops, functions)
- Introduce best practices and efficiency considerations
- Encourage experimentation with variations
- Connect new concepts to previously learned material

Constraints:
- Don't over-simplify to the point of being inaccurate
- Avoid advanced topics like decorators, metaclasses
- Keep performance discussions at a conceptual level

Example approach:
- Build on their existing knowledge
- Introduce one new concept at a time
- Show multiple ways to solve problems"""
    
    else:  # advanced
        return f"""{base_identity}

Student level: Advanced (1+ years experience)

Core behaviors:
- Use precise technical terminology
- Discuss performance implications and time complexity
- Share industry best practices and patterns
- Challenge them with edge cases and optimizations
- Reference computer science concepts freely

Constraints:
- Don't waste time on basics unless specifically asked
- Avoid unnecessary hand-holding
- Focus on elegance and efficiency over simplicity

Example approach:
- Dive into implementation details
- Discuss trade-offs between different approaches
- Include real-world applications and scalability"""

def demonstrate_level_responses(level: str):
    """Show how each level handles the recursion question"""
    
    system_prompt = create_system_prompt(level)
    user_prompt = "How does recursion work?"
    
    print(f"\n{'='*50}")
    print(f"📚 Level: {level.upper()}")
    print(f"{'='*50}")
    print(f"User asks: '{user_prompt}'")
    print("\nResponse adapted to level:")
    
    if level == "beginner":
        print("""
"Great question! Let me explain recursion with something familiar!

Imagine you're looking for your toy in nested boxes. You have a big box, 
and inside might be smaller boxes, and those might have even smaller boxes!

Here's how you'd search:
1. Open a box
2. If you find your toy - great, you're done!
3. If you find another box - repeat these same steps with that box
4. Keep going until you find your toy or run out of boxes

That's recursion! It's when a function calls itself to solve a smaller 
piece of the same problem. Like opening box after box using the same 
'open and check' process!

Simple code example:
def count_down(n):
    print(n)
    if n > 0:
        count_down(n - 1)  # Calling itself!

It prints 5, 4, 3, 2, 1, 0 - each time calling itself with a smaller number!"
        """)
    
    elif level == "intermediate":
        print("""
"Recursion is when a function calls itself to solve smaller instances 
of the same problem. You already know functions can call other functions - 
well, they can also call themselves!

Key components of recursion:
1. Base case - the condition that stops the recursion
2. Recursive case - where the function calls itself with modified parameters

Think of it like this: You solve a big problem by breaking it into smaller 
versions of the same problem, until you reach a version so simple you can 
solve it directly.

Example - calculating factorial:
def factorial(n):
    if n <= 1:  # Base case
        return 1
    else:  # Recursive case
        return n * factorial(n - 1)

factorial(5) = 5 * factorial(4) = 5 * 4 * factorial(3)... and so on.

The function keeps calling itself with smaller values until it hits 
the base case (n <= 1), then all the calls resolve back up the chain. 
Be careful though - forgetting the base case causes infinite recursion!"
        """)
    
    else:  # advanced
        print("""
"Recursion leverages the call stack to solve problems with self-similar 
structure. Each recursive call pushes a new stack frame, maintaining its 
own scope and parameters.

Key considerations:
1. Stack depth limitations (typically ~1000 in Python due to RecursionLimit)
2. Memory overhead from stack frames (O(n) space complexity minimum)
3. Tail recursion optimization (not supported in Python, unfortunately)

Classic recursive patterns:
- Divide and conquer (mergesort, quicksort)
- Tree/graph traversal (DFS)
- Dynamic programming with memoization
- Backtracking algorithms

Example with complexity analysis:
def fibonacci(n, memo={}):
    if n in memo:  # Memoization - O(1) lookup
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)
    return memo[n]

Without memoization: O(2^n) time
With memoization: O(n) time, O(n) space

Often, iterative solutions are more efficient in Python due to function 
call overhead and lack of tail-call optimization. Consider using 
@functools.lru_cache for automatic memoization in production code."
        """)

# Test all three levels
if __name__ == "__main__":
    print("ADAPTIVE TEACHING ASSISTANT")
    print("Same question, three different approaches based on student level")
    
    for level in ["beginner", "intermediate", "advanced"]:
        demonstrate_level_responses(level)
    
    print("\n" + "="*50)
    print("KEY OBSERVATIONS:")
    print("- Beginner: Physical analogies, celebration, simple code")
    print("- Intermediate: Technical concepts, building on knowledge")
    print("- Advanced: CS theory, performance analysis, best practices")