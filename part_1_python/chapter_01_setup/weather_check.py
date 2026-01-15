# weather_check.py
# From: Zero to AI Agent, Chapter 1, Section 1.3

import sys
import requests

print("=" * 50)
print("VIRTUAL ENVIRONMENT WEATHER CHECK")
print("=" * 50)

# Check if we're in a virtual environment
print("Checking virtual environment status...")
print(f"sys.prefix: {sys.prefix}")
print("")

# Make a simple request using the requests package
# This only works if requests is installed in your venv!
print("Fetching weather for London...")
response = requests.get("http://wttr.in/London?format=3")
print(response.text)

print("")
print("If you see weather above, your virtual environment works!")
print("The 'requests' package was successfully installed and used.")
print("=" * 50)
