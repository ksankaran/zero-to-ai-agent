# Chapter 1: Setting Up Your Development Environment

## System Check

Chapter 1 is all about setting up your development environment from scratch! Unlike other chapters, there are no prerequisites - you'll install everything as you work through the chapter.

**What you'll set up in this chapter:**
- Python 3.13 (or later)
- VS Code with Python extension
- Terminal/command line basics
- Virtual environments
- pip package manager

**Verification (after completing the chapter):**

Check Python is installed:
```bash
python --version
# Should show: Python 3.13.x (or your installed version)
```

Check pip is working:
```bash
pip --version
# Should show pip version and Python path
```

---

## Troubleshooting

### Section 1.1: Installing Python and VS Code

**Python Installation Issues:**

If you see an error like "python is not recognized as an internal or external command":
- You probably forgot to check "Add Python to PATH" during installation
- Solution: Uninstall Python from your Programs, then reinstall it, this time checking that crucial box

If you see a different version (like Python 3.11 or 3.12):
- You might have an older Python already installed
- Try typing python3.13 --version instead
- Or use py -3.13 --version on Windows

**VS Code and Python Issues:**

> **"I see 'Python 2.7' when I check the version"**
> - You have an old Python installed
> - Make sure you're typing python3 instead of python
> - Or uninstall Python 2 and reinstall Python 3
>
> **"VS Code says 'Select Python Interpreter'"**
> - Click on the message
> - Choose the Python 3.x option from the list
> - If no options appear, Python might not be installed correctly
>
> **"My code runs but nothing happens"**
> - Make sure you saved the file with a .py extension
> - Check that you're in the right folder in terminal (cd to navigate)
> - Try adding print("Testing") at the top of your file

### Section 1.2: Terminal/Command Line

> **"Command not found" or "not recognized"**
> - You typed the command wrong (check spelling)
> - The program isn't installed
> - The program isn't in your PATH (remember that checkbox during Python installation?)
>
> **"Permission denied"**
> - You're trying to modify a protected file
> - Solution: Be careful what you're trying to change
>
> **"No such file or directory"**
> - You're in the wrong location (use `pwd` to check)
> - The file doesn't exist (use `ls` to see what's there)
> - You typed the name wrong (remember: terminals are case-sensitive!)

### Section 1.3: Virtual Environments

> **"activation script cannot be loaded"** (Windows PowerShell)
> - Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
> - Try activating again
>
> **"No module named venv"**
> - Your Python installation might be incomplete
> - Reinstall Python with all optional features
>
> **VS Code not recognizing virtual environment**
> - Make sure you opened the project folder, not just a file
> - Manually select interpreter (bottom-right corner, some platforms have it in bottom-left)
> - Restart VS Code
>
> **Forgot to activate before installing packages**
> - Packages were installed globally
> - Activate your environment and reinstall
>
> **"pip is not recognized"**
> - Virtual environment isn't activated
> - Or pip isn't installed in the environment

### Section 1.4: Package Management with pip

