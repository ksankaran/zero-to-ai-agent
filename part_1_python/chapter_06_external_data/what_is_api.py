# From: Zero to AI Agent, Chapter 6, Section 6.3
# File: what_is_api.py

# This is what happens when you use an API:

# 1. YOU (the client) make a request:
#    "Hey weather service, what's the temperature in New York?"

# 2. THE API (the server) processes your request:
#    - Checks you're allowed to ask
#    - Finds the information
#    - Packages it nicely

# 3. THE API sends back a response:
#    "It's 72°F in New York, partly cloudy"

# APIs speak in HTTP - the same language web browsers use!
# Let's simulate this conversation:

def simulate_api_conversation():
    print("🌐 API CONVERSATION SIMULATION")
    print("="*50)
    
    # Your request
    print("YOU: GET https://api.weather.com/v1/location/new-york")
    print("     Headers: {'Authorization': 'your-api-key'}")
    
    print("\n⏳ API processing...")
    
    # API response (this would be JSON in real life)
    print("\nAPI RESPONSE:")
    print("Status: 200 OK")
    print("Body: {")
    print('  "location": "New York",')
    print('  "temperature": 72,')
    print('  "condition": "Partly Cloudy",')
    print('  "humidity": 65')
    print("}")
    
    print("\n✅ That's it! You asked, the API answered!")
    print("\n💡 Real APIs work exactly like this, just faster!")

simulate_api_conversation()

# Common API operations (like ordering from different sections of a menu):
print("\n" + "="*50)
print("📋 COMMON API OPERATIONS:")
print("="*50)
print("GET    - Fetch data (like reading)")
print("POST   - Send new data (like creating)")
print("PUT    - Update existing data (like editing)")
print("DELETE - Remove data (like deleting)")
print("PATCH  - Partial update (like fixing a typo)")
