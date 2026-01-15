# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: constants_example.py

# Constants (use UPPERCASE by convention)
PI = 3.14159
GRAVITY = 9.8
MAX_PLAYERS = 4
GAME_TITLE = "Python Adventure"
API_KEY = "your-api-key-here"  # In real code, use environment variables!

def calculate_circle_area(radius):
    return PI * radius ** 2  # Using global constant PI

def calculate_fall_speed(time):
    return GRAVITY * time  # Using global constant GRAVITY

def display_welcome():
    print(f"Welcome to {GAME_TITLE}!")
    print(f"This game supports up to {MAX_PLAYERS} players")

# Constants make code more readable and maintainable
area = calculate_circle_area(5)
print(f"Area: {area:.2f}")

speed = calculate_fall_speed(3)
print(f"Speed after 3 seconds: {speed} m/s")

display_welcome()