# From: Zero to AI Agent, Chapter 6, Section 6.2
# File: nested_json.py

import json

# Complex nested structure (like from a real API)
api_response = {
    "status": "success",
    "data": {
        "user": {
            "id": 12345,
            "username": "coder",
            "profile": {
                "full_name": "Jane Coder",
                "bio": "Love Python and AI!",
                "location": {
                    "city": "San Francisco",
                    "country": "USA",
                    "coordinates": {
                        "lat": 37.7749,
                        "lng": -122.4194
                    }
                }
            },
            "stats": {
                "posts": 42,
                "followers": 1337,
                "following": 256
            }
        },
        "recent_posts": [
            {
                "id": 1,
                "title": "Learning JSON",
                "likes": 15,
                "comments": [
                    {"user": "friend1", "text": "Great post!"},
                    {"user": "friend2", "text": "Thanks for sharing!"}
                ]
            },
            {
                "id": 2,
                "title": "Python Tips",
                "likes": 23,
                "comments": [
                    {"user": "dev123", "text": "Helpful!"}
                ]
            }
        ]
    },
    "timestamp": "2024-01-15T10:30:00Z"
}

# Save this complex structure
with open("api_response.json", "w") as file:
    json.dump(api_response, file, indent=4)
print("✅ Saved complex nested JSON")

print("\n" + "="*50)
print("NAVIGATING NESTED JSON:\n")

# Accessing nested values
username = api_response["data"]["user"]["username"]
print(f"Username: {username}")

city = api_response["data"]["user"]["profile"]["location"]["city"]
print(f"City: {city}")

followers = api_response["data"]["user"]["stats"]["followers"]
print(f"Followers: {followers:,}")

# Working with lists in JSON
print(f"\nRecent posts: {len(api_response['data']['recent_posts'])}")
for post in api_response["data"]["recent_posts"]:
    print(f"  • '{post['title']}' - {post['likes']} likes")
    
# Going deeper - comments on first post
first_post_comments = api_response["data"]["recent_posts"][0]["comments"]
print(f"\nComments on first post:")
for comment in first_post_comments:
    print(f"  {comment['user']}: {comment['text']}")

# Safe navigation (avoiding KeyError)
print("\n" + "="*50)
print("SAFE NAVIGATION WITH .get():\n")

# This could crash if key doesn't exist:
# bad_access = api_response["data"]["user"]["missing_key"]  # KeyError!

# Safe approach with .get()
phone = api_response.get("data", {}).get("user", {}).get("phone", "Not provided")
print(f"Phone: {phone}")

# Getting coordinates safely
coords = api_response.get("data", {}).get("user", {}).get("profile", {}).get("location", {}).get("coordinates", {})
if coords:
    print(f"Location: ({coords.get('lat')}, {coords.get('lng')})")
else:
    print("Location not available")
