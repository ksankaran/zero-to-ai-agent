# From: Zero to AI Agent, Chapter 12, Section 12.5
# File: preventing_tool_loops.py

from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langsmith import Client
from dotenv import load_dotenv
import time
import os

load_dotenv()

# Create a tool that might cause loops
call_count = 0

def problematic_search(query: str) -> str:
    global call_count
    call_count += 1
    # This tool returns questions instead of answers - loop risk!
    return f"Did you mean to search for '{query}'? Try being more specific."

def good_search(query: str) -> str:
    global call_count
    call_count += 1
    # This tool returns definitive answers - no loop risk
    return f"Found 5 results for '{query}': Result 1, Result 2, Result 3..."

# Create tools
problematic_tool = Tool(
    name="problematic_search",
    func=problematic_search,
    description="Search for information (might ask for clarification)"
)

good_tool = Tool(
    name="good_search",
    func=good_search,
    description="Search for information (returns definitive results)"
)

# Strategy 1: Set max_iterations
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
client = Client(api_key=langsmith_api_key)
prompt = client.pull_prompt("hwchase17/react")

print("PREVENTING TOOL LOOPS")
print("=" * 50)

# Test with problematic tool (with safety limit)
print("\n1. WITH LOOP PREVENTION (max_iterations=3):")
call_count = 0
agent_safe = create_react_agent(llm, [problematic_tool], prompt)
executor_safe = AgentExecutor(
    agent=agent_safe,
    tools=[problematic_tool],
    max_iterations=3,  # Safety limit!
    verbose=True
)

try:
    result = executor_safe.invoke({"input": "Find information about Python"})
    print(f"Call count: {call_count}")
    print(f"Result: {result['output']}")
except Exception as e:
    print(f"Stopped after {call_count} iterations")

# Test with good tool (no loop risk)
print("\n2. WITH GOOD TOOL DESIGN (returns answers):")
call_count = 0
agent_good = create_react_agent(llm, [good_tool], prompt)
executor_good = AgentExecutor(
    agent=agent_good,
    tools=[good_tool],
    max_iterations=3,
    verbose=False
)

result = executor_good.invoke({"input": "Find information about Python"})
print(f"Call count: {call_count}")
print(f"Result: {result['output'][:100]}...")

print("\n💡 Loop Prevention Strategies:")
print("1. Always set max_iterations (3-5 is usually enough)")
print("2. Tools should return answers, not questions")
print("3. Tools should indicate when they're done")
print("4. Use early_stopping_method='generate' for natural stops")