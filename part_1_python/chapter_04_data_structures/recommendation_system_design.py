# From: Zero to AI Agent, Chapter 4, Section 4.6
# recommendation_system_design.py - Choosing the right data structures for a recommendation system

# CHOOSING DATA STRUCTURES FOR A RECOMMENDATION SYSTEM

# 1. User profiles - Need key-value lookup by user_id
#    → DICTIONARY
user_profiles = {
    "user123": {
        "name": "Alice",
        "joined": "2024-01-01"
    },
    "user456": {
        "name": "Bob",
        "joined": "2024-01-15"
    }
}

# 2. User interests - Need unique items per user
#    → DICTIONARY OF SETS
user_interests = {
    "user123": {"python", "ai", "web"},
    "user456": {"javascript", "web", "mobile"}
}

# 3. Content items - Need to iterate in order
#    → LIST OF DICTIONARIES
content = [
    {"id": "c1", "title": "Learn Python", "tags": {"python", "programming"}},
    {"id": "c2", "title": "Web Development", "tags": {"web", "javascript"}},
    {"id": "c3", "title": "AI Basics", "tags": {"ai", "python"}}
]

# 4. View history - Order matters for recency
#    → DICTIONARY OF LISTS
view_history = {
    "user123": ["c1", "c3"],  # Ordered by time
    "user456": ["c2"]
}

# 5. Cached recommendations - Fast lookup, immutable
#    → DICTIONARY WITH TUPLE VALUES
cached_recommendations = {
    "user123": ("c2",),  # Tuple of recommendations
    "user456": ("c1", "c3")
}

# Using our chosen structures effectively
print("Generating recommendations for user123:")

# Get user interests (SET operations)
interests = user_interests["user123"]

# Find unviewed content (SET operations)
viewed = set(view_history["user123"])

# Score each content item
recommendations = []
for item in content:
    content_id = item["id"]
    if content_id not in viewed:  # Fast SET lookup
        # Calculate relevance (SET intersection)
        relevance = len(interests & item["tags"])
        if relevance > 0:
            recommendations.append((content_id, relevance))

# Sort and display
recommendations.sort(key=lambda x: x[1], reverse=True)
print(f"Recommendations: {recommendations}")

print("\nData structure choices:")
print("- User profiles: Dictionary (fast lookup by ID)")
print("- User interests: Dict of sets (unique interests per user)")
print("- Content: List of dicts (ordered, detailed items)")
print("- View history: Dict of lists (ordered history per user)")
print("- Cached: Dict of tuples (immutable recommendations)")
