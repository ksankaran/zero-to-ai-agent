# Appendix A: Python Quick Reference

## Your Go-To Python Cheat Sheet

Welcome to your Python quick reference! This appendix is designed to be your trusty companion whenever you need a quick reminder of Python syntax, common patterns, or debugging strategies. Bookmark this section  -  you'll come back to it often!

Think of this as your Python "cheat sheet"  -  not for cheating, but for being efficient! Even experienced developers keep references handy. The best programmers aren't the ones who memorize everything; they're the ones who know where to find the answers quickly.

---- 

## A.1 Common Python Patterns and Idioms

Python has a distinctive style that experienced developers call "Pythonic." These patterns make your code cleaner, more readable, and more efficient. Here are the patterns you'll use most often.

### Variables and Assignment

```python
# Multiple assignment (swap values without temp variable)
a, b = b, a

# Unpack a list or tuple
first, second, third = [1, 2, 3]
name, age, city = ("Alice", 30, "NYC")

# Unpack with * (catch the rest)
first, *middle, last = [1, 2, 3, 4, 5]
# first = 1, middle = [2, 3, 4], last = 5

# Default values with or
name = user_input or "Anonymous"

# Ternary operator (if-else in one line)
status = "adult" if age >= 18 else "minor"
```

### String Operations

```python
# f-strings (the modern way to format strings)
name = "Alice"
age = 30
print(f"Hello, {name}! You are {age} years old.")
print(f"In 5 years: {age + 5}")  # Expressions work too!

# Common string methods
text = "  Hello, World!  "
text.strip()        # Remove whitespace: "Hello, World!"
text.lower()        # Lowercase: "  hello, world!  "
text.upper()        # Uppercase: "  HELLO, WORLD!  "
text.replace("World", "Python")  # Replace text
text.split(",")     # Split into list: ['  Hello', ' World!  ']

# Join a list into a string
words = ["Hello", "World"]
" ".join(words)     # "Hello World"
", ".join(words)    # "Hello, World"

# Check string content
"python" in "I love python"  # True
text.startswith("Hello")      # True
text.endswith("!")            # True
"123".isdigit()               # True
"abc".isalpha()               # True
```

### List Operations

```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
empty = []
repeated = [0] * 5           # [0, 0, 0, 0, 0]
from_range = list(range(5))  # [0, 1, 2, 3, 4]

# Accessing elements
numbers[0]      # First: 1
numbers[-1]     # Last: 5
numbers[1:3]    # Slice: [2, 3]
numbers[:3]     # First 3: [1, 2, 3]
numbers[3:]     # From index 3: [4, 5]
numbers[::2]    # Every 2nd: [1, 3, 5]
numbers[::-1]   # Reversed: [5, 4, 3, 2, 1]

# Modifying lists
numbers.append(6)      # Add to end: [1,2,3,4,5,6]
numbers.insert(0, 0)   # Insert at index: [0,1,2,3,4,5,6]
numbers.extend([7,8])  # Add multiple: [0,1,2,3,4,5,6,7,8]
numbers.remove(3)      # Remove first occurrence of 3
numbers.pop()          # Remove and return last item
numbers.pop(0)         # Remove and return item at index
numbers.clear()        # Remove all items

# Useful list operations
len(numbers)           # Length
sum(numbers)           # Sum of all elements
min(numbers)           # Smallest
max(numbers)           # Largest
sorted(numbers)        # Returns new sorted list
numbers.sort()         # Sorts in place
numbers.reverse()      # Reverses in place
numbers.count(3)       # Count occurrences
numbers.index(3)       # Find index of first occurrence
```

### List Comprehensions

List comprehensions are one of Python's most powerful features. They let you create lists in a single, readable line.

