# Chapter 2: Python Basics - Variables and Data Types

## System Check

Before we dive in, let's make sure you're all set up:

1. Open VS Code
2. Open your terminal (Terminal → New Terminal or ``Ctrl+``` on Windows/Linux, ``Cmd+``` on Mac)
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
mkdir part_1_python\chapter_02_variables
cd part_1_python\chapter_02_variables
```

**On Mac/Linux:**
```bash
mkdir -p part_1_python/chapter_02_variables
cd part_1_python/chapter_02_variables
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

### Section 2.1: Variables

> **Error: "SyntaxError: invalid decimal literal"**
> This happens when you start a variable name with a number. Remember: variable names must start with a letter or underscore!
>
> **Error: "SyntaxError: invalid syntax"**
> Check for spaces or hyphens in your variable name. Use underscores instead: `user_name` not `user-name` or `user name`

> **Error: "NameError: name 'xyz' is not defined"**
> This means you're trying to use a variable that doesn't exist yet. Check for:
> - Typos (remember, Python is case-sensitive!)
> - Using a variable before creating it
> - Forgetting quotes around text
>
> **Quick fix:** Make sure you create the variable with `=` before trying to use it!

### Section 2.2: Numbers

> **Weird decimal results?**
> If you see results like 0.30000000000000004 instead of 0.3, don't worry! This is normal floating-point behavior. Solutions:
> - Use `round(number, 2)` to round to 2 decimal places
> - Use formatting: `f"{number:.2f}"` when displaying
> - For money, consider working in cents (integers)

---

## Practice Exercises

### Section 2.1

**Exercise 1: Personal Info Tracker**

Create variables to store your personal information and display them.

Requirements:
1. Create variables for your name, age, city, and whether you like pizza (True/False)
2. Print your name and age on one line
3. Print your city on another line
4. Print your pizza preference
5. Create a full introduction sentence using all variables

Test your solution with different values to make sure it works!

► `part_1_python/chapter_02_variables/exercise_1_2_1_solution.py`

**Exercise 2: Shopping Calculator**

Build a simple shopping calculator for computer equipment.

Requirements:
1. Create variables for keyboard ($79.99), mouse ($45.50), and monitor ($299.99)
2. Calculate the subtotal (sum of all items)
3. Calculate tax amount (8% of subtotal)
4. Calculate the final total (subtotal + tax)
5. Display all values with clear labels

Bonus: Try to format the output to look like a real receipt!

► `part_1_python/chapter_02_variables/exercise_2_2_1_solution.py`

**Exercise 3: Variable Swap Challenge**

Figure out how to swap the values of two variables.

Starting code:
```python
first_item = "coffee"
second_item = "tea"
# Your code here to swap them
```

Requirements:
1. Start with the given variables
2. Swap their values so first_item contains "tea" and second_item contains "coffee"
3. Print the values before and after swapping
4. Try to find at least two different methods

Hint: You might need a third variable for the classic approach!

► `part_1_python/chapter_02_variables/exercise_3_2_1_solution.py`

### Section 2.2

**Exercise 1: BMI Calculator**

Calculate Body Mass Index using the formula BMI = weight(kg) / height(m)²

Requirements:
1. Store weight in kilograms (e.g., 70)
2. Store height in meters (e.g., 1.75)
3. Calculate BMI using the formula
4. Round the result to 1 decimal place
5. Print the BMI value with a descriptive message

► `part_1_python/chapter_02_variables/exercise_1_2_2_solution.py`

**Exercise 2: Alien Age Calculator**

Calculate your age on different planets in our solar system!

Requirements:
1. Store your Earth age (e.g., 25)
2. Calculate your age on Mercury (Earth years / 0.24)
3. Calculate your age on Venus (Earth years / 0.62)
4. Calculate your age on Mars (Earth years / 1.88)
5. Calculate your age on Jupiter (Earth years / 11.86)
6. Display all ages with 1 decimal place

► `part_1_python/chapter_02_variables/exercise_2_2_2_solution.py`

**Exercise 3: Time Calculator**

Convert seconds into hours, minutes, and seconds format.

Requirements:
1. Start with total seconds (e.g., 7439)
2. Calculate hours using floor division
3. Calculate remaining minutes
4. Calculate remaining seconds
5. Display in format: "X hours, Y minutes, Z seconds"

► `part_1_python/chapter_02_variables/exercise_3_2_2_solution.py`

### Section 2.3

**Exercise 1: String Formatter**

Create formatted name variations (full name, initials, email format).

Requirements:
1. Store first, middle, and last names in variables
2. Create full name by concatenating
3. Extract initials (first letter of each name)
4. Create email format (firstname.lastname@company.com)
5. Display all variations with labels

► `part_1_python/chapter_02_variables/exercise_1_2_3_solution.py`

**Exercise 2: Mad Libs Story Generator**

Create a silly story by filling in blanks with different words!

Requirements:
1. Create variables for: adjective, animal, verb, food, place, number
2. Build a multi-line story using f-strings
3. Insert your variables into the story template
4. Display the complete silly story
5. Show the total story length using len()

