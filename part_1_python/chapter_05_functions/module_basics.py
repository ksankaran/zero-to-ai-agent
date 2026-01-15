# From: Zero to AI Agent, Chapter 5, Section 5.6
# File: module_basics.py

# Let's explore a module you've used before
import random

# Now we can use functions from the random module
dice_roll = random.randint(1, 6)
print(f"You rolled a {dice_roll}")

# Pick a random item from a list
colors = ["red", "blue", "green", "yellow"]
chosen_color = random.choice(colors)
print(f"Random color: {chosen_color}")

# Generate a random decimal between 0 and 1
random_float = random.random()
print(f"Random float: {random_float:.4f}")