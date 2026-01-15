# From: Zero to AI Agent, Chapter 12, Section 12.6
# File: graceful_degradation.py

from langchain_core.tools import Tool
from datetime import datetime
import json
import random

def smart_search_tool(query: str, options: str = "{}") -> str:
    """
    Search tool that degrades gracefully based on available services.
    """
    # Parse options
    try:
        opts = json.loads(options)
    except:
        opts = {}
    
    results = []
    
    # Try premium search (most detailed)
    try:
        if "premium" in opts and opts["premium"]:
            # Simulate premium API
            premium_result = f"PREMIUM: Detailed analysis of '{query}' with citations"
            results.append(premium_result)
    except:
        pass  # Premium failed, continue with others
    
    # Try standard search
    try:
        # Simulate standard search
        if random.random() > 0.3:  # 70% success rate
            standard_result = f"STANDARD: Basic information about '{query}'"
            results.append(standard_result)
    except:
        pass  # Standard failed, continue
    
    # Fallback: Use cached results
    try:
        # Simulate cache lookup
        cache = {
            "python": "Python is a programming language",
            "weather": "Weather varies by location",
            "news": "Latest updates from various sources"
        }
        
        for key in cache:
            if key.lower() in query.lower():
                results.append(f"CACHED: {cache[key]}")
                break
    except:
        pass
    
    # Ultimate fallback
    if not results:
        # Provide generic but helpful response
        return f"Unable to search for '{query}' at this time. Try: 1) Simplifying your query, 2) Checking your connection, 3) Trying again in a moment"
    
    # Return best available results
    return " | ".join(results)

def calculation_with_fallback(expression: str) -> str:
    """
    Calculator that falls back to simpler operations if complex ones fail.
    """
    # Try advanced calculation
    try:
        # Attempt with math module for complex operations
        import math
        # Create safe namespace with math functions
        safe_dict = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'sqrt': math.sqrt, 'log': math.log, 'pi': math.pi,
            'e': math.e
        }
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"Result: {result}"
    except:
        pass
    
    # Fallback to basic arithmetic
    try:
        # Only allow basic operations
        if all(c in '0123456789+-*/() .' for c in expression):
            result = eval(expression)
            return f"Result (basic): {result}"
    except:
        pass
    
    # Ultimate fallback: Explain what went wrong
    return f"Error: Cannot calculate '{expression}'. Try using only numbers and basic operations (+, -, *, /)."

print("GRACEFUL DEGRADATION EXAMPLES")
print("=" * 50)

# Test search degradation
search = Tool(name="SmartSearch", func=smart_search_tool, description="Search with fallbacks")

queries = ["python", "quantum computing", "xyz123abc"]
for q in queries:
    print(f"\nSearching: {q}")
    print(f"Result: {search.func(q)}")

# Test calculation degradation  
calc = Tool(name="SmartCalc", func=calculation_with_fallback, description="Calculate with fallbacks")

expressions = ["2+2", "sin(3.14/2)", "invalid expression"]
for expr in expressions:
    print(f"\nCalculating: {expr}")
    print(f"Result: {calc.func(expr)}")