```python
# Basic pattern: [expression for item in iterable]
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# With condition: [expression for item in iterable if condition]
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# Transform strings
names = ["alice", "bob", "charlie"]
upper_names = [name.upper() for name in names]
# ["ALICE", "BOB", "CHARLIE"]

# Nested loops
pairs = [(x, y) for x in [1,2] for y in [3,4]]
# [(1,3), (1,4), (2,3), (2,4)]

# Dictionary comprehension
square_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Set comprehension
unique_lengths = {len(name) for name in names}
# {5, 3, 7} (order may vary)
```

### Dictionary Operations

```python
# Creating dictionaries
person = {"name": "Alice", "age": 30, "city": "NYC"}
empty = {}
from_pairs = dict([("a", 1), ("b", 2)])

# Accessing values
person["name"]              # "Alice" (raises KeyError if missing)
person.get("name")          # "Alice" (returns None if missing)
person.get("job", "Unknown") # "Unknown" (custom default)

# Modifying dictionaries
person["email"] = "alice@email.com"  # Add new key
person["age"] = 31                    # Update existing
person.update({"age": 32, "job": "Developer"})  # Update multiple
del person["city"]                    # Delete key
removed = person.pop("age")           # Remove and return

# Iterating
for key in person:                    # Iterate keys
    print(key)

for key, value in person.items():     # Iterate both
    print(f"{key}: {value}")

# Check if key exists
"name" in person    # True
"salary" in person  # False
```

### Loops and Iteration

```python
# Basic for loop
for item in [1, 2, 3]:
    print(item)

# Range patterns
for i in range(5):          # 0, 1, 2, 3, 4
for i in range(2, 5):       # 2, 3, 4
for i in range(0, 10, 2):   # 0, 2, 4, 6, 8
for i in range(5, 0, -1):   # 5, 4, 3, 2, 1

# enumerate - get index AND value
names = ["Alice", "Bob", "Charlie"]
for i, name in enumerate(names):
    print(f"{i}: {name}")
# 0: Alice, 1: Bob, 2: Charlie

# zip - iterate multiple lists together
names = ["Alice", "Bob"]
ages = [30, 25]
for name, age in zip(names, ages):
    print(f"{name} is {age}")

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# Loop control
for i in range(10):
    if i == 3:
        continue    # Skip this iteration
    if i == 7:
        break       # Exit the loop
    print(i)
```

### Functions

```python
# Basic function
def greet(name):
    return f"Hello, {name}!"

# Default parameters
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")           # "Hello, Alice!"
greet("Alice", "Hi")     # "Hi, Alice!"

# *args - accept any number of positional arguments
def sum_all(*numbers):
    return sum(numbers)

sum_all(1, 2, 3)         # 6
sum_all(1, 2, 3, 4, 5)   # 15

# **kwargs - accept any number of keyword arguments
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="NYC")

# Lambda functions (anonymous functions)
square = lambda x: x ** 2
add = lambda x, y: x + y

# Using lambdas with sorted
people = [{"name": "Bob", "age": 25}, {"name": "Alice", "age": 30}]
sorted_by_age = sorted(people, key=lambda p: p["age"])
sorted_by_name = sorted(people, key=lambda p: p["name"])
```

### File Operations

```python
# Reading files (always use 'with' - it closes automatically)
with open("file.txt", "r") as f:
    content = f.read()        # Read entire file

with open("file.txt", "r") as f:
    lines = f.readlines()     # Read as list of lines

with open("file.txt", "r") as f:
    for line in f:            # Read line by line (memory efficient)
        print(line.strip())

# Writing files
with open("file.txt", "w") as f:   # Overwrite
    f.write("Hello, World!\n")

with open("file.txt", "a") as f:   # Append
    f.write("New line\n")

# Working with JSON
import json

# Read JSON
with open("data.json", "r") as f:
    data = json.load(f)

# Write JSON
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Using pathlib (modern way)
from pathlib import Path

path = Path("data/file.txt")
path.exists()           # Check if exists
path.is_file()          # Is it a file?
path.is_dir()           # Is it a directory?
path.parent             # Parent directory
path.name               # Filename
path.suffix             # Extension (.txt)
path.read_text()        # Read file content
path.write_text("Hi")   # Write to file
path.mkdir(exist_ok=True)  # Create directory
```