► `part_1_python/chapter_02_variables/exercise_2_2_3_solution.py`

**Exercise 3: Receipt Formatter**

Build a formatted receipt with aligned columns.

Requirements:
1. Store item names, prices, and quantities
2. Calculate totals for each item
3. Calculate subtotal, tax, and grand total
4. Format output with aligned columns
5. Use appropriate decimal formatting for money

► `part_1_python/chapter_02_variables/exercise_3_2_3_solution.py`

### Section 2.4

**Exercise 1: Boolean Comparisons**

Create boolean variables from various comparisons.

Requirements:
1. Check if age makes someone an adult (>= 18)
2. Check if age is in teen range (13-19)
3. Verify if a password matches
4. Check if temperature is comfortable (68-76)
5. Display all results with descriptive labels

► `part_1_python/chapter_02_variables/exercise_1_2_4_solution.py`

**Exercise 2: Logical Operations**

Combine conditions using and, or, not operators.

Requirements:
1. Check if someone can drive (age and license)
2. Check if it's safe to drive (multiple conditions)
3. Check if any requirement is missing
4. Create complex eligibility conditions
5. Display results clearly

► `part_1_python/chapter_02_variables/exercise_2_2_4_solution.py`

**Exercise 3: Student Eligibility**

Build an eligibility checker with multiple conditions.

Requirements:
1. Check GPA requirements for graduation
2. Verify attendance percentage
3. Check credit completion
4. Combine conditions for graduation eligibility
5. Check special recognition criteria

► `part_1_python/chapter_02_variables/exercise_3_2_4_solution.py`

### Section 2.5

**Exercise 1: Type Detective**

Identify types and convert between them.

Requirements:
1. Check the type of various values
2. Convert integers to float, string, and boolean
3. Convert strings to appropriate numeric types
4. Handle boolean conversions correctly
5. Display types before and after conversion

► `part_1_python/chapter_02_variables/exercise_1_2_5_solution.py`

**Exercise 2: Unit Converter**

Convert between different measurement units using type conversion.

Requirements:
1. Store values as strings (simulating user input)
2. Convert string inputs to float
3. Convert miles to kilometers (× 1.60934)
4. Convert pounds to kilograms (× 0.453592)
5. Convert Fahrenheit to Celsius ((F - 32) × 5/9)
6. Display converted values with appropriate formatting

► `part_1_python/chapter_02_variables/exercise_2_2_5_solution.py`

**Exercise 3: Receipt Calculator**

Clean up messy price strings and calculate totals.

Requirements:
1. Store prices as strings with $ symbols (e.g., "$4.99")
2. Use replace() to remove the $ symbol
3. Convert cleaned strings to float
4. Calculate subtotal, tax, and total
5. Display a formatted receipt with tip suggestions

► `part_1_python/chapter_02_variables/exercise_3_2_5_solution.py`

### Section 2.6

**Exercise 1: Movie Night Calculator**

Calculate the total cost of a movie night with professional formatting.

Requirements:
1. Store ticket price, popcorn price, and drink price
2. Store quantities for each item
3. Calculate item totals, subtotal, tax, and grand total
4. Calculate cost per person
5. Display as a formatted receipt with aligned columns

► `part_1_python/chapter_02_variables/exercise_1_2_6_solution.py`

**Exercise 2: Personal Info Card**

Create a formatted information card.

Requirements:
1. Collect personal information (name, age, etc.)
2. Format as a professional card
3. Use alignment for clean columns
4. Include borders/separators
5. Display contact information neatly

► `part_1_python/chapter_02_variables/exercise_2_2_6_solution.py`

**Exercise 3: Social Media Bio Generator**

Create a formatted social media profile bio.

Requirements:
1. Store user info: name, username, city, job title, hobbies
2. Create formatted bio sections using f-strings
3. Center-align the header with username and name
4. Display hobbies and a favorite quote
5. Calculate and show bio statistics (character counts)

► `part_1_python/chapter_02_variables/exercise_3_2_6_solution.py`

### Section 2.7

**Exercise 1: Commented Recipe Calculator**

Create a well-documented recipe scaling program.

Requirements:
1. Add a header block describing the program
2. Document the original recipe amounts with comments
3. Explain the scaling factor calculation
4. Comment each scaled ingredient calculation
5. Use section separators to organize the code

► `part_1_python/chapter_02_variables/exercise_1_2_7_solution.py`

**Exercise 2: Self-Documenting Code**

Improve variable names to eliminate need for comments.

Requirements:
1. Replace cryptic variable names
2. Use descriptive function names
3. Define named constants
4. Make code readable without comments
5. Add minimal strategic comments

► `part_1_python/chapter_02_variables/exercise_2_2_7_solution.py`

**Exercise 3: Savings Goal Calculator**

Create a well-documented savings projection program.

Requirements:
1. Add a program header explaining its purpose
2. Create a configuration section with named constants
3. Document each financial calculation clearly
4. Organize code into logical sections with headers
5. Explain the meaning of calculated values

► `part_1_python/chapter_02_variables/exercise_3_2_7_solution.py`
