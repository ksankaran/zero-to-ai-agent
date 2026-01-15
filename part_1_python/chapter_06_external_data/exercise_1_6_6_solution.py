# From: Zero to AI Agent, Chapter 6, Section 6.6
# Exercise 1 Solution: Student Grade Tracker

"""
Student Grade Tracker
Create a program that manages student grades in CSV.
"""

import csv
from pathlib import Path

def create_sample_grades():
    """Create sample grades file"""
    grades = [
        ['name', 'subject', 'grade'],
        ['Alice', 'Math', '85'],
        ['Alice', 'Science', '90'],
        ['Bob', 'Math', '75'],
        ['Bob', 'Science', '80'],
        ['Carol', 'Math', '95'],
        ['Carol', 'Science', '88']
    ]
    
    with open('grades.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(grades)
    print("✅ Created sample grades.csv")

def add_grade():
    """Add a new grade"""
    name = input("Student name: ")
    subject = input("Subject: ")
    grade = input("Grade: ")
    
    # Append to CSV
    with open('grades.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, subject, grade])
    
    print(f"✅ Added grade for {name}")

def calculate_averages():
    """Calculate average grade per student"""
    if not Path('grades.csv').exists():
        print("No grades file found!")
        return
    
    # Read all grades
    student_grades = {}
    
    with open('grades.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name']
            grade = float(row['grade'])
            
            if name not in student_grades:
                student_grades[name] = []
            student_grades[name].append(grade)
    
    # Calculate and display averages
    print("\n📊 Student Averages:")
    results = []
    
    for name, grades in student_grades.items():
        average = sum(grades) / len(grades)
        print(f"  {name}: {average:.1f}")
        results.append([name, f"{average:.1f}"])
    
    # Save to new file
    with open('averages.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'average'])
        writer.writerows(results)
    
    print("\n✅ Saved to averages.csv")

def main():
    print("=== Student Grade Tracker ===")
    
    # Create sample if doesn't exist
    if not Path('grades.csv').exists():
        create_sample_grades()
    
    while True:
        print("\n1. Add grade")
        print("2. Calculate averages")
        print("3. Exit")
        
        choice = input("Choose (1-3): ")
        
        if choice == '1':
            add_grade()
        elif choice == '2':
            calculate_averages()
        elif choice == '3':
            break
    
    print("Good luck with your studies! 📚")

if __name__ == "__main__":
    main()
