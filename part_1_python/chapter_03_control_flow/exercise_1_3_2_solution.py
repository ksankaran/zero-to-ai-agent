# From: Zero to AI Agent, Chapter 3, Section 3.2
# Exercise 1: Number Range Checker
# Categorize numbers into different ranges

print("=" * 40)
print("NUMBER RANGE CHECKER")
print("=" * 40)

# Get the number from the user
number = float(input("Enter a number: "))

# Categorize using chained comparisons
if number < 0:
    category = "Negative"
    description = "Below zero!"
elif 0 <= number <= 10:
    category = "Small"
    description = "A tiny number!"
elif 11 <= number <= 100:
    category = "Medium"
    description = "A moderate value!"
elif 101 <= number <= 1000:
    category = "Large"
    description = "That's a big number!"
else:
    category = "Huge"
    description = "Astronomical!"

# Display results
print("")
print(f"Number: {number}")
print(f"Category: {category}")
print(f"Description: {description}")
print("=" * 40)
