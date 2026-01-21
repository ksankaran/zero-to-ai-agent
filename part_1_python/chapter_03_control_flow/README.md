# Chapter 3: Control Flow - Teaching Your Programs to Think and Decide

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
mkdir part_1_python\chapter_03_control_flow
cd part_1_python\chapter_03_control_flow
```

**On Mac/Linux:**
```bash
mkdir -p part_1_python/chapter_03_control_flow
cd part_1_python/chapter_03_control_flow
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

You should see `(venv)` at the beginning of your terminal prompt. Perfect!

---

## Practice Exercises

### Section 3.1

**Exercise 1: Grade Calculator**
Create a program that converts a numerical score to a letter grade:
- 90-100: A
- 80-89: B
- 70-79: C
- 60-69: D
- Below 60: F

Add encouraging messages for each grade level!

► `part_1_python/chapter_03_control_flow/exercise_1_3_1_solution.py`

**Exercise 2: AI Agent Mood Simulator**
Create a simple AI assistant that responds differently based on the user's mood:
- If happy: share a joke
- If sad: offer encouragement
- If tired: suggest a break
- If excited: celebrate with them
- For any other mood: provide a general positive message

► `part_1_python/chapter_03_control_flow/exercise_2_3_1_solution.py`

### Section 3.2

**Exercise 1: Number Range Checker**
Create a program that takes a number and tells the user if it's:
- Negative (less than 0)
- Small (0-10)
- Medium (11-100)
- Large (101-1000)
- Huge (greater than 1000)

Use comparison operators and chained comparisons where appropriate.

► `part_1_python/chapter_03_control_flow/exercise_1_3_2_solution.py`

**Exercise 2: Password Validator**
Build a password strength checker that:
- Checks if password length is at least 8 characters
- Ensures password is not "password" or "12345678"
- Verifies password doesn't equal the username
- Gives specific feedback for each failure

► `part_1_python/chapter_03_control_flow/exercise_2_3_2_solution.py`

### Section 3.3

**Exercise 1: Eligibility Checker**
Create a program that checks if someone is eligible for a special program. They must meet ALL these conditions:
- Age between 18 and 65 (use `and` with comparisons)
- Either employed OR a full-time student (use `or`)
- NOT have any outstanding fees (use `not`)

Give clear feedback about which conditions they meet or don't meet.

► `part_1_python/chapter_03_control_flow/exercise_1_3_3_solution.py`

**Exercise 2: Smart Alarm System**
Build an alarm system that triggers when:
- Motion detected AND it's nighttime, OR
- Window opened AND nobody is home, OR
- Temperature is above 100°F (fire risk)

The system should also have a silent mode that overrides all alarms when enabled.

► `part_1_python/chapter_03_control_flow/exercise_2_3_3_solution.py`

### Section 3.4

**Exercise 1: Countdown Timer**
Create a countdown timer that:
- Asks the user for a starting number
- Counts down to 0
- Prints "Blast off!" at the end
- Shows the countdown in a nice format (e.g., "T-minus 10 seconds")

► `part_1_python/chapter_03_control_flow/exercise_1_3_4_solution.py`

**Exercise 2: Character Frequency Counter**
Write a program that:
- Takes a string from the user
- Counts how many times each vowel appears
- Shows statistics for consonants vs vowels
- Handles both uppercase and lowercase

► `part_1_python/chapter_03_control_flow/exercise_2_3_4_solution.py`

### Section 3.5

**Exercise 1: Number Guessing Game**
Create a number guessing game that:
- Generates a random number between 1 and 100
- Keeps asking for guesses until the user gets it right
- Tells them if their guess is too high or too low
- Counts the number of attempts
- Congratulates them when they win

► `part_1_python/chapter_03_control_flow/exercise_1_3_5_solution.py`

**Exercise 2: Input Accumulator**
Build a program that:
- Keeps asking for numbers until the user types "done"
- Calculates the sum of all numbers entered
- Shows the average at the end
- Handles invalid input gracefully (non-numbers)
- Shows how many valid numbers were entered

► `part_1_python/chapter_03_control_flow/exercise_2_3_5_solution.py`

### Section 3.6

**Exercise 1: Search and Stop**
Create a program that:
- Has a "secret word" stored in the program
- Gives the user 5 attempts to guess it
- Uses `break` to exit early if they guess correctly
- Uses `continue` to skip empty guesses
- Shows how many attempts they used (or if they failed)

► `part_1_python/chapter_03_control_flow/exercise_1_3_6_solution.py`

**Exercise 2: Menu System with Pass**
Build a menu system that:
- Shows options: 1) Calculate, 2) Convert, 3) Analyze, 4) Quit
- Implements Calculate (add two numbers)
- Uses `pass` as placeholder for Convert and Analyze
- Uses `break` to exit when user chooses Quit
- Uses `continue` for invalid menu choices

► `part_1_python/chapter_03_control_flow/exercise_2_3_6_solution.py`

### Section 3.7

**Exercise 1: Multiplication Table Generator**
Create a program that:
- Asks for a table size (e.g., 5 for a 5x5 table)
- Uses nested loops to generate the multiplication table
- Formats the output nicely with proper alignment
- Highlights the diagonal (where row = column) with special characters

► `part_1_python/chapter_03_control_flow/exercise_1_3_7_solution.py`

**Exercise 2: Star Pattern Printer**
Build a program that prints various patterns:
- Right triangle of stars
- Inverted triangle
- Diamond shape
- Let the user choose which pattern to print
- Use nested loops and conditions to create each pattern

► `part_1_python/chapter_03_control_flow/exercise_2_3_7_solution.py`

---

## Challenge Project: Build Your Own AI Decision System

Create a "Personal AI Assistant" that:
1. Greets the user based on time of day (using conditionals)
2. Offers a menu of services (using loops)
3. Can play a simple game (using nested structures)
4. Keeps track of user preferences (preparing for next chapter's data structures)
5. Has a conversation mode (using while loops and string checking)

This project combines everything from Chapter 3 and prepares you for the data structures coming in Chapter 4!
