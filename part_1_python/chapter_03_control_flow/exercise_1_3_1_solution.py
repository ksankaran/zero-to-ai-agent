# From: Zero to AI Agent, Chapter 3, Section 3.1
# Exercise 1: Grade Calculator
# Convert numerical score to letter grade with encouraging messages

print("=" * 40)
print("GRADE CALCULATOR")
print("=" * 40)

# Get the score from the user
score = float(input("Enter your numerical score (0-100): "))

# Determine the letter grade and message
if score >= 90:
    grade = "A"
    message = "Excellent work! You're a superstar!"
elif score >= 80:
    grade = "B"
    message = "Great job! Keep up the good work!"
elif score >= 70:
    grade = "C"
    message = "Good effort! You're getting there!"
elif score >= 60:
    grade = "D"
    message = "Keep working hard! You can improve!"
else:
    grade = "F"
    message = "Don't give up! Every expert was once a beginner."

# Display the results
print("")
print(f"Score: {score:.1f}")
print(f"Grade: {grade}")
print(f"Message: {message}")
print("=" * 40)
