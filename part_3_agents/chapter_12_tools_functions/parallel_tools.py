# From: Zero to AI Agent, Chapter 12, Section 12.4
# File: parallel_tools.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Define input schema for city-based tools
class CityInput(BaseModel):
    city: str = Field(description="Name of the city")

# Define multiple tools
def get_temperature(city: str) -> str:
    temps = {"New York": 72, "London": 59, "Tokyo": 68}
    return f"{temps.get(city, 'Unknown')}°F"

def get_time(city: str) -> str:
    times = {"New York": "10:30 AM", "London": "3:30 PM", "Tokyo": "11:30 PM"}
    return times.get(city, "Unknown")

def get_population(city: str) -> str:
    pops = {"New York": "8.3M", "London": "9.5M", "Tokyo": "14M"}
    return pops.get(city, "Unknown")

# Create tools with proper args_schema
tools = [
    Tool(
        name="get_temperature",
        func=get_temperature,
        description="Get temperature for a city",
        args_schema=CityInput  # Required for bind_tools!
    ),
    Tool(
        name="get_time",
        func=get_time,
        description="Get current time for a city",
        args_schema=CityInput  # Required for bind_tools!
    ),
    Tool(
        name="get_population",
        func=get_population,
        description="Get population for a city",
        args_schema=CityInput  # Required for bind_tools!
    )
]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Ask for multiple pieces of information
response = llm_with_tools.invoke([
    HumanMessage(content="Tell me the temperature, time, and population of New York")
])

print("Parallel tool calls:")
if response.tool_calls:
    for i, tool_call in enumerate(response.tool_calls, 1):
        print(f"\nTool Call {i}:")
        print(f"  Function: {tool_call['name']}")
        print(f"  Arguments: {tool_call['args']}")
        
        # Execute the function properly
        if tool_call['name'] == 'get_temperature':
            result = get_temperature(**tool_call['args'])
        elif tool_call['name'] == 'get_time':
            result = get_time(**tool_call['args'])
        elif tool_call['name'] == 'get_population':
            result = get_population(**tool_call['args'])
        else:
            result = "Unknown tool"
        
        print(f"  Result: {result}")

print("\nAll three tools called in parallel - much faster than sequential!")