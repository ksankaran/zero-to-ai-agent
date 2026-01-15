# From: Zero to AI Agent, Chapter 6, Section 6.2
# File: json_files.py

import json
import os

# Data for a simple game save system
game_save = {
    "player_name": "Hero",
    "current_level": 3,
    "position": {"x": 150, "y": 200},
    "inventory": [
        {"item": "sword", "quantity": 1, "equipped": True},
        {"item": "potion", "quantity": 5, "equipped": False},
        {"item": "gold", "quantity": 250, "equipped": False}
    ],
    "quests_completed": ["tutorial", "first_boss", "village_saved"],
    "play_time_seconds": 3600,
    "settings": {
        "difficulty": "normal",
        "sound_enabled": True,
        "auto_save": True
    }
}

# Save to a JSON file
print("Saving game...")
with open("save_game.json", "w") as file:
    json.dump(game_save, file, indent=4)
print("✅ Game saved to save_game.json")

# Load from the JSON file
print("\nLoading game...")
with open("save_game.json", "r") as file:
    loaded_save = json.load(file)

# Access the data
print(f"Welcome back, {loaded_save['player_name']}!")
print(f"You're on level {loaded_save['current_level']}")
print(f"You have {len(loaded_save['inventory'])} items")
print(f"Play time: {loaded_save['play_time_seconds'] // 60} minutes")

# Modify and re-save
print("\nPlaying for 5 more minutes...")
loaded_save['play_time_seconds'] += 300
loaded_save['current_level'] = 4
loaded_save['quests_completed'].append("dragon_defeated")

with open("save_game.json", "w") as file:
    json.dump(loaded_save, file, indent=4)
print("✅ Progress saved!")

# Show the actual file content
print("\n" + "="*50)
print("The actual JSON file looks like this:")
with open("save_game.json", "r") as file:
    print(file.read())
