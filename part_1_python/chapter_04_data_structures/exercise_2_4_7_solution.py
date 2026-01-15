# From: Zero to AI Agent, Chapter 4, Section 4.7
# Exercise 2: Grade Processing
# Process student records using comprehensions (without functions)

print("=" * 40)
print("GRADE PROCESSING")
print("=" * 40)

# Given student records
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78},
    {"name": "Diana", "grade": 95},
    {"name": "Eve", "grade": 88}
]

# Extract all names using list comprehension
all_names = [student["name"] for student in students]
print(f"All names: {all_names}")

# Get names of students with grades >= 90
high_achievers = [student["name"] for student in students if student["grade"] >= 90]
print(f"Students with grades >= 90: {high_achievers}")

# Create dictionary of name: grade pairs using dict comprehension
name_grade_dict = {student["name"]: student["grade"] for student in students}
print(f"Name-grade dictionary: {name_grade_dict}")

# Calculate letter grades using comprehension with conditional expression
letter_grades = {
    student["name"]: (
        'A' if student["grade"] >= 90 else
        'B' if student["grade"] >= 80 else
        'C'
    )
    for student in students
}
print(f"Letter grades: {letter_grades}")

# Create enhanced records with all information
enhanced_students = [
    {
        "name": student["name"],
        "grade": student["grade"],
        "letter": (
            'A' if student["grade"] >= 90 else
            'B' if student["grade"] >= 80 else
            'C'
        ),
        "honor_roll": student["grade"] >= 90
    }
    for student in students
]

print("\nEnhanced student records:")
for student in enhanced_students:
    print(f"  {student}")

print("=" * 40)
