# From: Zero to AI Agent, Chapter 4, Section 4.5
# frozen_sets.py - Working with immutable sets

# Creating frozen sets
constants = frozenset([3.14159, 2.71828, 1.41421])
print(f"Mathematical constants: {constants}")

# Frozen sets can be dictionary keys (regular sets cannot!)
user_groups = {
    frozenset(["admin", "user"]): "Full Access",
    frozenset(["user"]): "Limited Access",
    frozenset(["guest"]): "Read Only"
}

current_user_groups = frozenset(["user"])
access_level = user_groups.get(current_user_groups, "No Access")
print(f"User access level: {access_level}")

# Frozen sets support all non-mutating operations
set1 = frozenset([1, 2, 3])
set2 = frozenset([2, 3, 4])

print(f"Union: {set1 | set2}")
print(f"Intersection: {set1 & set2}")
print(f"Difference: {set1 - set2}")

# But you can't modify them
# set1.add(4)  # This would raise an AttributeError
