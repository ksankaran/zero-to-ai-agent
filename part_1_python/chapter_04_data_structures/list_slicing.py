# From: Zero to AI Agent, Chapter 4, Section 4.1
# list_slicing.py - Extracting portions of lists with slicing

# Let's work with a dataset of temperatures (in Celsius)
temperatures = [20, 22, 25, 23, 26, 28, 30, 29, 27, 24, 21, 19]
print("All temperatures:", temperatures)

# Basic slicing
first_three = temperatures[0:3]   # Items at index 0, 1, 2 (not 3!)
print("First three temps:", first_three)

# If you omit the start, it defaults to 0
first_four = temperatures[:4]     # Same as [0:4]
print("First four temps:", first_four)

# If you omit the end, it goes to the end of the list
from_index_6 = temperatures[6:]   # From index 6 to the end
print("From index 6 onward:", from_index_6)

# Get everything (make a copy)
all_temps = temperatures[:]       # Copies the entire list
print("Copy of all temps:", all_temps)

# Using step to skip items
every_other = temperatures[::2]   # Every 2nd item
print("Every other temp:", every_other)

# Reverse the list using step -1
reversed_temps = temperatures[::-1]
print("Reversed:", reversed_temps)

# Combine start, end, and step
morning_temps = temperatures[1:7:2]  # Index 1 to 6, every 2nd item
print("Select morning temps:", morning_temps)
