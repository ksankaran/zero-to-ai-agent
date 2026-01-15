# From: Zero to AI Agent, Chapter 4, Section 4.5
# recommendation_system.py - Building a recommendation engine with sets

# Simple recommendation system using set operations

# User interests database
user_interests = {
    "alice": {"python", "ai", "machine-learning", "data-science"},
    "bob": {"javascript", "web", "react", "node"},
    "charlie": {"python", "ai", "deep-learning", "nlp"},
    "diana": {"python", "web", "django", "api"}
}

# Content tags database
content_items = {
    "article_1": {"python", "tutorial", "beginners"},
    "article_2": {"ai", "machine-learning", "python"},
    "article_3": {"javascript", "react", "tutorial"},
    "article_4": {"python", "django", "web"},
    "article_5": {"deep-learning", "nlp", "ai"},
    "video_1": {"python", "data-science", "pandas"},
    "video_2": {"node", "javascript", "api"}
}

# User viewing history
user_history = {
    "alice": {"article_1", "article_2"},
    "bob": {"article_3"},
    "charlie": set(),
    "diana": {"article_4"}
}

# Generate recommendations for each user
print("Generating recommendations:\n")
for username in user_interests:
    user_int = user_interests[username]
    viewed = user_history.get(username, set())
    
    # Find unviewed content
    all_content = set(content_items.keys())
    unviewed = all_content - viewed
    
    # Score each unviewed content
    recommendations = []
    for content_id in unviewed:
        content_tags = content_items[content_id]
        
        # Calculate relevance (number of matching tags)
        relevance = len(user_int & content_tags)
        
        if relevance > 0:
            recommendations.append((content_id, relevance))
    
    # Sort by relevance
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    # Display top 3 recommendations
    print(f"{username}'s recommendations:")
    top_recs = recommendations[:3]
    if top_recs:
        for content_id, score in top_recs:
            print(f"  {content_id}: relevance score {score}")
    else:
        print(f"  No recommendations found")
    print()

# Find similar users (Jaccard similarity)
print("Finding similar users:\n")
user_list = list(user_interests.keys())
for i in range(len(user_list)):
    for j in range(i + 1, len(user_list)):
        user1 = user_list[i]
        user2 = user_list[j]
        
        interests1 = user_interests[user1]
        interests2 = user_interests[user2]
        
        # Calculate Jaccard similarity
        intersection = len(interests1 & interests2)
        union = len(interests1 | interests2)
        
        if union > 0:
            similarity = intersection / union
            if similarity > 0.3:  # Threshold
                print(f"{user1} and {user2}: {similarity:.2f} similarity")
                print(f"  Common interests: {interests1 & interests2}")

# Popular content analysis
print("\nPopular content (viewed by multiple users):")
all_viewed = set()
for viewed_set in user_history.values():
    all_viewed |= viewed_set

view_counts = {}
for content_id in all_viewed:
    count = sum(1 for viewed in user_history.values() if content_id in viewed)
    if count > 1:
        view_counts[content_id] = count

for content_id, count in view_counts.items():
    print(f"  {content_id}: {count} views")
