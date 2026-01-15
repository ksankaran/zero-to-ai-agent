# From: Zero to AI Agent, Chapter 4, Section 4.6
# Exercise 3: Social Network Features
# Using the right data structure for each job (without functions)

print("=" * 40)
print("SOCIAL NETWORK FEATURES")
print("=" * 40)

# User friendships - DICTIONARY OF SETS (bidirectional, unique)
friendships = {
    "Alice": {"Bob", "Charlie", "Diana"},
    "Bob": {"Alice", "Charlie", "Eve"},
    "Charlie": {"Alice", "Bob", "Diana"},
    "Diana": {"Alice", "Charlie"},
    "Eve": {"Bob"}
}

# Hashtags - SET (unique tags)
trending_hashtags = {"#python", "#coding", "#ai", "#machinelearning"}

# Feed - LIST (chronological order matters)
feed = [
    {"user": "Alice", "post": "Learning Python! #python", "time": "10:00"},
    {"user": "Bob", "post": "AI is amazing #ai #machinelearning", "time": "10:05"},
    {"user": "Charlie", "post": "Coding all day #coding", "time": "10:10"}
]

# User metadata - DICTIONARY
user_metadata = {
    "Alice": {"joined": "2024-01-01", "posts": 45},
    "Bob": {"joined": "2024-02-01", "posts": 32},
    "Charlie": {"joined": "2024-01-15", "posts": 28}
}

# Find mutual friends between two users using set intersection
user1 = "Alice"
user2 = "Bob"
mutual_friends = friendships[user1] & friendships[user2]
print(f"Mutual friends of {user1} and {user2}: {mutual_friends}")

# Extract all hashtags from feed using set operations
post_tags = set()
for post in feed:
    words = post["post"].split()
    for word in words:
        if word.startswith("#"):
            post_tags.add(word)
print(f"All hashtags used in feed: {post_tags}")

# Find hashtags in posts that are also trending
matching_trending = post_tags & trending_hashtags
print(f"Hashtags matching trending: {matching_trending}")

# Find friends of friends (excluding direct friends and self)
user = "Alice"
friends_of_friends = set()
for friend in friendships[user]:
    for fof in friendships[friend]:
        if fof != user and fof not in friendships[user]:
            friends_of_friends.add(fof)
print(f"\nFriends-of-friends for {user}: {friends_of_friends}")

# Display feed in order
print("\nFeed (in chronological order):")
for post in feed:
    print(f"  [{post['time']}] {post['user']}: {post['post']}")

print("=" * 40)
