# From: Zero to AI Agent, Chapter 12, Section 12.4
# File: tool_response_flow.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json

load_dotenv()

# Define input schema for stock price tool
class StockInput(BaseModel):
    symbol: str = Field(description="Stock ticker symbol (e.g., AAPL, GOOGL, MSFT)")

def get_stock_price(symbol: str) -> str:
    """Get current stock price."""
    # Simulated prices
    prices = {
        "AAPL": 178.50,
        "GOOGL": 142.30,
        "MSFT": 405.20
    }
    return json.dumps({
        "symbol": symbol,
        "price": prices.get(symbol.upper(), 0),
        "currency": "USD"
    })

# Create tool with proper args_schema
stock_tool = Tool(
    name="get_stock_price",
    func=get_stock_price,
    description="Get current stock price for a symbol",
    args_schema=StockInput  # Required for bind_tools!
)

# Initialize
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools([stock_tool])

# Start conversation
messages = [
    HumanMessage(content="What's the current price of Apple stock?")
]

# Step 1: LLM decides to use a tool
ai_response = llm_with_tools.invoke(messages)
messages.append(ai_response)

print("Step 1 - LLM wants to use a tool:")
if ai_response.tool_calls:
    print(f"  Tool: {ai_response.tool_calls[0]['name']}")
    print(f"  Args: {ai_response.tool_calls[0]['args']}")
    
    # Step 2: Execute the tool
    tool_call = ai_response.tool_calls[0]
    tool_result = get_stock_price(**tool_call['args'])
    
    # Step 3: Send tool result back to LLM
    tool_message = ToolMessage(
        content=tool_result,
        tool_call_id=tool_call['id']
    )
    messages.append(tool_message)
    
    print("\nStep 2 - Tool execution result:")
    print(f"  {tool_result}")
    
    # Step 4: LLM incorporates result into final response
    final_response = llm_with_tools.invoke(messages)
    
    print("\nStep 3 - Final response to user:")
    print(f"  {final_response.content}")
else:
    print("No tool calls were made")