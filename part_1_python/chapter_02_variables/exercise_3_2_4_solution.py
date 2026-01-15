# Exercise 3: Student Eligibility
# Build a student eligibility checker with multiple conditions

# Solution:

# Student data
gpa = 3.2
attendance_percentage = 85
completed_credits = 90
has_violations = False
community_service_hours = 25

# Eligibility criteria
min_gpa_honors = 3.5
min_gpa_pass = 2.0
min_attendance = 80
min_credits = 120
required_service_hours = 20

# Check various eligibility conditions
passes_gpa = gpa >= min_gpa_pass
qualifies_for_honors = gpa >= min_gpa_honors
good_attendance = attendance_percentage >= min_attendance
enough_credits = completed_credits >= min_credits
no_violations = not has_violations
sufficient_service = community_service_hours >= required_service_hours

# Graduation eligibility
can_graduate = (passes_gpa and good_attendance and 
                enough_credits and no_violations)

# Special recognition
special_recognition = (qualifies_for_honors and 
                      sufficient_service and 
                      no_violations)

print("Student Eligibility Report")
print("=" * 50)
print("Student Information:")
print(f"GPA: {gpa}")
print(f"Attendance: {attendance_percentage}%")
print(f"Credits completed: {completed_credits}/{min_credits}")
print(f"Has violations: {has_violations}")
print(f"Community service: {community_service_hours} hours")

print("\nEligibility Checks:")
print(f"Passes GPA requirement (>= {min_gpa_pass}):", passes_gpa)
print(f"Qualifies for honors (>= {min_gpa_honors}):", qualifies_for_honors)
print(f"Good attendance (>= {min_attendance}%):", good_attendance)
print(f"Enough credits (>= {min_credits}):", enough_credits)
print(f"No violations:", no_violations)
print(f"Sufficient service hours (>= {required_service_hours}):", sufficient_service)

print("\nFinal Determinations:")
print("Can graduate:", can_graduate)
print("Eligible for special recognition:", special_recognition)