> **"Could not find a version that satisfies the requirement"**
> - Package name might be wrong (it's `beautifulsoup4`, not `beautifulsoup`)
> - Package might not support your Python version

> **"No matching distribution found"**
> - You might be offline
> - The package might not exist on PyPI

> **Installation fails with error messages**
> - Some packages need system libraries (like `psycopg2` needs PostgreSQL)
> - On Windows, some packages need Visual C++ tools
> - Solution: Look for pre-built wheels or check the package documentation

### Section 1.5: First Python Programs

> **SyntaxError**
> ```python
> print("Hello World!)  # Missing closing quote
> ```
> Python couldn't understand your code structure. Check for missing quotes, parentheses, or colons.

> **IndentationError**
> ```python
> if True:
> print("Indented wrong")  # Should be indented
> ```
> Python uses indentation (spaces) to understand code blocks. Make sure your indents line up.

> **NameError**
> ```python
> print(unknown_variable)  # Variable doesn't exist
> ```
> You're trying to use something Python doesn't know about yet.

> **TypeError**
> ```python
> "5" + 5  # Can't add text to numbers
> ```
> You're mixing incompatible types. Convert them first!

### Section 1.6: Scripts vs Notebooks

> **Q: Should I learn notebooks now?**
> A: No, focus on scripts first. Notebooks can wait until you're comfortable with Python basics.

> **Q: Will I miss out by not using notebooks?**
> A: Not at all! Everything you learn with scripts applies to notebooks. Scripts actually teach better programming habits.

> **Q: When should I learn notebooks?**
> A: After Chapter 6, once you're comfortable with Python. Or even after finishing the book - there's no rush!

> **Q: Do professional programmers use notebooks?**
> A: Yes, but mainly for experimentation and data analysis. Production code is almost always in scripts.

---

## Practice Exercises

### Section 1.1

**Exercise 1: The Calculator**

Create a new file called `calculator.py` and make it:
1. Ask for two numbers
2. Add them together
3. Display the result

► `part_1_python/chapter_01_setup/exercise_1_1_1_solution.py`

**Exercise 2: The Personal Greeter**

Create a file called `greeter.py` that:
1. Asks for your name
2. Asks for your age
3. Prints a message like "Hello [name], you are [age] years old!"

► `part_1_python/chapter_01_setup/exercise_2_1_1_solution.py`

**Exercise 3: Explore VS Code**

Without writing code, explore VS Code:
1. Try changing the theme again
2. Open the Command Palette with Ctrl+Shift+P (or Cmd+Shift+P)
3. Type "Python" and see what Python-related commands are available

► `part_1_python/chapter_01_setup/exercise_3_1_1_solution.md`

### Section 1.2

**Exercise 1: Navigation Challenge**

Using only terminal commands:
1. Navigate to your Desktop
2. Create a folder called `terminal_practice`
3. Inside it, create three subfolders: `projects`, `notes`, `scripts`
4. Navigate into `scripts` and create an empty file called `test.py`
5. Navigate back to Desktop in one command

► `part_1_python/chapter_01_setup/exercise_1_1_2_solution.md`

**Exercise 2: Daily Journal Program**

► `part_1_python/chapter_01_setup/journal.py`

```python
import datetime

print("=" * 50)
print("DAILY JOURNAL")
print("=" * 50)

print(f"Today's date: {datetime.datetime.now()}")
print("")
print("Welcome to your coding journal!")
print("")
print("In Chapter 6, we'll learn to save entries to files.")
print("For now, practice running Python programs!")
print("")
print("Tip: Keep a real journal of what you learn.")
print("Writing helps reinforce new concepts.")
print("=" * 50)
```

Run it from terminal:
```bash
python journal.py
```

This displays the current date and a motivational message. In Chapter 6, we'll upgrade this to actually save your entries to files!

### Section 1.3

**Exercise 1: Multi-Environment Project**

Create two projects with different package versions to see isolation in action:

**Project 1: Old Version**
```bash
cd Desktop
mkdir project_old
cd project_old
python -m venv venv_old
.\venv_old\Scripts\Activate.ps1  # Or source venv_old/bin/activate

# Install an older version of a package
pip install numpy==1.21.0
python -c "import numpy; print(f'Project 1 NumPy: {numpy.__version__}')"
deactivate
```

**Project 2: New Version**
```bash
cd ..
mkdir project_new
cd project_new
python -m venv venv_new
.\venv_new\Scripts\Activate.ps1  # Or source venv_new/bin/activate

# Install the latest version
pip install numpy
python -c "import numpy; print(f'Project 2 NumPy: {numpy.__version__}')"
deactivate
```

Both projects coexist peacefully with different NumPy versions!

► `part_1_python/chapter_01_setup/exercise_1_1_3_solution.md`

**Exercise 2: Environment Inspector**

Create a script that reports on your current Python environment:
- Whether you're in a virtual environment
- Python version
- Location of Python executable
- Number of installed packages
- Total size of installed packages

► `part_1_python/chapter_01_setup/exercise_2_1_3_solution.py`

**Exercise 3: Requirements Comparison**

Create two virtual environments with different packages, generate requirements.txt for each, and write a script that compares them to show:
- Packages unique to each environment
- Packages in both but with different versions
- Packages that are identical

► `part_1_python/chapter_01_setup/exercise_3_1_3_solution.py`

### Section 1.4

**Exercise 1: Package Explorer**

Create a script that explores your Python environment:

► `part_1_python/chapter_01_setup/my_packages.py`

**Key pattern - checking if packages are installed:**
```python
# Test if a package is available
try:
    import requests
    print("✔ requests is installed and working!")
except ImportError:
    print("[X] requests is not installed")

# Repeat for other packages
try:
    import colorama
    print("✔ colorama is installed and working!")
except ImportError:
    print("[X] colorama is not installed")
```

Run it with:
```bash
python my_packages.py
```

This script explores your Python environment programmatically - a technique you'll use when building AI agents that need to understand their own capabilities.

► `part_1_python/chapter_01_setup/exercise_1_1_4_solution.py`

**Exercise 2: Dependency Detective**

Write a script that:
1. Takes a package name as input
2. Uses `pip show` to find its dependencies
3. Recursively finds dependencies of dependencies
4. Displays a dependency tree

► `part_1_python/chapter_01_setup/exercise_2_1_4_solution.py`

**Exercise 3: Version Manager**

Create a script that:
1. Reads your requirements.txt
2. Checks each package for available updates
3. Shows current version vs latest version
4. Warns about major version changes (1.x to 2.x)

► `part_1_python/chapter_01_setup/exercise_3_1_4_solution.py`

### Section 1.5

**Exercise 1: Personalized Greeter**

Create `personal_greeter.py` that:
- Asks for name and age
- Calculates birth year
- Gives a personalized message

► `part_1_python/chapter_01_setup/exercise_1_1_5_solution.py`

**Exercise 2: Temperature Converter**

Create `temp_converter.py` that:
- Asks for temperature in Celsius
- Converts to Fahrenheit (F = C × 9/5 + 32)
- Shows both temperatures

► `part_1_python/chapter_01_setup/exercise_2_1_5_solution.py`

**Exercise 3: Days Until Python Master**

Create `learning_tracker.py` that:
- Asks when you started learning (today!)
- Estimates 100 days to proficiency
- Shows the target date

► `part_1_python/chapter_01_setup/exercise_3_1_5_solution.py`

### Section 1.6

**Exercise 1: Understanding the Flow**

► `part_1_python/chapter_01_setup/flow_test.py`

Or create it yourself:
```python
"""
Understanding how scripts flow from top to bottom
"""

print("1. Scripts start here")

name = input("2. What's your name? ")

print(f"3. Hello {name}!")

number = int(input("4. Pick a number: "))

print(f"5. Your number doubled is {number * 2}")

print("6. Scripts end here - everything ran in order!")
```

Run it: `python flow_test.py`

Notice how it goes 1→2→3→4→5→6 every time. That's a script! In a notebook, you could run step 5 before step 4 (though it would error), or run step 3 multiple times. But scripts keep things simple and ordered.

► `part_1_python/chapter_01_setup/exercise_1_1_6_solution.py`
