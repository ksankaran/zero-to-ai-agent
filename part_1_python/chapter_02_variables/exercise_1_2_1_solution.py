# Exercise 1: Personal Info Tracker
# Create variables for your name, age, city, and whether you like pizza (True/False)
# Then print a sentence using all of them

# Solution:

# Create the variables
my_name = "Alice"
my_age = 25
my_city = "Seattle"
likes_pizza = True

# Print sentences using all variables
print("Hi! My name is", my_name)
print("I am", my_age, "years old")
print("I live in", my_city)
print("Do I like pizza?", likes_pizza)

# Alternative: Using f-strings (preview of what's coming!)
print(f"\nHello! I'm {my_name}, a {my_age}-year-old from {my_city}.")
print(f"Pizza lover? {likes_pizza}!")

# You could also create a full sentence
print("\nFull introduction:")
print("My name is", my_name, "and I'm", my_age, "years old.")
print("I live in", my_city, "and my pizza preference is:", likes_pizza)
