# From: Zero to AI Agent, Chapter 4, Section 4.4
# Exercise 3: API Response Handler
# Handle nested API response data (without functions)

print("=" * 40)
print("API RESPONSE HANDLER")
print("=" * 40)

# Mock API responses (nested dictionaries)
api_responses = {
    "user_endpoint": {
        "status": 200,
        "data": {
            "user": {"id": 123, "name": "Alice", "email": "alice@example.com"}
        }
    },
    "posts_endpoint": {
        "status": 200,
        "data": {
            "posts": [
                {"id": 1, "title": "First Post"},
                {"id": 2, "title": "Second Post"}
            ]
        }
    }
}

# Extract user name using safe navigation with .get()
response = api_responses["user_endpoint"]
user_name = response.get("data", {}).get("user", {}).get("name", "Not found")
print(f"Extracted user name: {user_name}")

# Handle missing keys safely
missing_field = response.get("data", {}).get("user", {}).get("age", None)
if missing_field is None:
    print("Missing field 'age': Not found")
else:
    print(f"Age: {missing_field}")

# Get user email
user_email = response.get("data", {}).get("user", {}).get("email", "Not found")
print(f"User email: {user_email}")

# Count API calls by endpoint
print("\nCounting API calls...")
endpoints = ["user_endpoint", "user_endpoint", "posts_endpoint", "user_endpoint"]

api_call_count = {}
for endpoint in endpoints:
    api_call_count[endpoint] = api_call_count.get(endpoint, 0) + 1
print(f"API call counts: {api_call_count}")

# Simple cache for API responses
cache = {}

# Simulate API calls with caching
print("\nTesting cache...")
endpoints_to_fetch = ["user_endpoint", "user_endpoint", "posts_endpoint"]

for endpoint in endpoints_to_fetch:
    if endpoint not in cache:
        cache[endpoint] = api_responses.get(endpoint, {"status": 404})
        print(f"  Fetched {endpoint} from API")
    else:
        print(f"  Using cached {endpoint}")

# Generate usage statistics
print("\nUsage Statistics:")
print(f"  Unique endpoints called: {len(api_call_count)}")

total_calls = 0
for count in api_call_count.values():
    total_calls = total_calls + count
print(f"  Total API calls: {total_calls}")

# Find most used endpoint
most_used = ""
highest_count = 0
for endpoint, count in api_call_count.items():
    if count > highest_count:
        highest_count = count
        most_used = endpoint
print(f"  Most used endpoint: {most_used} ({highest_count} calls)")

print("=" * 40)
