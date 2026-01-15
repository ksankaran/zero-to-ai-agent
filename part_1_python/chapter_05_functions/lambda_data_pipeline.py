# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_data_pipeline.py

# Sample data: user activity logs
activities = [
    {"user": "Alice", "action": "login", "timestamp": 1000},
    {"user": "Bob", "action": "purchase", "timestamp": 1005},
    {"user": "Alice", "action": "logout", "timestamp": 1010},
    {"user": "Charlie", "action": "login", "timestamp": 1015},
    {"user": "Bob", "action": "logout", "timestamp": 1020},
    {"user": "Alice", "action": "purchase", "timestamp": 1025},
]

# Using lambdas to analyze the data

# 1. Filter: Get only purchase actions
purchases = list(filter(lambda a: a["action"] == "purchase", activities))
print(f"Purchases: {len(purchases)}")

# 2. Map: Extract just usernames from purchases
purchasers = list(map(lambda a: a["user"], purchases))
print(f"Users who purchased: {purchasers}")

# 3. Sort: Order all activities by timestamp
activities.sort(key=lambda a: a["timestamp"])
print("\nActivities in order:")
for activity in activities:
    print(f"  {activity['timestamp']}: {activity['user']} - {activity['action']}")

# 4. Complex: Find unique users
unique_users = list(set(map(lambda a: a["user"], activities)))
print(f"\nUnique users: {unique_users}")