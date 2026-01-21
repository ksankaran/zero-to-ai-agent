# Chapter 5: Functions and Modules

## System Check

Before we dive in, let's make sure you're all set up:

1. Open VS Code
2. Open your terminal (Terminal → New Terminal or `Ctrl+`` on Windows/Linux, `Cmd+`` on Mac)
3. Navigate to your project folder:

**On Windows:**
```bash
cd %USERPROFILE%\Desktop\ai_agents_complete
```

**On Mac/Linux:**
```bash
cd ~/Desktop/ai_agents_complete
```

4. Create a folder for this chapter and navigate into it:

**On Windows:**
```bash
mkdir part_1_python\chapter_05_functions
cd part_1_python\chapter_05_functions
```

**On Mac/Linux:**
```bash
mkdir -p part_1_python/chapter_05_functions
cd part_1_python/chapter_05_functions
```

5. Create a virtual environment for this chapter:

**On Windows:**
```bash
python -m venv venv
venv/Scripts/Activate.ps1
```

**On Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt. Perfect! You're ready to go.

---

## Troubleshooting

### Parameter and Argument Errors (Section 5.2)

**Error 1: Too few/many arguments**
```python
def greet(name, age):
    print(f"Hi {name}, you are {age}")

greet("Alice")  # Error! Missing 'age' argument
greet("Alice", 25, "Extra")  # Error! Too many arguments
```
**Fix:** Match the number of arguments to parameters
```python
greet("Alice", 25)  # Perfect!
```

**Error 2: Positional argument after keyword argument**
```python
greet(name="Alice", 25)  # Error! Positional after keyword
```
**Fix:** Put positional arguments first
```python
greet("Alice", age=25)  # Positional first, then keyword
# OR use all keywords:
greet(name="Alice", age=25)  # All keywords is fine
```

**Error 3: Forgetting self in class methods (preview)**
```python
# You'll see this later, but good to know:
class Dog:
    def bark(sound):  # Missing 'self'!
        print(sound)
```
**Fix:** We'll cover this in detail when we learn about classes!

### Scope-Related Errors (Section 5.4)

**Error 1: UnboundLocalError**
```python
count = 10
def increment():
    count = count + 1  # Error! Python thinks count is local
```
**Fix:** Use global keyword or pass as parameter
```python
# Option 1: global
def increment():
    global count
    count = count + 1

# Option 2: parameter and return (better!)
def increment(current_count):
    return current_count + 1
```

**Error 2: NameError - variable not defined**
```python
def create_user():
    username = "Alice"

create_user()
print(username)  # Error! username is local to function
```
**Fix:** Return the value
```python
def create_user():
    username = "Alice"
    return username

username = create_user()
print(username)  # Works!
```

**Error 3: Modifying mutable objects**
```python
def add_item(item, items=[]):  # Dangerous default!
    items.append(item)
    return items
```
**Fix:** Use None as default
```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

**Error 4: Shadowing built-in names**
```python
list = [1, 2, 3]  # Bad! Shadows built-in list()
# Now you can't use list() to convert things to lists!
```
**Fix:** Use different names
```python
my_list = [1, 2, 3]  # Better!
numbers = [1, 2, 3]  # Even better - descriptive!
```

### Lambda Pitfalls (Section 5.5)

**Issue 1: Trying to use statements**
```python
# Wrong - print is being used as a statement
bad = lambda x: print(x)
```
**Fix:** Return the value instead
```python
good = lambda x: x  # Just return it
# Or use a regular function if you need to print
```

**Issue 2: Lambda too complex**
```python
# Hard to read and understand
result = lambda x: x**2 if x > 0 else -x**2 if x < 0 else 0
```
**Fix:** Use a regular function
```python
def process_number(x):
    if x > 0:
        return x**2
    elif x < 0:
        return -x**2
    else:
        return 0
```

**Issue 3: Lambda in a loop (captures variable)**
```python
# Problem: all lambdas will use the final value of i
funcs = []
for i in range(3):
    funcs.append(lambda: i)

for f in funcs:
    print(f())  # Prints: 2, 2, 2 (not 0, 1, 2!)
```
**Fix:** Capture the value explicitly
```python
funcs = []
for i in range(3):
    funcs.append(lambda x=i: x)  # Capture i as default parameter

for f in funcs:
    print(f())  # Prints: 0, 1, 2 (correct!)
```

### Module Creation Issues (Section 5.7)

**Issue 1: ModuleNotFoundError when importing your module**
```python
import my_module  # Error: Module not found
```
**Fix:** Ensure the module file is in the same directory or in Python path
```python
# Check current directory
import os
print(os.getcwd())
# Make sure my_module.py is here
```

**Issue 2: Changes to module not showing**
```python
# You edited the module but changes don't appear
```
**Fix:** Restart Python or reload the module
```python
import importlib
importlib.reload(my_module)
```

**Issue 3: Circular imports**
```python
# module_a imports module_b
# module_b imports module_a
```
**Fix:** Restructure code to avoid circular dependencies

**Issue 4: Name conflicts**
```python
# Don't name your module the same as built-in modules
# math.py, random.py, etc. will cause problems!
```
**Fix:** Use unique, descriptive names for your modules

### Class Issues (Section 5.8)

**Issue 1: Forgetting `self` in method definition**
```python
def add_score(points):  # Wrong! Missing self
```
**Fix:** Always include `self` as the first parameter in methods

**Issue 2: Forgetting `self.` when accessing attributes**
```python
def greet(self):
    print(f"Hi, I'm {name}")  # Wrong! Should be self.name
