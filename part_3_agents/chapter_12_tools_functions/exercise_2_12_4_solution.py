# From: Zero to AI Agent, Chapter 12, Section 12.4
# File: exercise_2_12_4_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class CalculatorInput(BaseModel):
    expression: str = Field(description="Expression to be evaluated in calculator")

def calculator(expression: str) -> str:
    """Perform calculation safely."""
    try:
        # Only allow safe operations
        allowed = set('0123456789+-*/().')
        if all(c in allowed or c.isspace() for c in expression):
            result = eval(expression)
            return f"{result}"
        return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {str(e)}"

calc_tool = Tool.from_function(
    func=calculator,
    name="Calculator",
    args_schema=CalculatorInput,
    description="Calculate math expressions"
)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools([calc_tool])

# Test multi-step calculation
queries = [
    "Calculate 15 * 4, 100 / 5, and 78 + 22",
    "What is 25 squared minus 100?",
    "Calculate (10 + 5) * 3"
]

for query in queries:
    print(f"\nQuery: {query}")
    response = llm_with_tools.invoke([HumanMessage(content=query)])
    
    if response.tool_calls:
        print(f"Parallel calculations: {len(response.tool_calls)} operations")
        for i, tool_call in enumerate(response.tool_calls, 1):
            print("tool_call: ", tool_call)
            result = calculator(tool_call['args']['expression'])
            print(f"  {i}. {tool_call['args']['expression']} = {result}")
