# From: Zero to AI Agent, Chapter 12, Section 12.6
# File: external_service_handling.py

from langchain_core.tools import Tool
import time
import random

# Simulate an unreliable external service
def unreliable_weather_api(city: str) -> dict:
    """Simulates an API that sometimes fails."""
    # 30% chance of failure
    if random.random() < 0.3:
        raise Exception("Service unavailable")
    # 20% chance of timeout
    if random.random() < 0.2:
        time.sleep(5)  # Simulate timeout
        raise TimeoutError("Request timed out")
    # Otherwise return data
    return {"city": city, "temp": 72, "conditions": "Sunny"}

def robust_weather_tool(city: str) -> str:
    """
    Weather tool with retry logic and fallbacks.
    """
    if not city:
        return "Error: City name required"
    
    # Try up to 3 times
    for attempt in range(3):
        try:
            # Set a timeout
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("API call timed out")
            
            # Note: signal doesn't work on Windows, this is for illustration
            # In production, use requests library with timeout parameter
            
            # Make the API call
            result = unreliable_weather_api(city)
            
            # Success! Format and return
            return f"Weather in {result['city']}: {result['temp']}°F, {result['conditions']}"
            
        except TimeoutError:
            if attempt < 2:  # Don't sleep on last attempt
                print(f"  Attempt {attempt + 1} timed out, retrying...")
                time.sleep(1)  # Brief pause before retry
            continue
            
        except Exception as e:
            if attempt < 2:
                print(f"  Attempt {attempt + 1} failed: {e}, retrying...")
                time.sleep(1)
            continue
    
    # All attempts failed - return graceful error
    return f"Error: Unable to get weather for {city}. Please try again later."

# Alternative: Fallback to a different service
def weather_with_fallback(city: str) -> str:
    """
    Try primary service, fallback to secondary if needed.
    """
    # Try primary service
    try:
        # Primary API call (simulated)
        if random.random() < 0.5:  # 50% failure rate
            raise Exception("Primary API failed")
        return f"Weather from PRIMARY: {city} is 72°F"
    except:
        # Fallback to secondary service
        try:
            # Secondary API call (simulated)
            if random.random() < 0.3:  # 30% failure rate
                raise Exception("Secondary API failed")
            return f"Weather from BACKUP: {city} is 70°F"
        except:
            # Both failed
            return f"Error: Weather services unavailable for {city}"

# Test the robust tool
print("TESTING EXTERNAL SERVICE HANDLING")
print("=" * 50)

tool = Tool(
    name="RobustWeather",
    func=robust_weather_tool,
    description="Get weather with retry logic"
)

print("\nTesting with retries (watch for retry messages):")
for i in range(5):
    result = tool.func("New York")
    print(f"Attempt {i+1}: {result}")
    print()
