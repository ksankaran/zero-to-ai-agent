# From: Zero to AI Agent, Chapter 12, Section 12.4
# File: structured_inputs.py

from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.tools import StructuredTool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Define the structure of your inputs using Pydantic
class FlightSearchInput(BaseModel):
    origin: str = Field(description="Departure city")
    destination: str = Field(description="Arrival city")  
    date: str = Field(description="Date in YYYY-MM-DD format")
    passengers: int = Field(default=1, description="Number of passengers")
    class_type: Optional[str] = Field(default="economy", description="economy, business, or first")

def search_flights(
    origin: str,
    destination: str,
    date: str,
    passengers: int = 1,
    class_type: str = "economy"
) -> str:
    """Search for flights based on criteria."""
    # Simulated search
    price = 200 * passengers
    if class_type == "business":
        price *= 3
    elif class_type == "first":
        price *= 5
    
    return f"Found flights from {origin} to {destination} on {date}: ${price} for {passengers} passenger(s) in {class_type}"

# Create a structured tool
flight_tool = StructuredTool.from_function(
    func=search_flights,
    name="search_flights",
    description="Search for available flights",
    args_schema=FlightSearchInput
)

# Use with function calling
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools([flight_tool])

# Complex request
response = llm_with_tools.invoke([
    HumanMessage(content="Find me business class flights from New York to London on March 15th, 2024 for 2 people")
])

if response.tool_calls:
    tool_call = response.tool_calls[0]
    print("Structured input parsed perfectly:")
    for key, value in tool_call['args'].items():
        print(f"  {key}: {value}")
    
    # Execute with confidence - parameters are guaranteed correct!
    result = search_flights(**tool_call['args'])
    print(f"\nResult: {result}")
