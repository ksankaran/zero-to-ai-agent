# From: Zero to AI Agent, Chapter 4, Section 4.7
# transforming_data.py - Real-world examples of data transformation

# Example 1: Processing user input
user_inputs = ["  Hello  ", "WORLD ", " python", "  AI  "]

# Clean and lowercase all inputs
cleaned = [text.strip().lower() for text in user_inputs]
print("Cleaned inputs:", cleaned)  # ['hello', 'world', 'python', 'ai']

# Example 2: Extracting data
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]

# Get all names
names = [user["name"] for user in users]
print("Names:", names)  # ['Alice', 'Bob', 'Charlie']

# Get names of users over 30
adults = [user["name"] for user in users if user["age"] > 30]
print("Over 30:", adults)  # ['Charlie']

# Example 3: File extensions
files = ["photo.jpg", "document.pdf", "image.png", "script.py", "data.csv"]

# Get only image files
images = [f for f in files if f.endswith((".jpg", ".png"))]
print("Images:", images)  # ['photo.jpg', 'image.png']

# Example 4: Converting temperatures
celsius = [0, 20, 30, 100]
fahrenheit = [c * 9/5 + 32 for c in celsius]
print("Fahrenheit:", fahrenheit)  # [32.0, 68.0, 86.0, 212.0]