### Error Handling

```python
# Basic try/except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# Catching multiple exceptions
try:
    value = int("abc")
except ValueError:
    print("Invalid number format")
except TypeError:
    print("Wrong type")

# Get the error message
try:
    risky_operation()
except Exception as e:
    print(f"Error: {e}")

# Full try/except/else/finally
try:
    file = open("data.txt")
    content = file.read()
except FileNotFoundError:
    print("File not found!")
else:
    print("File read successfully!")  # Runs if no exception
finally:
    print("Cleanup here")            # Always runs

# Common exceptions to know
# ValueError      - wrong value type
# TypeError       - wrong object type
# KeyError        - dict key not found
# IndexError      - list index out of range
# FileNotFoundError - file doesn't exist
# AttributeError  - attribute doesn't exist
# ImportError     - module not found
```

---- 

## A.2 Debugging Tips and Tricks

Bugs happen to everyone  -  even the best programmers spend significant time debugging. Here are proven strategies to find and fix problems quickly.

### Print Debugging (The Classic Approach)

Sometimes the simplest approach is the best. Strategic print statements can quickly reveal what's happening in your code.

```python
# Basic debugging prints
print(f"DEBUG: variable = {variable}")
print(f"DEBUG: type = {type(variable)}")
print(f"DEBUG: length = {len(variable)}")

# Track function entry/exit
def process_data(data):
    print(f"ENTER process_data: {data}")
    result = do_something(data)
    print(f"EXIT process_data: {result}")
    return result

# Track loop iterations
for i, item in enumerate(items):
    print(f"Loop {i}: processing {item}")
    # ... rest of loop

# Pro tip: Use a debug flag
DEBUG = True

def debug_print(*args):
    if DEBUG:
        print("DEBUG:", *args)
```

### Reading Error Messages

Python error messages are actually very helpful once you know how to read them. Here's how to decode them:

```python
# Example error traceback:
# Traceback (most recent call last):
#   File "script.py", line 10, in <module>
#     result = process(data)
#   File "script.py", line 5, in process
#     return data["key"]
# KeyError: 'key'

# How to read it:
# 1. Start at the BOTTOM - that's the actual error
# 2. The line above shows WHERE it happened
# 3. Work your way UP to see the call chain
```

**Common Error Messages Decoded:**

```python
# NameError: name 'x' is not defined
# → Variable doesn't exist (typo? wrong scope?)

# TypeError: 'str' object is not callable
# → You're trying to call a string like a function
# → Check: Did you overwrite a function name?

# IndentationError: unexpected indent
# → Mixing tabs and spaces, or wrong indentation level

# AttributeError: 'NoneType' object has no attribute 'x'
# → A function returned None when you expected something else

# ModuleNotFoundError: No module named 'x'
# → Package not installed: pip install x
```

### Using the VS Code Debugger

VS Code has a powerful built-in debugger that lets you pause your code and inspect variables. Here's how to use it:

- **Set a breakpoint:** Click in the left margin next to a line number (red dot appears)
- **Start debugging:** Press F5 or click Run → Start Debugging
- **Step through code:** F10 (step over), F11 (step into), Shift+F11 (step out)
- **Inspect variables:** Hover over any variable to see its value
- **Watch expressions:** Add variables to the Watch panel to monitor them
- **Debug console:** Type Python expressions while paused to test things

### Rubber Duck Debugging 🦆

This might sound silly, but it works! Explain your code out loud (to a rubber duck, a pet, or an imaginary friend). The act of explaining often reveals the bug.

Questions to ask yourself:

- What should this code do?
- What is it actually doing?
- What are my assumptions about the inputs?
- When did this last work?
- What changed since then?

### Common Bug Patterns to Check

