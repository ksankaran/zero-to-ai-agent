# From: Zero to AI Agent, Chapter 16, Section 16.1
# File: exercise_3_16_1_solution.py

"""
Exercise 3 Solution: Specialist vs. Generalist Comparison

This file compares single-agent vs multi-agent approaches for code review.
Run this file to see both approaches analyze the same code.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# The code to analyze
CODE = """
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    average = total / len(numbers)
    return average
"""

print("=" * 60)
print("CODE UNDER REVIEW:")
print("=" * 60)
print(CODE)

# =============================================================================
# APPROACH 1: Single Agent (Generalist)
# =============================================================================

GENERALIST_PROMPT = """You are a code review assistant.
For the given code:
1. Identify any bugs or potential issues
2. Suggest performance optimizations
3. Add comprehensive documentation

Provide all three analyses."""

print("\n" + "=" * 60)
print("APPROACH 1: SINGLE AGENT (GENERALIST)")
print("=" * 60)

response = llm.invoke(f"""
{GENERALIST_PROMPT}

Code:
```python
{CODE}
```
""")

print(response.content)

# =============================================================================
# APPROACH 2: Multi-Agent (Specialists)
# =============================================================================

print("\n" + "=" * 60)
print("APPROACH 2: MULTI-AGENT (SPECIALISTS)")
print("=" * 60)


# Shared state for all agents
class CodeReviewState(TypedDict):
    code: str
    bugs: str
    optimizations: str
    documentation: str


# Agent 1: Bug Finder
def bug_finder_agent(state: CodeReviewState) -> dict:
    """Specialist agent for finding bugs."""
    prompt = """You are a bug detection specialist.
    Your ONLY job is finding bugs and potential runtime errors.
    Look for: edge cases, type errors, division issues, index errors.
    Be thorough. List each bug with severity (critical/medium/low)."""
    
    response = llm.invoke(f"{prompt}\n\nCode:\n```python\n{state['code']}\n```")
    return {"bugs": response.content}


# Agent 2: Optimizer
def optimizer_agent(state: CodeReviewState) -> dict:
    """Specialist agent for performance optimization."""
    prompt = """You are a performance optimization expert.
    Your ONLY job is suggesting performance improvements.
    Consider: algorithmic efficiency, Pythonic idioms, memory usage.
    Rate each suggestion by impact (high/medium/low)."""
    
    response = llm.invoke(f"{prompt}\n\nCode:\n```python\n{state['code']}\n```")
    return {"optimizations": response.content}


# Agent 3: Documenter
def documenter_agent(state: CodeReviewState) -> dict:
    """Specialist agent for documentation."""
    prompt = """You are a documentation specialist.
    Your ONLY job is writing clear, comprehensive documentation.
    Include: docstring, parameter descriptions, return value, examples.
    Follow Google-style Python docstrings."""
    
    response = llm.invoke(f"{prompt}\n\nCode:\n```python\n{state['code']}\n```")
    return {"documentation": response.content}


# Build the multi-agent graph
workflow = StateGraph(CodeReviewState)

workflow.add_node("bug_finder", bug_finder_agent)
workflow.add_node("optimizer", optimizer_agent)
workflow.add_node("documenter", documenter_agent)

# All three run in sequence (could also be parallel in advanced setups)
workflow.add_edge(START, "bug_finder")
workflow.add_edge("bug_finder", "optimizer")
workflow.add_edge("optimizer", "documenter")
workflow.add_edge("documenter", END)

app = workflow.compile()

# Run the multi-agent system
result = app.invoke({
    "code": CODE,
    "bugs": "",
    "optimizations": "",
    "documentation": ""
})

print("\n🐛 BUG FINDER AGENT:")
print("-" * 40)
print(result["bugs"])
print("\n⚡ OPTIMIZER AGENT:")
print("-" * 40)
print(result["optimizations"])
print("\n📝 DOCUMENTER AGENT:")
print("-" * 40)
print(result["documentation"])

# =============================================================================
# COMPARISON NOTES
# =============================================================================

print("\n" + "=" * 60)
print("OBSERVATIONS:")
print("=" * 60)
print("""
1. DEPTH: Multi-agent responses go deeper in each area
2. FOCUS: Specialists fully explore their domain without context switching
3. QUALITY: Documentation from specialist is production-ready
4. TRADE-OFF: Multi-agent uses ~3x the API calls - worth it when quality matters
""")
