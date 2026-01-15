# From: Zero to AI Agent, Chapter 6, Section 6.2
# Exercise 3 Solution: Score Tracker

"""
Score Tracker
Create a game score tracker using JSON.
"""

import json
import os

def load_scores():
    """Load high scores from file"""
    if os.path.exists("highscores.json"):
        try:
            with open("highscores.json", "r") as file:
                return json.load(file)
        except:
            return []
    return []

def save_scores(scores):
    """Save scores to file"""
    with open("highscores.json", "w") as file:
        json.dump(scores, file, indent=4)

def add_score(scores):
    """Add a new score"""
    name = input("Player name: ")
    try:
        score = int(input("Score: "))
        
        # Add new score
        scores.append({
            "name": name,
            "score": score
        })
        
        # Sort by score (highest first) and keep top 5
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)
        scores = scores[:5]
        
        save_scores(scores)
        print(f"✅ Score added for {name}!")
        
        return scores
    except ValueError:
        print("Score must be a number!")
        return scores

def display_leaderboard(scores):
    """Show top 5 scores"""
    print("\n🏆 HIGH SCORES 🏆")
    print("-" * 30)
    
    if not scores:
        print("No scores yet!")
    else:
        for i, entry in enumerate(scores, 1):
            print(f"{i}. {entry['name']}: {entry['score']}")

def main():
    scores = load_scores()
    
    while True:
        print("\n=== Score Tracker ===")
        print("1. Add new score")
        print("2. View leaderboard")
        print("3. Exit")
        
        choice = input("Choose (1-3): ")
        
        if choice == "1":
            scores = add_score(scores)
        elif choice == "2":
            display_leaderboard(scores)
        elif choice == "3":
            print("Thanks for playing! 🎮")
            break

if __name__ == "__main__":
    main()
