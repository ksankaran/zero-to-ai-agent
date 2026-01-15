# basic_input.py
# From: Zero to AI Agent, Chapter 2, Section 2.6
# Learning to listen to users

# The simplest input
print("What is your name?")
name = input()
print(f"Hello, {name}!")

# Input with a prompt (much better!)
age = input("How old are you? ")
print(f"Wow, {age} is a great age!")

# Important: input() ALWAYS returns a string!
favorite_number = input("What's your favorite number? ")
print(f"Your favorite number is {favorite_number}")
print(f"Type of favorite_number: {type(favorite_number)}")  # It's a string!

# To do math, we need to convert
favorite_number = int(favorite_number)
print(f"Double your favorite number is {favorite_number * 2}")

# Multi-line prompts for clarity
prompt = """
Welcome to the Adventure Game!
You're standing at a crossroads.

Which way do you want to go?
1. North (to the mountains)
2. South (to the beach)
3. East (to the forest)
4. West (to the desert)

Enter your choice (1-4): """

choice = input(prompt)
print(f"You chose option {choice}. Adventure awaits!")
