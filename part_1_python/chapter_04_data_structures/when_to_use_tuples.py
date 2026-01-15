# From: Zero to AI Agent, Chapter 4, Section 4.6
# when_to_use_tuples.py - When to choose tuples for your data

# 1. Data represents a single, unchangeable entity
rgb_red = (255, 0, 0)  # Color definition
database_config = ("localhost", 5432, "mydb", "readonly")

# 2. You need to use it as a dictionary key
location_data = {
    (40.7128, -74.0060): "New York",
    (51.5074, -0.1278): "London"
}
# Lists can't be dictionary keys, but tuples can!

# 3. Returning multiple values (conceptually)
# Calculate both area and perimeter
width, height = 10, 5
result = (width * height, 2 * (width + height))  # (area, perimeter)
area, perimeter = result

# 4. Protecting data from accidental changes
SYSTEM_CONSTANTS = (3.14159, 2.71828, 1.41421)
# No one can accidentally modify these

# 5. Representing fixed records
user_record = ("Alice", 30, "alice@example.com", True)  # Fixed structure

# Real-world TUPLE examples in AI:

# Model configuration (shouldn't change during runtime)
MODEL_CONFIG = ("gpt-3.5", 2048, 0.7, "production")
model, max_tokens, temperature, environment = MODEL_CONFIG

# Training metrics snapshot (immutable record)
epoch_results = (1, 0.85, 0.15, 42.3)  # (epoch, accuracy, loss, time)

# Fixed coordinate pairs for computer vision
bounding_box = ((100, 100), (200, 200))  # ((x1, y1), (x2, y2))

print("Tuple examples:")
print(f"RGB Red: {rgb_red}")
print(f"Database config: {database_config}")
print(f"Model: {model}, Max tokens: {max_tokens}")
print(f"Area: {area}, Perimeter: {perimeter}")
