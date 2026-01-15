# From: Zero to AI Agent, Chapter 4, Section 4.3
# tuples_vs_lists.py - When to use tuples vs lists

# Use TUPLES when:
# 1. Data shouldn't change (coordinates, configuration, constants)
rgb_red = (255, 0, 0)  # Color values should be fixed
db_config = ("localhost", 5432, "mydb", "readonly")  # Database settings

# 2. You need dictionary keys
cache = {
    ("user", 123): "cached_data_1",
    ("post", 456): "cached_data_2"
}

# 3. Representing a single record/entity
person = ("Bob", 30, "Engineer")  # One person's data
point = (10, 20)  # One point in space

# Use LISTS when:
# 1. Data needs to change
shopping_cart = ["apples", "bread"]  # Will add/remove items
shopping_cart.append("milk")

# 2. You have a collection of similar items
temperatures = [22, 24, 23, 25, 21]  # Collection of readings
messages = []  # Will accumulate messages

# 3. You need list methods (sort, append, etc.)
scores = [85, 92, 78, 95]
scores.sort()  # Need to sort

# 4. Size will change
active_users = []  # Will grow and shrink
