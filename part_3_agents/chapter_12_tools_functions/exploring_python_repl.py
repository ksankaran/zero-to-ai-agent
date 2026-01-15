# From: Zero to AI Agent, Chapter 12, Section 12.3
# File: exploring_python_repl.py

from langchain_experimental.tools import PythonREPLTool

# Create the Python REPL tool
python_tool = PythonREPLTool()

print("Testing Python REPL Tool")
print("=" * 50)
print("⚠️  This tool can execute ANY Python code - use with caution!")
print()

# Test 1: Simple calculation
print("1. Simple math:")
result = python_tool.run("print(2 ** 10)")
print(f"   2^10 = {result}")
print()

# Test 2: Generate Fibonacci sequence
print("2. Fibonacci sequence:")
fibonacci_code = """
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[-1] + fib[-2])
        return fib

result = fibonacci(10)
print(f"First 10 Fibonacci numbers: {result}")
print(f"Sum: {sum(result)}")
"""
result = python_tool.run(fibonacci_code)
print(f"   {result}")
print()

# Test 3: Data analysis
print("3. Data analysis:")
analysis_code = """
data = [23, 45, 67, 89, 12, 34, 56, 78, 90, 11]
mean = sum(data) / len(data)
maximum = max(data)
minimum = min(data)
print(f"Data: {data}")
print(f"Mean: {mean:.2f}, Max: {maximum}, Min: {minimum}")
"""
result = python_tool.run(analysis_code)
print(f"   {result}")
