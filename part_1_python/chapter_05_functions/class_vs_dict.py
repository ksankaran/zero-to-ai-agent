# From: Zero to AI Agent, Chapter 5, Section 5.8
# class_vs_dict.py - Comparing classes and dictionaries

# Using a dictionary
player_dict = {
    "name": "Alice",
    "score": 0,
    "level": 1
}
# No built-in way to add methods
# Easy to make typos: player_dict["scroe"] = 100  # Oops!

print("Using dictionary:")
print(f"Name: {player_dict['name']}")
print(f"Score: {player_dict['score']}")


# Using a class
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.level = 1

    def level_up(self):
        self.level += 1
        print(f"{self.name} is now level {self.level}!")

    def add_score(self, points):
        self.score += points


print("\nUsing class:")
player = Player("Alice")
player.add_score(100)
player.level_up()  # Methods are built-in!
print(f"Name: {player.name}")
print(f"Score: {player.score}")
print(f"Level: {player.level}")
