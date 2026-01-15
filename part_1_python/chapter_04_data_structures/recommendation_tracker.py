# From: Zero to AI Agent, Chapter 4, Section 4.2
# recommendation_tracker.py - Simple recommendation system

# Recommendation system using dictionaries and lists
# Track what items users have viewed and liked

# Our data storage
users_data = {
    "alice": {
        "viewed": ["item1", "item2", "item3"],
        "liked": ["item1", "item3"],
        "recommendations": []
    },
    "bob": {
        "viewed": ["item2", "item4"],
        "liked": ["item4"],
        "recommendations": []
    }
}

# All available items in our system
all_items = ["item1", "item2", "item3", "item4", "item5", "item6"]

# Generate recommendations for each user
for username in users_data:
    user = users_data[username]
    
    # Find items they haven't viewed yet
    not_viewed = []
    for item in all_items:
        if item not in user["viewed"]:
            not_viewed.append(item)
    
    # Simple recommendation: items not viewed yet
    user["recommendations"] = not_viewed[:3]  # Top 3 recommendations
    
    print(f"\n{username}'s profile:")
    print(f"  Viewed: {user['viewed']}")
    print(f"  Liked: {user['liked']}")
    print(f"  Recommendations: {user['recommendations']}")

# Find popular items (liked by multiple users)
all_liked_items = []
for username in users_data:
    all_liked_items.extend(users_data[username]["liked"])

print("\n=== Popular Items ===")
for item in all_items:
    like_count = all_liked_items.count(item)
    if like_count > 0:
        print(f"  {item}: {like_count} likes")

# Find users with similar interests
print("\n=== Similar Users ===")
user_list = list(users_data.keys())
for i in range(len(user_list)):
    for j in range(i + 1, len(user_list)):
        user1 = user_list[i]
        user2 = user_list[j]
        
        # Find common liked items
        liked1 = users_data[user1]["liked"]
        liked2 = users_data[user2]["liked"]
        
        common_likes = []
        for item in liked1:
            if item in liked2:
                common_likes.append(item)
        
        if common_likes:
            print(f"  {user1} and {user2} both like: {common_likes}")
