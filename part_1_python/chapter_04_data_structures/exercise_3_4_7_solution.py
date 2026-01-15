# From: Zero to AI Agent, Chapter 4, Section 4.7
# Exercise 3: Number Processing

# Given numbers range
numbers = range(1, 21)

# Create a list of all even numbers
even_numbers = [n for n in numbers if n % 2 == 0]
print(f"Even numbers: {even_numbers}")

# Create a list of squares of odd numbers
odd_squares = [n**2 for n in numbers if n % 2 != 0]
print(f"Squares of odd numbers: {odd_squares}")

# Create dictionary where keys are numbers and values are "even" or "odd"
even_odd_dict = {n: "even" if n % 2 == 0 else "odd" for n in numbers}
print(f"Even/odd dictionary: {even_odd_dict}")

# Create list of tuples (number, square, cube) for numbers 1-10
number_tuples = [(n, n**2, n**3) for n in range(1, 11)]
print("\nNumber tuples (number, square, cube):")
for tup in number_tuples:
    print(f"  {tup}")

# Bonus: All together - comprehensive number analysis
number_analysis = [
    {
        "number": n,
        "square": n**2,
        "cube": n**3,
        "type": "even" if n % 2 == 0 else "odd",
        "divisible_by_3": n % 3 == 0
    }
    for n in range(1, 11)
]
print("\nComprehensive number analysis:")
for analysis in number_analysis:
    print(f"  {analysis}")
