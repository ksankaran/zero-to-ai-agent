# Chapter 6: Working with External Data

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
mkdir part_1_python\chapter_06_external_data
cd part_1_python\chapter_06_external_data
```

**On Mac/Linux:**
```bash
mkdir -p part_1_python/chapter_06_external_data
cd part_1_python/chapter_06_external_data
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

6. Install the required packages for Chapter 6:

► `requirements.txt`

Or copy and create the file yourself:
```
# requirements.txt
requests==2.32.5
python-dotenv==1.2.1
```

Then install with:
```
pip install -r requirements.txt
```

This will install:
- `requests` (2.32.5) - for making API calls in section 6.3
- `python-dotenv` (1.2.1) - for managing environment variables in section 6.5

---

## Troubleshooting

### File Operations (Section 6.1)

- **Problem:** "Permission Denied" error
  **Solution:** Check if the file is open in another program, or if you have write permissions to the directory.

- **Problem:** Files appear empty after writing
  **Solution:** Make sure you're closing the file (or using `with` statement) - data might still be in the buffer!

- **Problem:** Weird characters (�) in your file
  **Solution:** Use `encoding='utf-8'` when opening files: `open('file.txt', 'r', encoding='utf-8')`

- **Problem:** "File not found" even though you can see it
  **Solution:** Check your working directory with `os.getcwd()` - you might be in a different folder than you think!

- **Problem:** Line breaks look wrong
  **Solution:** Python handles line breaks automatically. Always use `\n` and let Python convert it for your operating system.

### JSON Issues (Section 6.2)

- **Problem:** "JSONDecodeError" when reading a file
  **Solution:** Check for trailing commas, ensure all strings use double quotes, and verify the file isn't corrupted. Use a JSON validator online.

- **Problem:** Can't save certain Python objects to JSON
  **Solution:** Convert unsupported types: datetime → `.isoformat()`, sets → `list()`, custom objects → dictionaries

- **Problem:** Unicode characters show as escape sequences
  **Solution:** Use `ensure_ascii=False` in `json.dump()`: `json.dump(data, file, ensure_ascii=False)`

- **Problem:** JSON file is one long line, hard to read
  **Solution:** Add `indent` parameter: `json.dump(data, file, indent=4)`

- **Problem:** Float values like NaN or Infinity
  **Solution:** Replace with None or string representation before serializing

### Common API Issues (Section 6.3)

- **Problem:** "Connection refused" or timeout errors
  **Solution:** Check your internet connection, verify the API URL is correct, and add timeout parameters to requests

- **Problem:** 401 Unauthorized error
  **Solution:** Check your API key is correct, not expired, and being sent in the right format (header vs parameter)

- **Problem:** 429 Too Many Requests
  **Solution:** You're hitting rate limits. Add delays between requests or implement proper rate limiting

- **Problem:** JSON decode error
  **Solution:** The response might not be JSON. Check `response.headers['Content-Type']` and print `response.text` to debug

- **Problem:** SSL certificate errors
  **Solution:** Update your certificates, or (for testing only!) use `verify=False` in requests

### Error Handling Issues (Section 6.4)

- **Problem:** Exception not caught
  **Solution:** Check exception type with `type(e).__name__`, might be different than expected

- **Problem:** Finally not executing
  **Solution:** Don't use `sys.exit()` in try block, use return/break instead

- **Problem:** Lost exception context
  **Solution:** Use `raise ... from e` to preserve original exception

- **Problem:** Too broad exception handling
  **Solution:** Replace `except:` with specific exceptions

### Environment Variable Issues (Section 6.5)

- **Problem:** Environment variable not found
  **Solution:** Check spelling, ensure it's exported (not just set), and restart your terminal/IDE

- **Problem:** .env file not loading
  **Solution:** Ensure python-dotenv is installed, .env is in the right directory, and you're calling load_dotenv()

- **Problem:** Different behavior on different systems
  **Solution:** Use os.path.expanduser('~') for home directory, Path for cross-platform paths

