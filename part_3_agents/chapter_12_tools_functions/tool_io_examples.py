# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: tool_io_examples.py

from langchain_core.tools import Tool
import json
from datetime import datetime

# Tool with multiple inputs (passed as formatted string)
def create_reminder(reminder_text: str) -> str:
    """
    Create a reminder with date and message.
    Format: 'DATE|MESSAGE' like '2024-12-25|Christmas Day'
    """
    try:
        parts = reminder_text.split('|')
        if len(parts) != 2:
            return "Error: Use format 'DATE|MESSAGE'"
        
        date_str, message = parts
        # Validate date
        reminder_date = datetime.strptime(date_str.strip(), '%Y-%m-%d')
        
        return f"✓ Reminder set for {date_str}: {message}"
    except ValueError:
        return "Error: Invalid date format. Use YYYY-MM-DD"

# Tool that returns structured data (as formatted string)
def get_weather(city: str) -> str:
    """Get weather for a city (simulated)."""
    # In real life, this would call an API
    weather_data = {
        "New York": {"temp": 72, "condition": "Sunny", "humidity": 65},
        "London": {"temp": 59, "condition": "Cloudy", "humidity": 80},
        "Tokyo": {"temp": 68, "condition": "Clear", "humidity": 55}
    }
    
    if city in weather_data:
        data = weather_data[city]
        return f"Weather in {city}: {data['temp']}°F, {data['condition']}, {data['humidity']}% humidity"
    else:
        return f"Weather data not available for {city}"

# Create the tools
reminder_tool = Tool(
    name="ReminderCreator",
    func=create_reminder,
    description="Create a reminder. Input format: 'YYYY-MM-DD|message text'"
)

weather_tool = Tool(
    name="WeatherChecker", 
    func=get_weather,
    description="Get current weather for a city. Input: city name"
)

# Test them
print(reminder_tool.func("2024-12-25|Christmas Day"))
print(weather_tool.func("New York"))
