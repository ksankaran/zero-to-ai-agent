# From: Zero to AI Agent, Chapter 4, Section 4.6
# cheat_sheet.py - Quick reference guide for data structures

# LISTS - [1, 2, 3]
# ✅ Use when: order matters, need indices, duplicates OK, will modify
# ❌ Avoid for: fast lookups, unique items only, dictionary keys
# Big-O: Access O(1), Search O(n), Insert/Delete O(n)

example_list = [1, 2, 3, 4, 5]
print(f"List example: {example_list}")
print(f"  Access by index: {example_list[0]}")
print(f"  Can have duplicates: {[1, 1, 2, 2, 3]}")

# TUPLES - (1, 2, 3)
# ✅ Use when: data won't change, need dictionary keys, returning multiple values
# ❌ Avoid for: data that needs updates, sorting needed
# Big-O: Access O(1), Search O(n)

example_tuple = (1, 2, 3, 4, 5)
print(f"\nTuple example: {example_tuple}")
print(f"  Immutable - can't change")
print(f"  Can be dict key: {{('key', 'parts'): 'value'}}")

# DICTIONARIES - {"a": 1}
# ✅ Use when: key-value pairs, fast lookups, caching, JSON data
# ❌ Avoid for: ordered iteration (Python 3.6+ maintains order though), duplicate keys
# Big-O: Access/Insert/Delete O(1) average

example_dict = {"name": "Alice", "age": 30}
print(f"\nDictionary example: {example_dict}")
print(f"  Fast lookup: {example_dict['name']}")
print(f"  Key-value pairs")

# SETS - {1, 2, 3}
# ✅ Use when: uniqueness required, fast membership testing, set operations
# ❌ Avoid for: ordered data, indexed access, duplicate values needed
# Big-O: Add/Remove/Contains O(1) average

example_set = {1, 2, 3, 4, 5}
print(f"\nSet example: {example_set}")
print(f"  No duplicates: {1, 1, 2, 2, 3} becomes {set([1, 1, 2, 2, 3])}")
print(f"  Fast membership: 3 in {example_set} = {3 in example_set}")

# COMBINATIONS
print("\n" + "=" * 50)
print("Common Combinations:")
print("=" * 50)

# List of dicts: Records/rows of data
records = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
print(f"List of dicts: {records}")

# Dict of lists: Grouping similar items
groups = {"colors": ["red", "blue"], "sizes": ["S", "M", "L"]}
print(f"Dict of lists: {groups}")

# Dict of sets: Unique items per key
unique_groups = {"tags": {"python", "ai"}, "skills": {"coding", "design"}}
print(f"Dict of sets: {unique_groups}")

# List of tuples: Paired data, coordinates
coordinates = [(0, 0), (1, 1), (2, 2)]
print(f"List of tuples: {coordinates}")
