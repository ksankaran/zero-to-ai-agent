# Exercise 2: Logical Operations
# Combine conditions with and/or/not

# Solution:

# Driver requirements
age = 18
has_license = True
vision_test_passed = True
written_test_passed = False
insurance_valid = True

# Eligibility checks
can_drive = age >= 16 and has_license
safe_to_drive = can_drive and vision_test_passed
fully_legal = can_drive and insurance_valid
any_test_failed = not written_test_passed or not vision_test_passed

print("Driver Eligibility Checker")
print("=" * 40)
print("Age:", age)
print("Has license:", has_license)
print("Vision test passed:", vision_test_passed)
print("Written test passed:", written_test_passed)
print("Insurance valid:", insurance_valid)

print("\nEligibility Results:")
print("Can drive (age >= 16 AND has license):", can_drive)
print("Safe to drive (can drive AND vision passed):", safe_to_drive)
print("Fully legal (can drive AND insurance):", fully_legal)
print("Any test failed:", any_test_failed)

# Complex condition
all_requirements = (age >= 16 and has_license and 
                   vision_test_passed and written_test_passed and 
                   insurance_valid)
print("\nMeets ALL requirements:", all_requirements)