```python
# 1. Off-by-one errors
for i in range(len(items)):     # Goes 0 to len-1
for i in range(1, len(items)):  # Skips first item!

# 2. Mutable default arguments
def bad(items=[]):      # BUG: same list reused!
def good(items=None):   # CORRECT
    items = items or []

# 3. Modifying list while iterating
for item in items:
    items.remove(item)    # BUG: skips items!

# CORRECT: iterate over a copy
for item in items[:]:     # [:] makes a copy
    items.remove(item)

# 4. = vs ==
if x = 5:    # SyntaxError (assignment)
if x == 5:   # Correct (comparison)

# 5. Variable shadowing
list = [1, 2, 3]    # Overwrites built-in list()!
str = "hello"       # Overwrites built-in str()!
# Avoid using built-in names as variables
```

---- 

## A.3 Performance Optimization Basics

Most of the time, you shouldn't worry about optimization  -  write clear code first. But when performance matters, here are the key strategies.

### The Golden Rule: Measure First!

Never optimize without measuring. What you think is slow often isn't the real bottleneck.

```python
import time

# Simple timing
start = time.time()
# ... your code ...
end = time.time()
print(f"Took {end - start:.4f} seconds")

# Reusable timer decorator
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    # ... code ...
```

### Choose the Right Data Structure

The biggest performance gains often come from using the right data structure for your needs.

```python
# Checking membership: set vs list
# List: O(n) - checks every element
# Set: O(1) - instant lookup

# SLOW: checking if item exists in list
allowed_users = ["alice", "bob", "charlie"]
if username in allowed_users:  # Slow for large lists

# FAST: checking if item exists in set
allowed_users = {"alice", "bob", "charlie"}
if username in allowed_users:  # Fast even for millions

# Looking up values: dict vs list of tuples
# SLOW
users = [("alice", 30), ("bob", 25)]
for name, age in users:
    if name == "bob":
        return age

# FAST
users = {"alice": 30, "bob": 25}
age = users["bob"]  # Instant lookup
```

### Avoid Common Slow Patterns

```python
# 1. String concatenation in loops
# SLOW: Creates new string each iteration
result = ""
for item in items:
    result += str(item)

# FAST: Use join
result = "".join(str(item) for item in items)

# 2. Repeated function calls
# SLOW: len() called every iteration
for i in range(len(items)):
    if i < len(items) - 1:
        # ...

# FAST: Store result once
n = len(items)
for i in range(n):
    if i < n - 1:
        # ...

# 3. Creating lists when you just need to iterate
# SLOW: Creates entire list in memory
squares = [x**2 for x in range(1000000)]
for s in squares:
    # ...

# FAST: Use generator (creates values on demand)
squares = (x**2 for x in range(1000000))
for s in squares:
    # ...
```

### Use Built-in Functions

Python's built-in functions are implemented in C and are much faster than equivalent Python code.

```python
# Use built-ins instead of loops
sum(numbers)        # Instead of manual loop
max(numbers)        # Instead of tracking max
min(numbers)        # Instead of tracking min
any(conditions)     # True if any is True
all(conditions)     # True if all are True

# Example: Check if any number is negative
# SLOW
has_negative = False
for n in numbers:
    if n < 0:
        has_negative = True
        break

# FAST
has_negative = any(n < 0 for n in numbers)
```

### Quick Tips Summary

- **Measure first:** Don't guess what's slow  -  time it
- **Use sets for membership:** O(1) vs O(n) for lists
- **Use dicts for lookups:** Instant access by key
- **Avoid string += in loops:** Use ''.join() instead
- **Use generators for large data:** () instead of [](#)
- **Prefer built-ins:** sum(), max(), min(), any(), all()
- **Cache expensive results:** Store computed values
- **Profile before optimizing:** Find the real bottleneck

---- 

## Final Notes

This quick reference covers the patterns you'll use most often. Keep it handy as you work through the book and build your AI agents!

Remember:

- **Write clear code first,** optimize later if needed
- **When stuck, print everything**  -  visibility beats guessing
- **Read error messages carefully**  -  they usually tell you what's wrong
- **Google is your friend**  -  every programmer uses it

Happy coding! 🐍