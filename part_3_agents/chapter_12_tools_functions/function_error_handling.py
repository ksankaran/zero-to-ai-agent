# From: Zero to AI Agent, Chapter 12, Section 12.4
# File: function_error_handling.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage, ToolMessage
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json

load_dotenv()

# Define input schema for the function
class DivideInput(BaseModel):
    a: float = Field(description="The dividend (number to be divided)")
    b: float = Field(description="The divisor (number to divide by)")

def divide_numbers(a: float, b: float) -> str:
    """Safely divide two numbers with error handling."""
    if b == 0:
        # Return structured error that LLM can understand
        return json.dumps({
            "success": False,
            "error": "Division by zero",
            "suggestion": "Please provide a non-zero divisor"
        })
    
    result = a / b
    return json.dumps({
        "success": True,
        "result": result,
        "calculation": f"{a} ÷ {b} = {result}"
    })

# Create tool with proper args_schema
calc_tool = Tool(
    name="divide_numbers",
    func=divide_numbers,
    description="Divide two numbers safely with error handling",
    args_schema=DivideInput  # THIS IS REQUIRED FOR bind_tools!
)

# Bind tool to LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tool = llm.bind_tools([calc_tool])

# Test cases including error scenarios
test_cases = [
    "What is 100 divided by 5?",
    "Divide 50 by 0",  # This will trigger error handling
    "Calculate 15.5 divided by 2.5"
]

for query in test_cases:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('-'*60)
    
    # Get LLM response
    response = llm_with_tool.invoke([HumanMessage(content=query)])
    
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        print(f"Tool called: {tool_call['name']}")
        print(f"Arguments: {tool_call['args']}")
        
        # Execute the tool
        result = divide_numbers(**tool_call['args'])
        print(f"Tool result: {result}")
        
        # Parse result to check for errors
        result_data = json.loads(result)
        
        # Send result back to LLM for final response
        tool_message = ToolMessage(
            content=result,
            tool_call_id=tool_call['id']
        )
        
        final_response = llm_with_tool.invoke([
            HumanMessage(content=query),
            response,
            tool_message
        ])
        
        print(f"\nFinal answer: {final_response.content}")
        
        # Show how the error was handled
        if not result_data["success"]:
            print(f"⚠️ Error handled gracefully: {result_data['error']}")
            print(f"💡 Suggestion: {result_data['suggestion']}")
    else:
        print("No tool was called")