# From: Zero to AI Agent, Chapter 5, Section 5.5
# File: lambda_sorting_pattern.py

# 1. SORTING - Sort by custom criteria
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78}
]

# Sort by grade (lambda tells Python what to sort by)
students.sort(key=lambda student: student["grade"])
print("Sorted by grade:")
for student in students:
    print(f"  {student['name']}: {student['grade']}")

# Sort by name length
students.sort(key=lambda student: len(student["name"]))
print("\nSorted by name length:")
for student in students:
    print(f"  {student['name']} ({len(student['name'])} letters)")