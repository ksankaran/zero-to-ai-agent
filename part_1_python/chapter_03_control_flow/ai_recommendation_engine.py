# From: Zero to AI Agent, Chapter 3, Section 3.3
# ai_recommendation_engine.py
# Simplified version of how Netflix might recommend movies

user_age = int(input("Your age: "))
likes_action = input("Do you like action movies? (yes/no): ").lower() == "yes"
likes_comedy = input("Do you like comedy? (yes/no): ").lower() == "yes"
watched_marvel = input("Have you watched Marvel movies? (yes/no): ").lower() == "yes"
is_weekend = input("Is it weekend? (yes/no): ").lower() == "yes"

print("\n🎬 AI Recommendation Engine Results:")

# Complex recommendation logic
if user_age >= 13 and likes_action and watched_marvel:
    print("Recommended: The Latest Superhero Movie")
elif (likes_comedy and is_weekend) or (user_age < 18 and not likes_action):
    print("Recommended: Family Comedy Special")
elif user_age >= 18 and not is_weekend and likes_action:
    print("Recommended: Quick Action Thriller (90 minutes)")
else:
    print("Recommended: Trending Documentary Series")

# This is how real recommendation systems work - just with thousands of conditions!
