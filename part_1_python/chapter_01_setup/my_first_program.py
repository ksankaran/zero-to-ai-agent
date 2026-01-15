# my_first_program.py
# From: Zero to AI Agent, Chapter 1, Section 1.5

import datetime
import sys
import platform

# Print a welcome banner
print("=" * 50)
print("   WELCOME TO PYTHON PROGRAMMING!")
print("=" * 50)

# Show when this program is running
current_time = datetime.datetime.now()
print(f"\n📅 Date: {current_time.strftime('%B %d, %Y')}")
print(f"⏰ Time: {current_time.strftime('%I:%M %p')}")

# Share some system information
print(f"\n💻 Computer Name: {platform.node()}")
print(f"🖥️  Operating System: {platform.system()} {platform.release()}")
print(f"🐍 Python Version: {sys.version.split()[0]}")

# A personal message
print("\n" + "=" * 50)
name = input("What's your name? ")
print(f"\nHello, {name}! 👋")
print("Welcome to the amazing world of Python programming!")
print("You're on your way to building AI agents!")
print("=" * 50)

# Show where Python is installed
print(f"\n📁 Python Location: {sys.executable}")

# Fun fact
import random
facts = [
    "Python was named after Monty Python, not the snake!",
    "Python was created in 1991 by Guido van Rossum.",
    "Python is used by Google, Netflix, and Instagram!",
    "Python can be used for AI, web development, and automation!",
    "The Zen of Python has 19 guiding principles for writing Python."
]
print(f"\n💡 Fun Fact: {random.choice(facts)}")

print("\n✨ Your development environment is ready for AI adventures!")