# From: Zero to AI Agent, Chapter 12, Section 12.5
# File: exercise_3_12_5_solution.py

from langchain_core.tools import Tool
from datetime import datetime, timedelta
import random

# Travel planning tools
def get_current_date() -> str:
    """Get today's date."""
    return datetime.now().strftime("%Y-%m-%d")

def calculate_next_month(date: str = None) -> str:
    """Calculate dates for next month."""
    base = datetime.now() if not date else datetime.strptime(date, "%Y-%m-%d")
    next_month = base + timedelta(days=30)
    return f"{next_month.strftime('%Y-%m-%d')} to {(next_month + timedelta(days=2)).strftime('%Y-%m-%d')}"

def check_weather(location: str, dates: str) -> str:
    """Check weather forecast."""
    # Simulated weather
    weather = random.choice(["Sunny", "Partly Cloudy", "Light Rain"])
    temp = random.randint(60, 75)
    return f"Weather in {location} ({dates}): {weather}, {temp}°F average"

def search_flights(origin: str, destination: str, dates: str) -> str:
    """Search for flights."""
    # Simulated flight search
    price = random.randint(400, 800)
    return f"Flights {origin} → {destination} ({dates}): Found 5 options, from ${price}"

def search_hotels(location: str, dates: str, nights: int = 3) -> str:
    """Search for hotels."""
    # Simulated hotel search
    price = random.randint(100, 200)
    return f"Hotels in {location} ({dates}, {nights} nights): 10 options, from ${price}/night"

def find_activities(location: str, interests: str = "general") -> str:
    """Find activities and attractions."""
    activities = {
        "Tokyo": ["Visit Senso-ji Temple", "Explore Shibuya", "Tokyo Tower", "Tsukiji Market"],
        "Paris": ["Eiffel Tower", "Louvre Museum", "Seine River Cruise", "Montmartre"],
        "default": ["City tour", "Local museum", "Food market", "Parks"]
    }
    city_activities = activities.get(location, activities["default"])
    return f"Top activities in {location}: " + ", ".join(city_activities[:3])

def create_itinerary(trip_details: str) -> str:
    """Create final itinerary from all gathered information."""
    return f"""
    TRIP ITINERARY
    ==============
    {trip_details}
    
    Day 1: Arrival and city orientation
    Day 2: Major attractions
    Day 3: Cultural experiences and departure
    
    Total estimated budget: $1,500-2,000 per person
    """

# Create tools with clear orchestration hints
tools = [
    Tool(
        name="get_date",
        func=get_current_date,
        description="Get current date. Use FIRST to establish timeline."
    ),
    Tool(
        name="calculate_dates",
        func=calculate_next_month,
        description="Calculate travel dates for next month. Use AFTER getting current date."
    ),
    Tool(
        name="check_weather",
        func=lambda x: check_weather(*x.split("|")),
        description="Check weather. Input: 'location|dates'. Use AFTER establishing dates."
    ),
    Tool(
        name="search_flights",
        func=lambda x: search_flights(*x.split("|")),
        description="Search flights. Input: 'origin|destination|dates'. Can use PARALLEL with hotels."
    ),
    Tool(
        name="search_hotels",
        func=lambda x: search_hotels(*x.split("|")),
        description="Search hotels. Input: 'location|dates|nights'. Can use PARALLEL with flights."
    ),
    Tool(
        name="find_activities",
        func=lambda x: find_activities(x),
        description="Find activities for a location. Can use ANYTIME after location known."
    ),
    Tool(
        name="create_itinerary",
        func=create_itinerary,
        description="Create final itinerary. Use LAST after gathering all information."
    )
]

# Demonstrate orchestration sequence
print("TRAVEL PLANNING ORCHESTRATION")
print("=" * 60)
print("\nQuery: 'Plan a 3-day trip to Tokyo next month'\n")
print("EXPECTED ORCHESTRATION SEQUENCE:")
print("1. get_date() → Know current date")
print("2. calculate_dates() → Determine next month dates")
print("3. PARALLEL:")
print("   - check_weather('Tokyo|dates')")
print("   - search_flights('MyCity|Tokyo|dates')")
print("   - search_hotels('Tokyo|dates|3')")
print("   - find_activities('Tokyo')")
print("4. create_itinerary(all_gathered_info)")
print("\n✅ Tools designed for natural orchestration flow!")

# Test individual tools
print("\nTOOL EXECUTION SAMPLES:")
print("-" * 40)
current = get_current_date()
print(f"Current date: {current}")

dates = calculate_next_month()
print(f"Travel dates: {dates}")

weather = check_weather("Tokyo", dates)
print(f"Weather: {weather}")

flights = search_flights("New York", "Tokyo", dates)
print(f"Flights: {flights}")

activities = find_activities("Tokyo")
print(f"Activities: {activities}")
