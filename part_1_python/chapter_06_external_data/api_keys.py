# From: Zero to AI Agent, Chapter 6, Section 6.3
# File: 04_api_keys.py


import requests
import os

print("🔑 WORKING WITH API KEYS\n")

# IMPORTANT: Never put API keys directly in code!
# Bad example (DON'T DO THIS):
# api_key = "sk-1234567890abcdef"  # NEVER DO THIS!

# Good example (DO THIS):
print("="*50)
print("SAFE API KEY PRACTICES:")
print("="*50)

# Method 1: Environment variables (BEST for production)
print("\n1️⃣ Using environment variables:")
print("   Set in terminal: export MY_API_KEY='your-key-here'")
print("   Or in .env file (with python-dotenv)")

# Simulated environment variable
os.environ['DEMO_API_KEY'] = 'demo-key-12345'  # Just for demo
api_key = os.environ.get('DEMO_API_KEY')
print(f"   Retrieved key: {api_key[:10]}..." if api_key else "   No key found")

# Method 2: Config file (Good for development)
print("\n2️⃣ Using a config file:")
config = {
    "api_key": "your-key-here",
    "api_secret": "your-secret-here"
}

# Save config (in real life, don't commit this file!)
import json
with open("config.json", "w") as f:
    json.dump(config, f)
print("   Config saved to config.json")

# Load config
with open("config.json", "r") as f:
    loaded_config = json.load(f)
print(f"   Loaded key: {loaded_config['api_key'][:10]}...")

# Method 3: Input prompt (Good for scripts)
print("\n3️⃣ Prompting for key:")
# api_key = input("   Enter your API key: ")  # Uncomment in real use

# Example: Using API key in requests
print("\n" + "="*50)
print("USING API KEYS IN REQUESTS:")
print("="*50)

# Different ways APIs expect keys:

# 1. In headers (most common)
headers_auth = {
    "Authorization": f"Bearer {api_key}",
    "X-API-Key": api_key  # Some APIs use this instead
}
print("1. Header authentication:")
print(f"   Authorization: Bearer {api_key[:10]}...")

# 2. In query parameters
params_auth = {
    "api_key": api_key,
    "other_param": "value"
}
print("\n2. Query parameter authentication:")
print(f"   https://api.example.com/data?api_key={api_key[:10]}...")

# 3. In request body (less common)
body_auth = {
    "api_key": api_key,
    "request_data": "your data"
}
print("\n3. Body authentication:")
print("   Included in POST request body")

# Demo with a real API that uses API keys (NASA's API - free!)
print("\n" + "="*50)
print("REAL EXAMPLE - NASA API (Free key: 'DEMO_KEY'):")
print("="*50)

nasa_api_key = "DEMO_KEY"  # NASA provides this for testing
url = "https://api.nasa.gov/planetary/apod"
params = {"api_key": nasa_api_key}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"\n🚀 NASA Astronomy Picture of the Day:")
    print(f"Title: {data['title']}")
    print(f"Date: {data['date']}")
    print(f"URL: {data['url']}")
    print(f"Explanation: {data['explanation'][:200]}...")
else:
    print(f"❌ Error: {response.status_code}")

# Clean up
os.remove("config.json")
print("\n💡 Remember: Keep your API keys secret and safe!")
