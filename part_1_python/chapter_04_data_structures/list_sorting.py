# From: Zero to AI Agent, Chapter 4, Section 4.2
# list_sorting.py - Sorting and reversing lists

# Sorting numbers
prices = [29.99, 14.50, 39.99, 24.99, 19.99]
print("Original prices:", prices)

# sort() - Sorts the list IN PLACE (modifies the original)
prices.sort()
print("After sort() - ascending:", prices)

prices.sort(reverse=True)  # Sort in descending order
print("After sort(reverse=True):", prices)

# sorted() - Returns a NEW sorted list (doesn't modify original)
original = [5, 2, 8, 1, 9]
sorted_copy = sorted(original)
print(f"Original: {original}")  # Unchanged!
print(f"Sorted copy: {sorted_copy}")

# Sorting strings
words = ["python", "agent", "neural", "bot", "ai"]
words.sort()
print("Alphabetically sorted:", words)

# reverse() - Reverses the list IN PLACE
countdown = [1, 2, 3, 4, 5]
countdown.reverse()
print("Reversed countdown:", countdown)

# Advanced: Sorting with a key function
# Sort by length of string
names = ["Jo", "Alexander", "Bob", "Christina"]
names.sort(key=len)  # Sort by length
print("Sorted by length:", names)

# Sort ignoring case
mixed_case = ["apple", "Banana", "cherry", "Date"]
mixed_case.sort()  # Capital letters come first!
print("Default sort:", mixed_case)

mixed_case = ["apple", "Banana", "cherry", "Date"]
mixed_case.sort(key=str.lower)  # Ignore case
print("Case-insensitive sort:", mixed_case)
