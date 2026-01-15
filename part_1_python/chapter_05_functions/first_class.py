# From: Zero to AI Agent, Chapter 5, Section 5.8
# first_class.py - Your first class example

class Player:
    """A player in our game"""

    def __init__(self, name):
        # These are ATTRIBUTES - data that belongs to each player
        self.name = name
        self.score = 0
        self.level = 1

    def add_score(self, points):
        # This is a METHOD - a function that belongs to the class
        self.score += points
        print(f"{self.name} earned {points} points!")


# Create players from the blueprint
alice = Player("Alice")
bob = Player("Bob")

# Each player has their own data
alice.add_score(100)
bob.add_score(50)

print(f"{alice.name}: {alice.score} points")  # Alice: 100 points
print(f"{bob.name}: {bob.score} points")      # Bob: 50 points
