# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: requests_module_example.py

# First install: pip install requests
import requests

# Make a simple web request
response = requests.get("https://api.github.com")
print(f"Status code: {response.status_code}")
print(f"Response headers: {response.headers['content-type']}")

# Get JSON data from an API
# Using a free API that doesn't require authentication
joke_response = requests.get("https://official-joke-api.appspot.com/random_joke")
if joke_response.status_code == 200:
    joke = joke_response.json()
    print(f"\nHere's a joke:")
    print(f"Setup: {joke['setup']}")
    print(f"Punchline: {joke['punchline']}")