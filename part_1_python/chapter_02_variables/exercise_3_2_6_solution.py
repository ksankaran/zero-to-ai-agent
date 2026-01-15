# Exercise 3: Social Media Bio Generator
# Create a formatted social media profile bio

# Solution:

print("=" * 40)
print("SOCIAL MEDIA BIO GENERATOR")
print("=" * 40)

# User information (simulating input)
name = "Alex Chen"
username = "alexcodes"
age = 28
city = "San Francisco"
job_title = "Software Developer"
hobby1 = "hiking"
hobby2 = "photography"
hobby3 = "cooking"
favorite_quote = "Code is poetry"

# Create formatted bio sections
header = f"@{username}"
tagline = f"{job_title} | {city}"
hobbies_line = f"Loves {hobby1}, {hobby2}, and {hobby3}"
quote_line = f'"{favorite_quote}"'

# Calculate some fun stats
years_until_30 = 30 - age
username_length = len(username)
total_bio_length = len(name) + len(tagline) + len(hobbies_line) + len(quote_line)

# Display the bio
print("\n" + "~" * 40)
print(f"{header:^40}")
print(f"{name:^40}")
print("~" * 40)
print(f"\n{tagline}")
print(f"{hobbies_line}")
print(f"\n{quote_line}")
print("\n" + "~" * 40)

# Display stats
print("\nBio Statistics:")
print(f"  Username length: {username_length} characters")
print(f"  Total bio length: {total_bio_length} characters")
print(f"  Years until 30: {years_until_30}")
print("=" * 40)
