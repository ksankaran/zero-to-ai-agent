# From: Zero to AI Agent, Chapter 6, Section 6.3
# File: 03_understanding_http.py


import requests
import json

print("📚 UNDERSTANDING HTTP\n")

# HTTP Status Codes (like response codes)
print("="*50)
print("HTTP STATUS CODES - What the API is telling you:")
print("="*50)
print("✅ 200 - OK: Everything worked!")
print("✅ 201 - Created: New resource created successfully")
print("⚠️  400 - Bad Request: You sent invalid data")
print("⚠️  401 - Unauthorized: You need to log in / bad API key")
print("⚠️  403 - Forbidden: You're not allowed to access this")
print("⚠️  404 - Not Found: That endpoint/resource doesn't exist")
print("⚠️  429 - Too Many Requests: Slow down! Rate limit hit")
print("❌ 500 - Server Error: The API is having problems")
print("❌ 503 - Service Unavailable: API is down for maintenance")

# Let's see these in action
print("\n" + "="*50)
print("SEEING STATUS CODES IN ACTION:")
print("="*50)

# Good request (200)
print("\n1. Good request (expecting 200):")
response = requests.get("https://httpbin.org/get")
print(f"   Status: {response.status_code} - {response.reason}")

# Bad request - wrong endpoint (404)
print("\n2. Wrong endpoint (expecting 404):")
response = requests.get("https://httpbin.org/this-doesnt-exist")
print(f"   Status: {response.status_code} - {response.reason}")

# Unauthorized (401)
print("\n3. Unauthorized (expecting 401):")
response = requests.get("https://httpbin.org/basic-auth/user/pass")
print(f"   Status: {response.status_code} - {response.reason}")

# HTTP Methods in action
print("\n" + "="*50)
print("HTTP METHODS - Different ways to talk to APIs:")
print("="*50)

base_url = "https://httpbin.org"

# GET - Retrieve data
print("\n📥 GET - Fetching data:")
response = requests.get(f"{base_url}/get", params={"key": "value"})
print(f"Status: {response.status_code}")
print(f"URL called: {response.url}")

# POST - Send data
print("\n📤 POST - Sending data:")
data = {"username": "pythonista", "score": 100}
response = requests.post(f"{base_url}/post", json=data)
if response.status_code == 200:
    result = response.json()
    print(f"Data sent: {result.get('json', {})}")
else:
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

# Headers - Additional information
print("\n📋 HEADERS - Extra information with requests:")
headers = {
    "User-Agent": "My Python Program",
    "Accept": "application/json",
    "Custom-Header": "Hello API!"
}
response = requests.get(f"{base_url}/headers", headers=headers)
if response.status_code == 200:
    result = response.json()
    print("Headers received by server:")
    for key, value in result['headers'].items():
        if key in ['User-Agent', 'Accept', 'Custom-Header']:
            print(f"  {key}: {value}")
else:
    print(f"Status: {response.status_code}")
