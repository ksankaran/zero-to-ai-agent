# From: Zero to AI Agent, Chapter 4, Section 4.6
# common_mistakes.py - Common mistakes and how to avoid them

# MISTAKE 1: Using lists for lookups (slow!)
# Bad:
users_list = ["alice", "bob", "charlie"]
if "charlie" in users_list:  # Has to check each item
    print("Found (slow way)")

# Good:
users_set = {"alice", "bob", "charlie"}
if "charlie" in users_set:  # Instant lookup
    print("Found (fast way)")

# MISTAKE 2: Using dictionaries when order matters
# Bad (in older Python):
steps_dict = {
    1: "Wash vegetables",
    2: "Cut vegetables",
    3: "Cook vegetables"
}
# Dictionary order wasn't guaranteed in older Python!

# Good:
steps_list = [
    "Wash vegetables",
    "Cut vegetables",
    "Cook vegetables"
]
print(f"Step 1: {steps_list[0]}")

# MISTAKE 3: Modifying a list while iterating
# Bad:
numbers = [1, 2, 3, 4, 5]
# This would cause problems:
# for n in numbers:
#     if n % 2 == 0:
#         numbers.remove(n)  # Dangerous!

# Good:
numbers = [1, 2, 3, 4, 5]
odd_numbers = []
for n in numbers:
    if n % 2 != 0:
        odd_numbers.append(n)
print(f"Odd numbers: {odd_numbers}")

# MISTAKE 4: Not using sets for uniqueness
# Bad:
seen = []
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
for item in data:
    if item not in seen:  # Slow for large lists
        seen.append(item)

# Good:
seen_set = set()
for item in data:
    seen_set.add(item)  # Automatically handles uniqueness
print(f"Unique items: {seen_set}")

# MISTAKE 5: Forgetting tuples can't be modified
# Bad:
config = ("localhost", 5432)
# config[0] = "remotehost"  # This would cause an error!

# Good:
config_list = ["localhost", 5432]  # If you need to modify
config_list[0] = "remotehost"
print(f"Modified config: {config_list}")

print("\nRemember: Choose the right tool for the job!")
