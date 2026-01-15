# From: Zero to AI Agent, Chapter 6, Section 6.3
# File: 02_first_api_call.py


import requests  # First, install this: pip install requests
import json

print("🚀 YOUR FIRST API CALLS!\n")

# Example 1: Get a random joke
print("="*50)
print("Getting a random joke...")
print("="*50)

response = requests.get("https://official-joke-api.appspot.com/random_joke")

# Check if request was successful
if response.status_code == 200:
    joke = response.json()  # Parse JSON response
    print(f"\n🎭 Here's your joke:")
    print(f"Setup: {joke['setup']}")
    print(f"Punchline: {joke['punchline']}")
else:
    print(f"❌ Error: {response.status_code}")

# Example 2: Get random advice
print("\n" + "="*50)
print("Getting random advice...")
print("="*50)

response = requests.get("https://api.adviceslip.com/advice")

if response.status_code == 200:
    advice_data = response.json()
    advice = advice_data['slip']['advice']
    print(f"\n💡 Advice for you: {advice}")
else:
    print(f"❌ Error: {response.status_code}")

# Example 3: Get random user data (great for testing)
print("\n" + "="*50)
print("Getting random user data...")
print("="*50)

response = requests.get("https://randomuser.me/api/")

if response.status_code == 200:
    user_data = response.json()
    user = user_data['results'][0]
    
    print(f"\n👤 Random User:")
    print(f"Name: {user['name']['first']} {user['name']['last']}")
    print(f"Email: {user['email']}")
    print(f"Country: {user['location']['country']}")
    print(f"Age: {user['dob']['age']}")
else:
    print(f"❌ Error: {response.status_code}")

# Example 4: Get your IP address info
print("\n" + "="*50)
print("Getting your IP information...")
print("="*50)

response = requests.get("https://ipapi.co/json/")

if response.status_code == 200:
    ip_data = response.json()
    print(f"\n🌍 Your Connection Info:")
    print(f"IP: {ip_data.get('ip', 'Unknown')}")
    print(f"City: {ip_data.get('city', 'Unknown')}")
    print(f"Region: {ip_data.get('region', 'Unknown')}")
    print(f"Country: {ip_data.get('country_name', 'Unknown')}")
else:
    print(f"❌ Error: {response.status_code}")

print("\n🎉 Congratulations! You just talked to 4 different APIs!")