- **Problem:** Secrets visible in logs/errors
  **Solution:** Never print full secrets, use `key[:4] + '****'` to show just prefix

### CSV Issues (Section 6.6)

- **Problem:** Extra blank lines when writing CSV on Windows
  **Solution:** Always use `newline=''` when opening files for CSV writing

- **Problem:** Commas in data breaking columns
  **Solution:** The csv module handles this automatically with proper quoting

- **Problem:** Large file crashes program
  **Solution:** Process row-by-row, never `list(reader)` for huge files

- **Problem:** Excel changes data formats
  **Solution:** Use `.txt` extension or import wizard in Excel to preserve formats

---

## Practice Exercises

### Section 6.1

**Exercise 1: Daily Note Taker**
Create a simple program that lets you write a daily note to a file.

**Your Task:**
1. Ask the user for their note
2. Add the current date/time to the note
3. Save it to a file called "daily_notes.txt"
4. Each note should be on a new line with the date

**Starter Hints:**
- Use `datetime.now()` to get current time
- Use `open("daily_notes.txt", "a")` to append
- Format: `[2024-01-15 10:30] Your note here`

► `exercise_1_6_1_solution.py`

**Exercise 2: Simple Shopping List**
Build a shopping list that saves items to a file.

**Your Task:**
1. Show a menu: Add item, View list, Clear list, Exit
2. Save items to "shopping_list.txt" (one per line)
3. Display all items when viewing
4. Clear should empty the file

**Starter Hints:**
- Use a while loop for the menu
- Use `"w"` mode to clear the file
- Use `readlines()` to get all items

► `exercise_2_6_1_solution.py`

**Exercise 3: Word Counter**
Create a program that counts words in any text file.

**Your Task:**
1. Ask user for a filename
2. Count total words in the file
3. Count total lines
4. Find the longest word
5. Display the results

**Starter Hints:**
- Use `split()` to separate words
- Handle FileNotFoundError with try/except
- A word is anything separated by spaces

► `exercise_3_6_1_solution.py`

---

### Section 6.2

**Exercise 1: Simple Contact Book**
Create a contact book that saves to JSON.

**Your Task:**
1. Create a menu: Add contact, View all, Find contact, Exit
2. Each contact has: name, phone, email
3. Save contacts to "contacts.json"
4. Load existing contacts when program starts

**Starter Hints:**
- Store contacts as a list of dictionaries
- Use `json.dump()` to save, `json.load()` to load
- Handle FileNotFoundError when loading

► `exercise_1_6_2_solution.py`

**Exercise 2: Settings Manager**
Build a program that manages app settings in JSON.

**Your Task:**
1. Create default settings (username, theme, font_size)
2. Let user change any setting
3. Save settings to "settings.json"
4. Load settings on startup, use defaults if file doesn't exist

**Starter Hints:**
- Use a dictionary for settings
- Provide a menu to change each setting
- Use `json.dumps(data, indent=4)` for pretty formatting

► `exercise_2_6_2_solution.py`

**Exercise 3: Score Tracker**
Create a game score tracker using JSON.

**Your Task:**
1. Track player name and score
2. Save top 5 high scores to "highscores.json"
3. Display leaderboard
4. Add new scores and keep only top 5

**Starter Hints:**
- Store scores as list of dictionaries
- Sort by score: `sorted(scores, key=lambda x: x['score'], reverse=True)`
- Keep only first 5: `scores[:5]`

► `exercise_3_6_2_solution.py`

---

### Section 6.3

**Exercise 1: Weather Checker**
Create a simple weather app using a free API.

**Your Task:**
1. Use the free wttr.in API (no key needed!)
2. Ask user for a city name
3. Get and display current temperature
4. Show weather condition (sunny, rainy, etc.)
5. Handle errors if city not found

**Starter Hints:**
- URL: `https://wttr.in/{city}?format=j1`
- Use `requests.get(url)` to fetch data
- Temperature is in `response.json()['current_condition'][0]['temp_C']`

