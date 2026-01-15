# From: Zero to AI Agent, Chapter 12, Section 12.5
# File: multi_tool_orchestration.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

# Create a suite of complementary tools
def get_date(dummy_input: str = "") -> str:
    """Get today's date. The dummy_input is ignored."""
    return datetime.now().strftime("%Y-%m-%d")

def search_events(input_str: str) -> str:
    """Search for events. Input format: 'date|location'"""
    try:
        date, location = input_str.split("|")
        return f"Events on {date} in {location}: Concert at 7pm, Festival at noon"
    except:
        return "Error: Please provide input as 'date|location'"

def check_weather(input_str: str) -> str:
    """Check weather. Input format: 'date|location'"""
    try:
        date, location = input_str.split("|")
        return f"Weather for {location} on {date}: Sunny, 75°F"
    except:
        return "Error: Please provide input as 'date|location'"

def make_recommendation(input_str: str) -> str:
    """Make recommendation. Input format: 'events|weather'"""
    try:
        events, weather = input_str.split("|")
        if "Sunny" in weather and "Festival" in events:
            return "Perfect day for the outdoor festival!"
        elif "Concert" in events:
            return "Evening concert would be great!"
        return "Consider indoor activities."
    except:
        return "Error: Please provide input as 'events|weather'"

# Design tools to work together
tools = [
    Tool(
        name="get_current_date",
        func=get_date,
        description="Get today's date in YYYY-MM-DD format. Just call without arguments."
    ),
    Tool(
        name="search_events",
        func=search_events,
        description="Find events. Input: 'date|location' like '2024-03-15|New York'"
    ),
    Tool(
        name="check_weather",
        func=check_weather,
        description="Check weather. Input: 'date|location' like '2024-03-15|New York'"
    ),
    Tool(
        name="make_recommendation",
        func=make_recommendation,
        description="Make recommendation. Input: 'events info|weather info'"
    )
]

# Initialize LLM and get prompt
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Get the ReAct prompt from LangSmith
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
client = Client(api_key=langsmith_api_key)
prompt = client.pull_prompt("hwchase17/react")

# Create agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

# Test orchestration
test_queries = [
    "What should I do in New York today?",
    "Find events and weather for Boston tomorrow"
]

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)
    
    result = agent_executor.invoke({"input": query})
    print(f"\nFinal Answer: {result['output']}")