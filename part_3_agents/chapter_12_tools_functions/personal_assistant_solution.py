# From: Zero to AI Agent, Chapter 12, Section 12.7
# File: personal_assistant_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import os

load_dotenv()

# 1. Time Management Tools
def get_time_zone(location: str) -> str:
    """Get time in different timezones."""
    timezone_offsets = {
        "NYC": -5, "London": 0, "Tokyo": 9, 
        "Paris": 1, "Sydney": 11
    }
    
    if location in timezone_offsets:
        utc_now = datetime.utcnow()
        local_time = utc_now + timedelta(hours=timezone_offsets[location])
        return f"Time in {location}: {local_time.strftime('%I:%M %p')}"
    return f"Unknown timezone for {location}"

def set_reminder(reminder: str) -> str:
    """Save a reminder to file."""
    try:
        with open("reminders.txt", "a") as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            f.write(f"[{timestamp}] {reminder}\n")
        return f"Reminder set: {reminder}"
    except:
        return "Error setting reminder"

# 2. Task Management Tools
def manage_todo(action_and_task: str) -> str:
    """Manage todo list. Input: 'add:task' or 'complete:task' or 'list'"""
    parts = action_and_task.split(':')
    action = parts[0].lower()
    
    todos_file = "todos.json"
    
    # Load existing todos
    if os.path.exists(todos_file):
        with open(todos_file, 'r') as f:
            todos = json.load(f)
    else:
        todos = []
    
    if action == "add" and len(parts) > 1:
        task = ':'.join(parts[1:])
        todos.append({"task": task, "done": False})
        with open(todos_file, 'w') as f:
            json.dump(todos, f)
        return f"Added task: {task}"
    
    elif action == "complete" and len(parts) > 1:
        task = ':'.join(parts[1:])
        for todo in todos:
            if todo["task"] == task:
                todo["done"] = True
        with open(todos_file, 'w') as f:
            json.dump(todos, f)
        return f"Completed: {task}"
    
    elif action == "list":
        pending = [t["task"] for t in todos if not t["done"]]
        return f"Pending tasks: {', '.join(pending) if pending else 'None'}"
    
    return "Usage: 'add:task', 'complete:task', or 'list'"

# 3. Calculation Tools
def unit_converter(conversion_request: str) -> str:
    """Convert units. Input: 'value unit to unit' like '10 meters to feet'"""
    conversions = {
        ("meters", "feet"): 3.28084,
        ("feet", "meters"): 0.3048,
        ("kg", "pounds"): 2.20462,
        ("celsius", "fahrenheit"): lambda c: c * 9/5 + 32,
    }
    
    try:
        parts = conversion_request.lower().split()
        value = float(parts[0])
        from_unit = parts[1]
        to_unit = parts[3]
        
        key = (from_unit, to_unit)
        if key in conversions:
            if callable(conversions[key]):
                result = conversions[key](value)
            else:
                result = value * conversions[key]
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
    except:
        pass
    
    return "Conversion not available. Try: '10 meters to feet'"

# 4. Weather Tool (enhanced)
def weather_assistant(city: str) -> str:
    """Get weather and clothing suggestions."""
    weather_data = {
        "London": {"temp": 59, "condition": "Rainy"},
        "Paris": {"temp": 64, "condition": "Cloudy"},
        "NYC": {"temp": 72, "condition": "Sunny"},
    }
    
    if city in weather_data:
        data = weather_data[city]
        suggestion = ""
        
        if "rain" in data["condition"].lower():
            suggestion = " Bring an umbrella!"
        elif data["temp"] < 60:
            suggestion = " Wear a jacket!"
        elif data["temp"] > 75:
            suggestion = " Light clothing recommended!"
        
        return f"Weather in {city}: {data['temp']}°F, {data['condition']}.{suggestion}"
    
    return f"No weather data for {city}"

# Create all tools
tools = [
    Tool(name="TimeZone", func=get_time_zone, 
         description="Get time in a city. Input: city name like 'NYC' or 'London'"),
    Tool(name="Reminder", func=set_reminder,
         description="Set a reminder. Input: reminder text"),
    Tool(name="TodoList", func=manage_todo,
         description="Manage todos. Input: 'add:task', 'complete:task', or 'list'"),
    Tool(name="UnitConverter", func=unit_converter,
         description="Convert units. Input: 'value from_unit to to_unit'"),
    Tool(name="Weather", func=weather_assistant,
         description="Get weather and clothing suggestions. Input: city name"),
]

# Create the personal assistant
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
client = Client(api_key=langsmith_api_key)
prompt = client.pull_prompt("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=6,
    handle_parsing_errors=True
)

print("🤖 PERSONAL ASSISTANT READY!")
print("=" * 50)

# Test complex query from the challenge
test_query = """What's the weather in Paris and NYC, which is warmer, 
and add 'pack umbrella' to my todo list if either is rainy"""

print(f"User: {test_query}")
print("-" * 50)

result = agent_executor.invoke({"input": test_query})
print(f"\nAssistant: {result['output']}")