► `exercise_1_6_3_solution.py`

**Exercise 2: Dad Joke Fetcher**
Build a program that fetches random jokes from an API.

**Your Task:**
1. Use the free Dad Joke API
2. Fetch a random joke
3. Display it nicely formatted
4. Ask user if they want another joke
5. Keep count of jokes viewed

**Starter Hints:**
- URL: `https://icanhazdadjoke.com/`
- Add header: `{'Accept': 'application/json'}`
- Joke is in `response.json()['joke']`

► `exercise_2_6_3_solution.py`

**Exercise 3: Number Facts**
Create a program that gets interesting facts about numbers.

**Your Task:**
1. Use the Numbers API (no key needed)
2. Ask user for a number
3. Get a math fact about that number
4. Get a trivia fact about that number
5. Save interesting facts to a file

**Starter Hints:**
- Math URL: `http://numbersapi.com/{number}/math`
- Trivia URL: `http://numbersapi.com/{number}/trivia`
- Response is plain text, use `response.text`

► `exercise_3_6_3_solution.py`

---

### Section 6.4

**Exercise 1: Safe Calculator**
Create a calculator that handles errors gracefully.

**Your Task:**
1. Ask user for two numbers and an operation (+, -, *, /)
2. Handle ValueError if user enters non-numbers
3. Handle ZeroDivisionError for division by zero
4. Keep asking until valid input is given
5. Show the result

**Starter Hints:**
- Use try/except around `float(input())`
- Use separate except blocks for different errors
- Use a while loop to retry on error

► `exercise_1_6_4_solution.py`

**Exercise 2: File Reader with Error Handling**
Build a program that safely reads any file.

**Your Task:**
1. Ask user for a filename
2. Try to read and display the file
3. Handle FileNotFoundError with helpful message
4. Handle PermissionError if file is protected
5. Offer to try another file on error

**Starter Hints:**
- Use multiple except blocks
- Give specific messages for each error type
- Use a loop to allow retrying

► `exercise_2_6_4_solution.py`

**Exercise 3: List Index Checker**
Create a program that safely accesses list items.

**Your Task:**
1. Create a list of 5 items
2. Ask user for an index
3. Handle IndexError if index too large
4. Handle ValueError if not a number
5. Display the item at that index

**Starter Hints:**
- List indices start at 0
- Use try/except around `list[int(index)]`
- Show valid range in error message

► `exercise_3_6_4_solution.py`

---

### Section 6.5

**Exercise 1: Simple Config Reader**
Create a program that reads configuration from environment variables.

**Your Task:**
1. Create a .env file with APP_NAME and DEBUG_MODE
2. Load these variables using python-dotenv
3. Display the configuration
4. Use default values if variables don't exist
5. Never print actual API keys (just show first 4 chars)

**Starter Hints:**
- Use `load_dotenv()` at the start
- Use `os.environ.get('KEY', 'default')`
- For secrets: `key[:4] + '****' if len(key) > 4 else '****'`

► `exercise_1_6_5_solution.py`

**Exercise 2: Environment Switcher**
Build a program that works differently in dev vs production.

**Your Task:**
1. Check for an ENVIRONMENT variable
2. If "development": show debug messages
3. If "production": hide debug messages
4. Use different file paths for each environment
5. Show current environment on startup

**Starter Hints:**
- Set default: `os.environ.get('ENVIRONMENT', 'development')`
- Use if/else to change behavior
- Debug example: `if env == 'development': print('DEBUG:', message)`

► `exercise_2_6_5_solution.py`

**Exercise 3: Safe API Key Loader**
Create a program that safely loads and uses an API key.

**Your Task:**
1. Create .env file with a fake API_KEY
2. Load the key without showing it
3. Check if key exists before using
4. Show warning if key is missing
5. Create .env.example file showing structure

**Starter Hints:**
- Check existence: `if not api_key:`
- Never print full key
- .env.example should have: `API_KEY=your-key-here`

► `exercise_3_6_5_solution.py`

