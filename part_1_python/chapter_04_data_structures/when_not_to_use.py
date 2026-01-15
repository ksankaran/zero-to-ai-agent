# From: Zero to AI Agent, Chapter 4, Section 4.7
# when_not_to_use.py - When NOT to use list comprehensions

# TOO COMPLEX - Hard to read!
# Don't do this:
# result = [x if x > 0 else -x if x < 0 else 0 for x in numbers if x != 5]

# Better as a regular loop:
numbers = [-3, -1, 0, 1, 5, 7]
result = []
for x in numbers:
    if x != 5:
        if x > 0:
            result.append(x)
        elif x < 0:
            result.append(-x)
        else:
            result.append(0)
print("Result:", result)

# SIDE EFFECTS - Don't use comprehensions just for side effects
# Bad - using comprehension just to print (creates useless list):
# [print(x) for x in range(5)]  # Don't do this!

# Good - use a regular loop for side effects:
print("Printing with loop (correct way):")
for x in range(5):
    print(x, end=" ")
print()

# TOO LONG - If it doesn't fit on one line, use a loop
# Bad - too long to read easily:
# data = [complicated_expression(x) * another_function(x) / some_calculation(x) for x in very_long_iterable_name if complex_condition(x) and another_condition(x)]

# Good - break it up:
items = [1, 2, 3, 4, 5]
data = []
for x in items:
    if x > 2 and x < 5:  # condition1 and condition2
        value = x * 2  # expression
        data.append(value)
print("Clean loop result:", data)

print("\nRemember: Readability counts! If it's hard to read, use a regular loop.")
