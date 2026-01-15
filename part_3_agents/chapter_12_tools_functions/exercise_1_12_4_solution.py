# From: Zero to AI Agent, Chapter 12, Section 12.4
# File: exercise_1_12_4_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class WeatherInput(BaseModel):
    city: str = Field(description="City name")
    unit: Literal["celsius", "fahrenheit", "kelvin"] = Field(
        default="celsius",
        description="Temperature unit"
    )

def get_weather_with_units(city: str, unit: str = "celsius") -> str:
    """Get weather with specified temperature unit."""
    # Simulated weather data (always in Celsius)
    weather_data = {
        "London": {"temp_c": 15, "condition": "Cloudy"},
        "New York": {"temp_c": 22, "condition": "Sunny"},
        "Tokyo": {"temp_c": 18, "condition": "Clear"},
    }
    
    if city not in weather_data:
        return f"Weather data not available for {city}"
    
    data = weather_data[city]
    temp_c = data["temp_c"]
    
    # Convert temperature
    if unit == "fahrenheit":
        temp = (temp_c * 9/5) + 32
        symbol = "°F"
    elif unit == "kelvin":
        temp = temp_c + 273.15
        symbol = "K"
    else:
        temp = temp_c
        symbol = "°C"
    
    return f"Weather in {city}: {temp:.1f}{symbol}, {data['condition']}"

# Create tool with structured input
weather_tool = Tool.from_function(
    func=get_weather_with_units,
    name="GetWeather",
    description="Get weather for a city with temperature unit",
    args_schema=WeatherInput
)

# Test with LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tool = llm.bind_tools([weather_tool])

# Test queries
test_queries = [
    "What's the weather in London?",
    "Weather in New York in Fahrenheit",
    "Tokyo weather in Kelvin"
]

for query in test_queries:
    response = llm_with_tool.invoke([HumanMessage(content=query)])
    if response.tool_calls:
        result = get_weather_with_units(**response.tool_calls[0]['args'])
        print(f"{query} → {result}")
