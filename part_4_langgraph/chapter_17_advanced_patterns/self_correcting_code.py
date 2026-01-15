# From: Zero to AI Agent, Chapter 17, Section 17.6
# Save as: self_correcting_code.py

from typing import TypedDict, Annotated
import operator
import traceback
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

class CodeState(TypedDict):
    task: str
    code: str
    test_result: str
    error_message: str
    is_working: bool
    iteration: int
    max_iterations: int
    attempt_history: Annotated[list[str], operator.add]

def generate_code(state: CodeState) -> dict:
    """Generate or fix code."""
    
    if state["iteration"] == 0:
        prompt = f"""Write Python code to accomplish this task.
Return ONLY the code, no explanations.

Task: {state['task']}

Code:"""
    else:
        prompt = f"""Fix this Python code based on the error.

Task: {state['task']}

Current code:
```python
{state['code']}
```

Error:
{state['error_message']}

Write the corrected code only:"""
    
    response = llm.invoke(prompt)
    
    # Extract code from response (handle markdown code blocks)
    code = response.content
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]
    
    return {
        "code": code.strip(),
        "iteration": state["iteration"] + 1,
        "attempt_history": [f"Attempt {state['iteration'] + 1}"]
    }

def test_code(state: CodeState) -> dict:
    """Execute the code and capture results."""
    
    code = state["code"]
    
    try:
        # Create a restricted execution environment
        exec_globals = {"__builtins__": __builtins__}
        exec_locals = {}
        
        # Execute the code
        exec(code, exec_globals, exec_locals)
        
        # If we get here, code ran without errors
        return {
            "is_working": True,
            "test_result": "Code executed successfully",
            "error_message": ""
        }
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        return {
            "is_working": False,
            "test_result": "Code failed",
            "error_message": error_msg
        }

def check_code_status(state: CodeState) -> str:
    """Check if code works or needs fixing."""
    
    if state["is_working"]:
        return "success"
    
    if state["iteration"] >= state["max_iterations"]:
        return "give_up"
    
    return "fix"

def build_code_graph():
    graph = StateGraph(CodeState)
    
    graph.add_node("generate", generate_code)
    graph.add_node("test", test_code)
    
    graph.add_edge(START, "generate")
    graph.add_edge("generate", "test")
    
    graph.add_conditional_edges(
        "test",
        check_code_status,
        {
            "fix": "generate",
            "success": END,
            "give_up": END
        }
    )
    
    return graph.compile()

def test_code_generation():
    graph = build_code_graph()
    
    tasks = [
        "Write a function called 'fibonacci' that returns the nth fibonacci number",
        "Write a function called 'is_palindrome' that checks if a string is a palindrome",
        "Write a function called 'flatten' that flattens a nested list"
    ]
    
    for task in tasks:
        print("\n" + "=" * 60)
        print(f"🎯 Task: {task}")
        print("=" * 60)
        
        result = graph.invoke({
            "task": task,
            "code": "",
            "test_result": "",
            "error_message": "",
            "is_working": False,
            "iteration": 0,
            "max_iterations": 3,
            "attempt_history": []
        })
        
        status = "✅ Success" if result["is_working"] else "❌ Failed"
        print(f"\n{status} after {result['iteration']} attempts")
        print(f"\n📝 Final Code:\n{result['code']}")

if __name__ == "__main__":
    test_code_generation()
