# Exercise 1: BMI Calculator
# Calculate Body Mass Index using the formula BMI = weight(kg) / height(m)²

# Solution:

# Store weight and height
weight_kg = 70  # Weight in kilograms
height_m = 1.75  # Height in meters

# Calculate BMI
# Formula: BMI = weight / (height * height)
bmi = weight_kg / (height_m ** 2)

# Round to 1 decimal place
bmi_rounded = round(bmi, 1)

# Display the result
print("BMI Calculator")
print("-" * 30)
print("Weight:", weight_kg, "kg")
print("Height:", height_m, "m")
print("Your BMI is:", bmi_rounded)

# Additional: BMI categories
print("\nBMI Categories:")
print("< 18.5: Underweight")
print("18.5-24.9: Normal weight")
print("25-29.9: Overweight")
print(">= 30: Obese")

# Alternative calculation showing step by step
print("\n--- Step by step ---")
height_squared = height_m * height_m
print("Height squared:", height_squared)
bmi_calc = weight_kg / height_squared
print("BMI calculation:", weight_kg, "/", height_squared, "=", bmi_calc)
