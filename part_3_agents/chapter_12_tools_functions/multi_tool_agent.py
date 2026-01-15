# From: Zero to AI Agent, Chapter 12, Section 12.7
# File: multi_tool_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client
from dotenv import load_dotenv
from datetime import datetime
import random
import os

load_dotenv()

# Create diverse tools
def calculate(expression: str) -> str:
    """Perform mathematical calculations."""
    try:
        # Safety: only allow numbers and basic operations
        allowed = set('0123456789+-*/().')
        if all(c in allowed or c.isspace() for c in expression):
            result = eval(expression)
            return str(result)
        return "Error: Only basic math operations allowed"
    except Exception as e:
        return f"Error: {str(e)}"

def get_time(location: str = "local") -> str:
    """Get current time."""
    current_time = datetime.now()
    return f"Current time: {current_time.strftime('%I:%M %p, %A, %B %d, %Y')}"

def get_weather(city: str) -> str:
    """Get weather for a city (simulated)."""
    # In production, this would call a real weather API
    weather_data = {
        "New York": {"temp": 72, "condition": "Partly cloudy"},
        "London": {"temp": 59, "condition": "Rainy"},
        "Tokyo": {"temp": 68, "condition": "Clear"},
        "Paris": {"temp": 64, "condition": "Cloudy"},
    }
    
    if city in weather_data:
        data = weather_data[city]
        return f"Weather in {city}: {data['temp']}°F, {data['condition']}"
    else:
        return f"Weather data not available for {city}"

def search_info(query: str) -> str:
    """Search for information (simulated)."""
    # In production, this would use a real search API
    responses = {
        "python": "Python is a high-level programming language known for its simplicity.",
        "langchain": "LangChain is a framework for building applications with LLMs.",
        "agent": "An AI agent is a system that can perceive, reason, and act autonomously.",
    }
    
    query_lower = query.lower()
    for key, value in responses.items():
        if key in query_lower:
            return value
    
    return f"Information about '{query}' is not in my current database."

# Create tool objects
tools = [
    Tool(
        name="Calculator",
        func=calculate,
        description="Perform mathematical calculations. Input: math expression like '2+2' or '15*3.14'"
    ),
    Tool(
        name="Clock",
        func=get_time,
        description="Get the current date and time. Input: location (or 'local' for local time)"
    ),
    Tool(
        name="Weather",
        func=get_weather,
        description="Get current weather for a city. Input: city name"
    ),
    Tool(
        name="Search",
        func=search_info,
        description="Search for information about a topic. Input: search query"
    ),
]

# Create the agent
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
client = Client(api_key=langsmith_api_key)
prompt = client.pull_prompt("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)

# Create executor with safety limits
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,  # Prevent infinite loops
    handle_parsing_errors=True  # Handle any parsing issues
)

print("🤖 MULTI-TOOL AI AGENT READY!")
print("=" * 50)

# Test with various queries
test_queries = [
    "What's 25 * 4?",
    "What time is it?",
    "What's the weather in London?",
    "Tell me about Python",
    "What's the weather in Paris and what's 100 divided by 4?",  # Multiple tools!
]

for query in test_queries:
    print(f"\n📝 User: {query}")
    print("-" * 40)
    
    result = agent_executor.invoke({"input": query})
    
    print(f"\n🤖 Agent: {result['output']}")
    print("=" * 50)
