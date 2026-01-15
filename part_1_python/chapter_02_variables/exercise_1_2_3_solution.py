# Exercise 1: String Formatter
# Create formatted name variations (full name, initials, email format)

# Solution:

# Store name components
first_name = "John"
last_name = "Smith"
middle_name = "Alexander"

# Create variations
full_name = first_name + " " + last_name
full_name_with_middle = first_name + " " + middle_name + " " + last_name

# Extract initials
first_initial = first_name[0]
last_initial = last_name[0]
middle_initial = middle_name[0]
initials = first_initial + last_initial
initials_full = first_initial + middle_initial + last_initial

# Create email format
email_username = first_name.lower() + "." + last_name.lower()
email = email_username + "@company.com"

# Display all variations
print("Name Formatter")
print("=" * 40)
print("First name:", first_name)
print("Middle name:", middle_name)
print("Last name:", last_name)
print("\nVariations:")
print("Full name:", full_name)
print("Full name with middle:", full_name_with_middle)
print("Initials:", initials)
print("Full initials:", initials_full)
print("Email:", email)

# Alternative: Using string methods
print("\n--- Using string methods ---")
print("Uppercase:", full_name.upper())
print("Title case:", full_name.title())
print("Lowercase:", full_name.lower())