---

### Section 6.6

**Exercise 1: Student Grade Tracker**
Create a program that manages student grades in CSV.

**Your Task:**
1. Create a CSV with columns: name, subject, grade
2. Add new student grades
3. Calculate average grade per student
4. Save results to a new CSV file
5. Handle if file doesn't exist

**Starter Hints:**
- Use `csv.DictReader()` to read
- Use `csv.DictWriter()` to write
- Calculate average: `sum(grades) / len(grades)`

► `exercise_1_6_6_solution.py`

**Exercise 2: Expense Tracker**
Build a simple expense tracker using CSV.

**Your Task:**
1. Track: date, description, amount, category
2. Add new expenses
3. View all expenses
4. Calculate total by category
5. Export summary to new CSV

**Starter Hints:**
- Use today's date: `datetime.now().strftime('%Y-%m-%d')`
- Store amounts as float
- Group by category using a dictionary

► `exercise_2_6_6_solution.py`

**Exercise 3: Product Inventory**
Create an inventory management system with CSV.

**Your Task:**
1. Track: product_name, quantity, price
2. Add new products
3. Update quantities
4. Calculate total inventory value
5. Find products low in stock (< 10)

**Starter Hints:**
- Value = quantity × price
- Update by reading all, modifying, writing back
- Use a threshold variable for low stock

► `exercise_3_6_6_solution.py`

---

## Challenge Project: Build Your Own Data Pipeline

### The Challenge: Create a Data Processing System

Now it's time to combine everything you've learned in Chapter 6 into one powerful project!

> `part_1_python/chapter_06_external_data/dashboard_challenge.py`

### What You'll Build:

A **Data Pipeline** - a system that takes raw data, processes it, and outputs clean, useful information. Think of it like a factory assembly line for data!

```python
class DataPipeline:
    """
    A system that processes data through stages:
    Raw Data → Load → Clean → Transform → Save → Useful Output!
    """

    def __init__(self):
        self.data = []  # Your data will live here

    def load_csv(self, filename):
        """Load data from a CSV file"""
        # You'll implement this!

    def clean(self):
        """Remove bad data, fix formats"""
        # You'll implement this!

    def save(self, output_file):
        """Save the processed data"""
        # You'll implement this!
```

### Your Mission:

Build a data pipeline that processes real-world data using ALL the skills from Chapter 6:

1. **Files** (Section 6.1) → Read and write data files
2. **JSON** (Section 6.2) → Save data in JSON format
3. **APIs** (Section 6.3) → Fetch fresh data from the internet
4. **Error Handling** (Section 6.4) → Handle problems gracefully
5. **Environment Variables** (Section 6.5) → Keep API keys secure
6. **CSV** (Section 6.6) → Process spreadsheet data

### Pick Your Project:

Choose one of these starter projects (or create your own!):

#### Option 1: Weather Tracker
```python
# Process weather for multiple cities
pipeline = DataPipeline()
pipeline.load_csv("cities.csv")  # List of cities
pipeline.fetch_weather()          # Get weather from API
pipeline.save("weather_report.csv")
```

#### Option 2: Expense Analyzer
```python
# Process and analyze expenses
pipeline = DataPipeline()
pipeline.load_csv("expenses.csv")  # Your expenses
pipeline.clean()                   # Fix messy data
pipeline.calculate_totals()        # Add analysis
pipeline.save("expense_report.json")
```

#### Option 3: News Aggregator
```python
# Collect and organize news
pipeline = DataPipeline()
pipeline.load_csv("topics.csv")    # Topics to search
pipeline.fetch_news()              # Get from news API
pipeline.save("daily_digest.txt")
```

### Build Up in Phases:

**Phase 1**: Get basic pipeline working (load CSV, save CSV)

**Phase 2**: Add data cleaning (remove empty rows, fix formats)

**Phase 3**: Add APIs (fetch fresh data from weather, news, or prices)

**Phase 4**: Make it professional (error handling, environment variables, logging)
