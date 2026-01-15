# From: Zero to AI Agent, Chapter 3, Section 3.3
# Exercise 1: Eligibility Checker
# Check if someone is eligible for a special program

print("=" * 40)
print("PROGRAM ELIGIBILITY CHECKER")
print("=" * 40)

# Get user information
age = int(input("Enter your age: "))
employment_status = input("Are you employed? (yes/no): ").lower().strip()
student_status = input("Are you a full-time student? (yes/no): ").lower().strip()
has_fees = input("Do you have any outstanding fees? (yes/no): ").lower().strip()

# Check conditions
age_eligible = 18 <= age <= 65
work_or_study = employment_status == "yes" or student_status == "yes"
no_outstanding_fees = has_fees != "yes"

# Detailed feedback
print("")
print("ELIGIBILITY ASSESSMENT:")
print("-" * 40)

if age_eligible:
    print("[OK] Age requirement met (18-65)")
else:
    print(f"[X] Age requirement not met (you're {age}, need 18-65)")

if work_or_study:
    print("[OK] Employment/Student requirement met")
else:
    print("[X] Must be either employed OR a full-time student")

if no_outstanding_fees:
    print("[OK] No outstanding fees")
else:
    print("[X] Outstanding fees must be cleared")

# Final decision
print("")
print("FINAL DECISION:")
print("-" * 40)
if age_eligible and work_or_study and no_outstanding_fees:
    print("ELIGIBLE - You qualify for the program!")
else:
    print("NOT ELIGIBLE - Please review the requirements above")
print("=" * 40)
