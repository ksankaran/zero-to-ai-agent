# From: Zero to AI Agent, Chapter 4, Section 4.3
# tuple_accessing.py - Accessing and unpacking tuple elements

# AI model configuration tuple
model_config = ("gpt-3", 175, "billion", 96, 12288, 2048)
# (name, size, unit, layers, hidden_size, context_length)

# Indexing works exactly like lists
model_name = model_config[0]
num_layers = model_config[3]
context = model_config[-1]  # Negative indexing works too!

print(f"Model: {model_name}")
print(f"Layers: {num_layers}")
print(f"Context length: {context}")

# Slicing works the same way
size_info = model_config[1:3]  # Get size and unit
print(f"Size info: {size_info}")

# You can loop through tuples
print("Configuration details:")
for item in model_config:
    print(f"  - {item}")

# Unpacking - this is SUPER useful with tuples!
point = (3, 7)
x, y = point  # Unpacks the tuple into separate variables
print(f"x = {x}, y = {y}")

# Unpacking with AI example
response = ("success", "Hello! How can I help?", 0.92)
status, message, confidence = response
print(f"Status: {status}")
print(f"Message: {message}")
print(f"Confidence: {confidence}")

# You can even use * to grab multiple elements
numbers = (1, 2, 3, 4, 5, 6, 7)
first, *middle, last = numbers
print(f"First: {first}")
print(f"Middle: {middle}")  # This becomes a list!
print(f"Last: {last}")
