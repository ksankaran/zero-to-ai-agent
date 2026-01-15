# From: Zero to AI Agent, Chapter 12, Section 12.4
# File: function_calling_intro.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import Tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json

load_dotenv()

# Define the input schema
class WeatherInput(BaseModel):
    location: str = Field(description="The city or location to get weather for")
    unit: str = Field(default="fahrenheit", description="Temperature unit: 'fahrenheit' or 'celsius'")

# Define a simple function
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the weather for a location."""
    # Simulated weather data
    weather_data = {
        "New York": {"f": 72, "c": 22},
        "London": {"f": 59, "c": 15},
        "Tokyo": {"f": 68, "c": 20}
    }
    
    if location in weather_data:
        temp = weather_data[location]["c" if unit == "celsius" else "f"]
        unit_symbol = "°C" if unit == "celsius" else "°F"
        return f"The weather in {location} is {temp}{unit_symbol}"
    return f"Weather data not available for {location}"

# Convert to a tool with schema
weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="Get weather for a location",
    args_schema=WeatherInput  # THIS IS CRITICAL!
)

# Modern way: Bind tools directly to the model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools([weather_tool])

# Ask a question that needs the tool
response = llm_with_tools.invoke([
    HumanMessage(content="What's the weather in New York?")
])

print("LLM Response:", response)

# If the LLM wants to use a tool, it tells us EXACTLY how
if response.tool_calls:
    tool_call = response.tool_calls[0]
    print(f"\nTool to call: {tool_call['name']}")
    print(f"Arguments: {tool_call['args']}")
    
    # Execute the function with the exact arguments
    result = get_weather(**tool_call['args'])
    print(f"Result: {result}")