# From: Zero to AI Agent, Chapter 4, Section 4.3
# tuple_immutability.py - Understanding tuple immutability

# Lists are mutable (changeable)
list_scores = [85, 90, 78]
list_scores[1] = 95  # This works fine
print(f"Modified list: {list_scores}")

# Tuples are immutable (unchangeable)
tuple_scores = (85, 90, 78)
# tuple_scores[1] = 95  # This would cause an error!
# Uncomment the line above to see: TypeError: 'tuple' object does not support item assignment

# But wait - you CAN "modify" a tuple by creating a new one
original = (1, 2, 3)
# To "add" an element, create a new tuple
modified = original + (4,)  # Note the comma for single element!
print(f"Original: {original}")  # Still (1, 2, 3)
print(f"Modified: {modified}")  # New tuple (1, 2, 3, 4)

# To "change" an element, convert to list, modify, convert back
config = ("model_v1", 100, "active")
print(f"Original config: {config}")

# Need to update? Create a new tuple
temp_list = list(config)
temp_list[0] = "model_v2"
new_config = tuple(temp_list)
print(f"New config: {new_config}")
print(f"Original still unchanged: {config}")
