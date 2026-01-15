# From: Zero to AI Agent, Chapter 4, Section 4.4
# Exercise 2: Student Grade Manager

# Store students with grades
students = {
    "Alice": {"Math": 85, "Science": 92, "English": 78},
    "Bob": {"Math": 73, "Science": 68, "English": 81},
    "Charlie": {"Math": 90, "Science": 88, "English": 85}
}

# Add new student
students["Diana"] = {"Math": 95, "Science": 91, "English": 89}
print("Added Diana")

# Calculate averages
for name, grades in students.items():
    avg = sum(grades.values()) / len(grades)
    students[name]["average"] = avg
    print(f"{name}: Average = {avg:.1f}")

# Find top performer
top_student = max(students.items(), key=lambda x: x[1].get("average", 0))
print(f"\nTop performer: {top_student[0]} with {top_student[1]['average']:.1f}")

# Generate report card for specific student
student = "Alice"
print(f"\nReport Card for {student}:")
for subject, grade in students[student].items():
    if subject != "average":
        print(f"  {subject}: {grade}")
print(f"  Overall Average: {students[student]['average']:.1f}")

# List failing students (grade < 60)
print("\nStudents with failing grades:")
for name, grades in students.items():
    for subject, grade in grades.items():
        if subject != "average" and grade < 60:
            print(f"  {name} - {subject}: {grade}")