```
**Fix:** Use `self.attribute_name` to access instance attributes

**Issue 3: Confusing the class with an instance**
```python
Player.add_score(100)  # Wrong! Player is the class
alice.add_score(100)   # Right! alice is an instance
```
**Fix:** Create an instance first, then call methods on it

---

## Practice Exercises

### Section 5.1

**Exercise 1: Temperature Facts**
Create a function called `show_temperature_facts()` that:
1. Prints the freezing point of water in Celsius and Fahrenheit
2. Prints the boiling point of water in Celsius and Fahrenheit
3. Prints a fun temperature fact

```python
# Try it yourself first!
# Then check the solution below
```

► `exercise_1_5_1_solution.py`

**Exercise 2: Daily Motivation**
Create a function called `daily_motivation()` that:
1. Prints a motivational quote
2. Shows today's date (hint: you learned about importing in earlier chapters!)
3. Prints an encouraging message about learning Python

```python
# Your code here
```

► `exercise_2_5_1_solution.py`

**Exercise 3: Code Stats Reporter**
Create a function called `report_progress()` that:
1. Creates a list of chapters you've completed (1 through 4)
2. Calculates how many chapters you've finished
3. Prints a progress report
4. Uses a loop to list each completed chapter

```python
# Give it a shot!
```

► `exercise_3_5_1_solution.py`

---

### Section 5.2

**Exercise 1: Temperature Converter with Parameters**
Create a function called `convert_temperature(value, from_unit, to_unit)` that:
1. Takes a temperature value and two units ('C', 'F', or 'K')
2. Converts between Celsius, Fahrenheit, and Kelvin
3. Prints the conversion
4. Handles at least C→F and F→C conversions

```python
# Try it yourself first!
# Hints:
# C to F: (C × 9/5) + 32
# F to C: (F - 32) × 5/9
```

► `exercise_1_5_2_solution.py`

**Exercise 2: Password Strength Checker**
Create a function called `check_password(password, min_length=8, require_numbers=True)` that:
1. Checks if password meets the minimum length
2. Optionally checks if it contains numbers
3. Prints whether the password is strong or weak
4. Uses default parameters

► `exercise_2_5_2_solution.py`

**Exercise 3: Shopping Cart Calculator**
Create a function called `calculate_total(items_list, tax_rate=0.08, discount_percent=0)` that:
1. Takes a list of prices
2. Applies optional discount
3. Adds tax
4. Prints itemized breakdown and total

► `exercise_3_5_2_solution.py`

---

### Section 5.3

**Exercise 1: Grade Calculator**
Create a function called `calculate_letter_grade(score)` that:
1. Takes a numerical score (0-100)
2. Returns the letter grade (A: 90-100, B: 80-89, C: 70-79, D: 60-69, F: below 60)
3. Returns None if the score is invalid (negative or above 100)

Then create a function `get_grade_statistics(scores)` that:
1. Takes a list of scores
2. Returns the average, highest score, lowest score, and most common letter grade

► `exercise_1_5_3_solution.py`

**Exercise 2: Username Generator**
Create a function called `generate_username(first_name, last_name, birth_year)` that:
1. Takes first name, last name, and birth year
2. Returns a username in format: first initial + last name + last 2 digits of birth year
3. Everything should be lowercase

Create another function `validate_username(username)` that:
1. Checks if username is 4-15 characters
2. Returns True if valid, False otherwise

► `exercise_2_5_3_solution.py`

**Exercise 3: Shopping Cart Calculator**
Create these functions:
1. `calculate_item_total(price, quantity)` - returns price * quantity
2. `apply_discount(total, discount_percent)` - returns discounted total
3. `calculate_tax(subtotal, tax_rate)` - returns tax amount
4. `calculate_final_total(items_list, discount_percent, tax_rate)` - uses all above functions

Where items_list is a list of tuples like: `[("apple", 1.50, 3), ("banana", 0.75, 6)]`

► `exercise_3_5_3_solution.py`

---

### Section 5.4

**Exercise 1: Bank Account System**
Create a banking system that properly manages scope:
1. Use a global constant for `MINIMUM_BALANCE = 10`
2. Create functions that take account data and return updated data (no global state)
3. Functions needed: `create_account(name, initial_balance)`, `deposit(account, amount)`, `withdraw(account, amount)`, `get_balance(account)`
4. The withdraw function should check against MINIMUM_BALANCE

► `exercise_1_5_4_solution.py`

**Exercise 2: Word Counter with Statistics**
Create a text analysis system:
1. NO global variables except constants
2. Create a function `analyze_text(text)` that returns a dictionary with word count, sentence count, and average word length
3. Create a function `compare_texts(text1, text2)` that uses `analyze_text` and returns which text is longer
4. All data should be passed via parameters and returns

► `exercise_2_5_4_solution.py`

**Exercise 3: Fix the Scope Issues**
Fix the scope problems in the provided code without using global variables.

► `exercise_3_5_4_solution.py`

---

### Section 5.5

**Exercise 1: List Operations**
Use lambda functions to:
1. Square all numbers in a list
2. Filter out negative numbers
3. Convert a list of strings to uppercase
4. Find all even numbers

► `exercise_1_5_5_solution.py`

**Exercise 2: Sorting Challenge**
Given a list of tuples `(name, age, salary)`:
1. Sort by age using lambda
2. Sort by salary (highest first) using lambda
3. Sort by name length using lambda

► `exercise_2_5_5_solution.py`

**Exercise 3: Text Processing**
Use lambda functions to create a text processing pipeline:
1. Remove short words (less than 3 characters)
2. Capitalize remaining words
3. Sort by word length

► `exercise_3_5_5_solution.py`

---

### Section 5.6

**Exercise 1: Date Calculator**
Create a program that:
1. Asks the user for their birthdate
2. Calculates their age in years, months, and days
3. Tells them how many days until their next birthday
4. Uses the `datetime` module

► `exercise_1_5_6_solution.py`

**Exercise 2: File Organizer**
Using the `os` module, create a function that:
1. Lists all files in the current directory
2. Groups them by extension (.txt, .py, .json, etc.)
3. Counts how many of each type
4. Uses `collections.Counter` for counting

► `exercise_2_5_6_solution.py`

**Exercise 3: Weather Data Processor**
Create a program that:
1. Uses `random` to generate fake temperature data for 7 days
2. Uses `statistics` module to calculate mean, median, and standard deviation
3. Uses `json` to save the data and statistics to a file

► `exercise_3_5_6_solution.py`

---

### Section 5.7

**Exercise 1: String Utilities Module**
Create a module called `string_utils.py` with functions for:
1. `capitalize_words(text)` - Capitalize first letter of each word
2. `remove_punctuation(text)` - Remove all punctuation
3. `count_vowels(text)` - Count vowels in text
4. `is_palindrome(text)` - Check if text is palindrome

Then create a test file that uses all functions.

► `exercise_1_5_7_solution.py`

**Exercise 2: Data Validation Module**
Create a module called `validators.py` with:
1. `validate_email(email)` - Check if email format is valid
2. `validate_phone(phone)` - Check if phone number is valid (10 digits)
3. `validate_password(password)` - Check password strength
4. A `ValidationResult` class that stores validation status and message

► `exercise_2_5_7_solution.py`

**Exercise 3: Mini Game Module**
Create a game module with:
1. A `Player` class with name, score, and level
2. Functions for `roll_dice()`, `flip_coin()`, `draw_card()`
3. A `Game` class that uses the Player class and functions
4. Make it playable when run directly

► `exercise_3_5_7_solution.py`

---

### Section 5.8

**Exercise 1: Book Class**
Create a `Book` class with:
- Attributes: title, author, pages, current_page
- Methods: `read(pages)` to advance current page, `get_progress()` to show percentage read
- A method to check if the book is finished

► `exercise_1_5_8_solution.py`

**Exercise 2: Shopping Cart**
Create a `ShoppingCart` class with:
- A list to store items (each item has name and price)
- Methods: `add_item(name, price)`, `remove_item(name)`, `get_total()`, `display()`
- A method to apply a discount percentage

► `exercise_2_5_8_solution.py`

**Exercise 3: Simple Chatbot**
Create a `Chatbot` class with:
- Attributes: name, mood, response_count
- A dictionary of responses for different keywords
- A `respond(message)` method that returns appropriate responses
- Mood that changes based on conversation

► `exercise_3_5_8_solution.py`

---

## Challenge Project: Personal Assistant Module

Time to put it all together! Create a personal assistant module that combines everything you've learned.

### Project Requirements:

Create a module called `personal_assistant.py` that includes:

1. **A PersonalAssistant class** with methods for:
   - Greeting the user (use time of day for appropriate greeting)
   - Managing a to-do list (add, remove, list tasks)
   - Setting reminders with timestamps
   - Generating passwords
   - Performing calculations

2. **Utility functions** for:
   - Text processing (clean, capitalize, word count)
   - Date/time operations (days until date, age calculator)
   - File operations (save/load assistant data)

3. **Make it interactive** when run directly:
   - Menu system for different features
   - Save state between sessions (using JSON)

4. **Documentation**:
   - Module docstring
   - Function/method docstrings
   - Comments for complex logic

### Starter Code:

> `part_1_python/chapter_05_functions/personal_assistant.py`

```python
"""Personal Assistant Module - manages tasks and more!"""

class PersonalAssistant:
    """Your personal Python assistant"""
    def __init__(self, name="PyAssistant"):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        """Add a task to the to-do list"""
        self.tasks.append(task)
        return f"Added: {task}"
```

### Bonus Challenges:
1. Add a weather feature using an API
2. Include a calculator with history
3. Add data persistence with JSON files
4. Create tests for your module
