# From: Zero to AI Agent, Chapter 4, Section 4.6
# combining_structures.py - Combining data structures for maximum power

# 1. LIST OF DICTIONARIES - Perfect for records
users = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35}
]

# Easy to iterate
for user in users:
    print(f"{user['name']} is {user['age']} years old")

# 2. DICTIONARY OF LISTS - Perfect for grouping
students_by_grade = {
    "A": ["Alice", "Amy", "Anna"],
    "B": ["Bob", "Bill", "Betty"],
    "C": ["Charlie", "Carl"]
}

# Easy to access groups
a_students = students_by_grade["A"]

# 3. DICTIONARY OF SETS - Perfect for unique groupings
user_permissions = {
    "admin": {"read", "write", "delete", "modify"},
    "editor": {"read", "write", "modify"},
    "viewer": {"read"}
}

# Check permissions
if "delete" in user_permissions.get("editor", set()):
    print("Editor can delete")
else:
    print("Editor cannot delete")

# 4. LIST OF TUPLES - Perfect for paired data
coordinates = [
    (10, 20),
    (30, 40),
    (50, 60)
]
for x, y in coordinates:
    print(f"Point at ({x}, {y})")

# 5. DICTIONARY OF DICTIONARIES - Perfect for nested data
company_data = {
    "employees": {
        "alice": {"role": "developer", "salary": 70000},
        "bob": {"role": "designer", "salary": 65000}
    },
    "departments": {
        "engineering": {"head": "alice", "budget": 500000},
        "design": {"head": "bob", "budget": 200000}
    }
}

# 6. SET OF TUPLES - Perfect for unique pairs
edges = {
    ("A", "B"),
    ("B", "C"),
    ("A", "C")
}
print(f"Graph has {len(edges)} edges")

print("\nCombining structures examples:")
print(f"Number of users: {len(users)}")
print(f"A students: {a_students}")
print(f"Admin permissions: {user_permissions['admin']}")
print(f"Alice's role: {company_data['employees']['alice']['role']}")
