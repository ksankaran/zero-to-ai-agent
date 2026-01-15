# From: Zero to AI Agent, Chapter 17, Section 17.6
# Save as: exercise_2_17_6_solution.py
# Exercise 2: Bug-Fixing Agent

from typing import TypedDict, Annotated
import operator
import traceback
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

class BugFixState(TypedDict):
    buggy_code: str
    expected_behavior: str
    test_cases: list[dict]  # [{"input": ..., "expected": ...}]
    current_code: str
    error_message: str
    test_output: str
    is_fixed: bool
    iteration: int
    max_iterations: int
    fix_attempts: Annotated[list[dict], operator.add]
    bug_diagnosis: str

def diagnose_and_fix(state: BugFixState) -> dict:
    """Analyze the bug and attempt a fix."""
    
    if state["iteration"] == 0:
        # First attempt - analyze the buggy code
        prompt = f"""Analyze this buggy code and fix it.

Buggy Code:
```python
{state['buggy_code']}
```

Expected Behavior:
{state['expected_behavior']}

Test Cases:
{state['test_cases']}

First, identify what the bug is.
Then, write the corrected code.

Format your response as:
BUG: <description of the bug>
FIXED CODE:
```python
<corrected code>
```"""
    else:
        # Subsequent attempts - fix based on error
        prompt = f"""The previous fix didn't work. Try again.

Original Buggy Code:
```python
{state['buggy_code']}
```

Current Attempted Fix:
```python
{state['current_code']}
```

Error/Test Failure:
{state['error_message']}

Previous diagnosis: {state['bug_diagnosis']}

Write a new corrected version:

BUG: <updated diagnosis>
FIXED CODE:
```python
<corrected code>
```"""
    
    response = llm.invoke(prompt)
    content = response.content
    
    # Extract bug diagnosis
    bug_diagnosis = ""
    if "BUG:" in content:
        bug_section = content.split("BUG:")[1]
        bug_diagnosis = bug_section.split("FIXED CODE")[0].strip() if "FIXED CODE" in bug_section else bug_section.split("\n")[0].strip()
    
    # Extract code
    code = state["buggy_code"]  # Default to original if parsing fails
    if "```python" in content:
        code = content.split("```python")[1].split("```")[0].strip()
    elif "```" in content:
        parts = content.split("```")
        if len(parts) >= 2:
            code = parts[1].strip()
    
    return {
        "current_code": code,
        "bug_diagnosis": bug_diagnosis,
        "iteration": state["iteration"] + 1,
        "fix_attempts": [{
            "attempt": state["iteration"] + 1,
            "diagnosis": bug_diagnosis,
            "code_snippet": code[:100] + "..."
        }]
    }

def run_tests(state: BugFixState) -> dict:
    """Run the test cases against the current code."""
    
    code = state["current_code"]
    test_cases = state["test_cases"]
    
    try:
        # Execute the code to define functions
        exec_globals = {"__builtins__": __builtins__}
        exec_locals = {}
        exec(code, exec_globals, exec_locals)
        
        # Run test cases
        all_passed = True
        test_results = []
        
        for i, test in enumerate(test_cases):
            try:
                # Get the function name from the code (assumes first defined function)
                func_name = None
                for name, obj in exec_locals.items():
                    if callable(obj):
                        func_name = name
                        break
                
                if func_name is None:
                    raise Exception("No function found in code")
                
                func = exec_locals[func_name]
                
                # Run the test
                if isinstance(test["input"], tuple):
                    result = func(*test["input"])
                else:
                    result = func(test["input"])
                
                if result == test["expected"]:
                    test_results.append(f"Test {i+1}: PASS")
                else:
                    test_results.append(f"Test {i+1}: FAIL (got {result}, expected {test['expected']})")
                    all_passed = False
                    
            except Exception as e:
                test_results.append(f"Test {i+1}: ERROR - {str(e)}")
                all_passed = False
        
        return {
            "is_fixed": all_passed,
            "test_output": "\n".join(test_results),
            "error_message": "" if all_passed else f"Test failures:\n{chr(10).join(test_results)}"
        }
        
    except Exception as e:
        return {
            "is_fixed": False,
            "test_output": f"Execution error: {str(e)}",
            "error_message": f"{type(e).__name__}: {str(e)}"
        }

def check_fix_status(state: BugFixState) -> str:
    """Check if bug is fixed or need more attempts."""
    
    if state["is_fixed"]:
        return "fixed"
    
    if state["iteration"] >= state["max_iterations"]:
        return "give_up"
    
    return "retry"

def build_bug_fixer():
    graph = StateGraph(BugFixState)
    
    graph.add_node("fix", diagnose_and_fix)
    graph.add_node("test", run_tests)
    
    graph.add_edge(START, "fix")
    graph.add_edge("fix", "test")
    
    graph.add_conditional_edges(
        "test",
        check_fix_status,
        {
            "retry": "fix",
            "fixed": END,
            "give_up": END
        }
    )
    
    return graph.compile()

def test_bug_fixer():
    graph = build_bug_fixer()
    
    # Test cases with buggy code
    test_cases = [
        {
            "name": "Off-by-one error in sum",
            "buggy_code": """
def sum_list(numbers):
    total = 0
    for i in range(len(numbers) - 1):  # Bug: should be len(numbers)
        total += numbers[i]
    return total
""",
            "expected_behavior": "Sum all numbers in the list",
            "tests": [
                {"input": [1, 2, 3], "expected": 6},
                {"input": [10, 20], "expected": 30},
                {"input": [5], "expected": 5}
            ]
        },
        {
            "name": "Wrong comparison operator",
            "buggy_code": """
def is_positive(n):
    if n > 0:  # Should be >= for including 0 as non-negative
        return True
    return False
    
def count_positive(numbers):
    count = 0
    for n in numbers:
        if n < 0:  # Bug: should be n > 0
            count += 1
    return count
""",
            "expected_behavior": "Count how many positive numbers are in the list",
            "tests": [
                {"input": [1, -2, 3, -4, 5], "expected": 3},
                {"input": [-1, -2, -3], "expected": 0},
                {"input": [0, 1, 2], "expected": 2}
            ]
        }
    ]
    
    for test_case in test_cases:
        print("\n" + "=" * 60)
        print(f"🐛 Bug Fix Test: {test_case['name']}")
        print("=" * 60)
        
        result = graph.invoke({
            "buggy_code": test_case["buggy_code"],
            "expected_behavior": test_case["expected_behavior"],
            "test_cases": test_case["tests"],
            "current_code": "",
            "error_message": "",
            "test_output": "",
            "is_fixed": False,
            "iteration": 0,
            "max_iterations": 5,
            "fix_attempts": [],
            "bug_diagnosis": ""
        })
        
        status = "✅ FIXED" if result["is_fixed"] else "❌ NOT FIXED"
        print(f"\nResult: {status} after {result['iteration']} attempts")
        
        print("\n📋 Fix Attempts:")
        for attempt in result["fix_attempts"]:
            print(f"  Attempt {attempt['attempt']}: {attempt['diagnosis'][:80]}...")
        
        print(f"\n🔍 Final Diagnosis: {result['bug_diagnosis']}")
        print(f"\n📊 Test Results:\n{result['test_output']}")
        
        if result["is_fixed"]:
            print(f"\n✅ Fixed Code:\n{result['current_code']}")

if __name__ == "__main__":
    test_bug_fixer()
