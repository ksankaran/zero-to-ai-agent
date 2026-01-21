# Chapter 4: Data Structures - Organizing Your Data Like a Pro

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
mkdir part_1_python\chapter_04_data_structures
cd part_1_python\chapter_04_data_structures
```

**On Mac/Linux:**
```bash
mkdir -p part_1_python/chapter_04_data_structures
cd part_1_python/chapter_04_data_structures
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

### IndexError: list index out of range

This happens when you try to access an index that doesn't exist. If your list has 6 items, the valid indices are 0 through 5. Trying to access index 6 or higher will cause this error. Always remember: if a list has n items, the last valid index is n-1.

### ValueError: list.remove(x): x not in list

This happens when you try to remove an item that doesn't exist. Always check if an item exists before removing it:
```python
if "item" in my_list:
    my_list.remove("item")
```

### KeyError: 'key_name'

This happens when you try to access a key that doesn't exist in a dictionary. Always use one of these safe approaches:
1. Check first: `if key in dictionary:`
2. Use get(): `value = dictionary.get(key, default_value)`
3. Use try/except for error handling

---

## Practice Exercises

### Section 4.1

**Exercise 1: Shopping Cart Manager**

Create a shopping cart system that:
1. Starts with an empty cart (list)
2. Adds these items: "apples", "bread", "milk", "eggs", "cheese"
3. Displays the first and last items using indexing
4. Removes the third item
5. Checks if "milk" is in the cart
6. Displays the total number of items

► `part_1_python/chapter_04_data_structures/exercise_1_4_1_solution.py`

**Exercise 2: Grade Analyzer**

Build a grade tracking system that:
1. Creates a list of 10 test scores: [85, 92, 78, 95, 88, 73, 91, 82, 79, 96]
2. Finds and displays the highest score (hint: use max())
3. Finds and displays the lowest score (hint: use min())
4. Calculates the average score
5. Extracts the top 3 scores using slicing after sorting
6. Counts how many scores are above 85

► `part_1_python/chapter_04_data_structures/exercise_2_4_1_solution.py`

**Exercise 3: Matrix Operations**

Work with a 3x3 matrix (nested list):
1. Create a 3x3 matrix: [[1,2,3], [4,5,6], [7,8,9]]
2. Access and print the center element (5)
3. Extract and print the first row
4. Extract and print the last column [3, 6, 9]
5. Calculate the sum of diagonal elements [1, 5, 9]
6. Create a flattened list containing all elements in order

► `part_1_python/chapter_04_data_structures/exercise_3_4_1_solution.py`

### Section 4.2

**Exercise 1: Shopping Cart Manager**

Create a shopping cart system that:
1. Start with an empty cart
2. Add items: "apple", "banana", "apple", "orange", "banana", "grape"
3. Count how many apples and bananas are in the cart
4. Remove one banana using remove()
5. Sort the cart alphabetically
6. Display the final cart and total number of items

► `part_1_python/chapter_04_data_structures/exercise_1_4_2_solution.py`

**Exercise 2: Score Tracker**

Build a score tracking system that:
1. Start with scores: [75, 82, 90, 68, 95, 78]
2. Add three more scores: 88, 92, 79 using extend()
3. Find the highest and lowest scores
4. Calculate the average score
5. Remove the lowest score using remove()
6. Sort scores from highest to lowest
7. Display the top 3 scores

► `part_1_python/chapter_04_data_structures/exercise_2_4_2_solution.py`

**Exercise 3: Message Queue**

Build a message queue that:
1. Maintains a maximum of 5 messages
2. Process these messages in order: "msg1", "msg2", "msg3", "msg4", "msg5", "msg6", "msg7"
3. When full, remove the oldest message using pop(0) before adding new ones
4. After processing all messages, show the final queue
5. Search for any message containing "5" using index()
6. Count how many times "msg" appears in any message

► `part_1_python/chapter_04_data_structures/exercise_3_4_2_solution.py`

### Section 4.3

**Exercise 1: Color Palette Manager**

Create a color palette system that:
1. Store RGB colors as tuples: red=(255,0,0), green=(0,255,0), blue=(0,0,255)
2. Create a mixed color by averaging two color tuples
3. Store colors in a dictionary with tuple keys for coordinates
4. Return color information as a named tuple with fields: name, rgb, hex

► `part_1_python/chapter_04_data_structures/exercise_1_4_3_solution.py`

**Exercise 2: Game State Snapshots**

Build a simple game state system that:
1. Store player position as a tuple (x, y)
2. Save game snapshots as tuples: (turn_number, position, score, health)
3. Maintain a list of these immutable snapshots
4. Find the snapshot with the highest score
5. Return game statistics as a tuple

► `part_1_python/chapter_04_data_structures/exercise_2_4_3_solution.py`

**Exercise 3: Model Configuration Validator**

Create a configuration system that:
1. Define valid model configs as tuples: (name, layers, parameters, learning_rate)
2. Store multiple configurations
3. Validate that configurations haven't been modified
4. Return the smallest and largest models based on parameters
5. Unpack and display configuration details

► `part_1_python/chapter_04_data_structures/exercise_3_4_3_solution.py`

### Section 4.4

**Exercise 1: Product Inventory System**

Create an inventory system that:
1. Store products with name, price, and quantity
2. Add new products
3. Update quantities
4. Calculate total inventory value
5. Find products below a certain stock level
6. Generate a restock report

► `part_1_python/chapter_04_data_structures/exercise_1_4_4_solution.py`

**Exercise 2: Student Grade Manager**

Build a grade management system that:
1. Store students with their grades in multiple subjects
2. Add new students and grades
3. Calculate average grade per student
4. Find the top performer
5. Generate a report card for a specific student
6. List all students failing any subject (grade < 60)

► `part_1_python/chapter_04_data_structures/exercise_2_4_4_solution.py`

**Exercise 3: API Response Handler**

Create a system that:
1. Process mock API responses (nested dictionaries)
2. Extract specific fields safely
3. Handle missing keys gracefully
4. Count total API calls by endpoint
5. Cache responses to avoid duplicate calls
6. Generate usage statistics

► `part_1_python/chapter_04_data_structures/exercise_3_4_4_solution.py`

### Section 4.5

**Exercise 1: Email List Manager**

Create a system that:
1. Manage email lists for different campaigns
2. Add emails to lists (no duplicates allowed)
3. Find common subscribers between campaigns
4. Identify exclusive subscribers for each campaign
5. Merge campaign lists without duplicates
6. Generate statistics about overlap between campaigns

► `part_1_python/chapter_04_data_structures/exercise_1_4_5_solution.py`

**Exercise 2: Skill Matcher**

Build a job matching system that:
1. Store job requirements as sets of skills
2. Store candidate skills as sets
3. Find perfect matches (candidate has all required skills)
4. Find partial matches with match percentage
5. Identify missing skills for each candidate
6. Recommend training based on skill gaps

► `part_1_python/chapter_04_data_structures/exercise_2_4_5_solution.py`

**Exercise 3: Document Similarity Analyzer**

Create a text analysis system that:
1. Extract unique words from documents
2. Calculate vocabulary overlap between documents
3. Find common themes (shared important words)
4. Identify unique vocabulary per document
5. Calculate similarity scores
6. Group similar documents together

► `part_1_python/chapter_04_data_structures/exercise_3_4_5_solution.py`

### Section 4.6

**Exercise 1: Task Management System**

Design data structures for a task management system that needs to:
1. Store tasks with title, priority, and status
2. Track unique tags across all tasks
3. Maintain task order by creation time
4. Quickly look up tasks by ID
5. Group tasks by status

► `part_1_python/chapter_04_data_structures/exercise_1_4_6_solution.py`

**Exercise 2: Quiz Application**

Choose data structures for a quiz app that needs to:
1. Store questions with multiple choice answers
2. Track which questions a user has answered
3. Maintain question order
4. Store correct answers securely
5. Calculate scores quickly

► `part_1_python/chapter_04_data_structures/exercise_2_4_6_solution.py`

**Exercise 3: Social Network Features**

Pick data structures for social features that need to:
1. Store user friendships (bidirectional)
2. Track unique hashtags in posts
3. Maintain a feed in chronological order
4. Store user metadata
5. Find mutual friends efficiently

► `part_1_python/chapter_04_data_structures/exercise_3_4_6_solution.py`

### Section 4.7

**Exercise 1: Data Cleaning**
You have messy data that needs cleaning:
- A list of strings with extra spaces: ["  hello  ", " WORLD ", "  Python  "]
- Create a cleaned list with stripped, lowercase strings
- Filter out any strings shorter than 4 characters

► `part_1_python/chapter_04_data_structures/exercise_1_4_7_solution.py`

**Exercise 2: Grade Processing**
Given a list of student records:
```python
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78},
    {"name": "Diana", "grade": 95},
    {"name": "Eve", "grade": 88}
]
```
Use comprehensions to:
- Extract all names
- Get names of students with grades >= 90
- Create a dictionary of name: grade pairs
- Calculate letter grades (A if >= 90, B if >= 80, C otherwise)

► `part_1_python/chapter_04_data_structures/exercise_2_4_7_solution.py`

**Exercise 3: Number Processing**
Given numbers = range(1, 21):
- Create a list of all even numbers
- Create a list of squares of odd numbers
- Create a dictionary where keys are numbers and values are "even" or "odd"
- Create a list of tuples (number, square, cube) for numbers 1-10

► `part_1_python/chapter_04_data_structures/exercise_3_4_7_solution.py`

---

## Challenge Project: Personal Data Dashboard

### The Challenge: Build "DataMaster" - Your Personal Data Analysis System

Create a comprehensive data analysis system that combines ALL the data structures you've learned to process real-world information!

### Project Requirements:

#### Part 1: Data Collection System
Create a system that can:
- **Store** multiple datasets (use appropriate structures)
- **Import** data from CSV files (parse into dictionaries)
- **Track** unique values across all datasets (sets)
- **Maintain** data history (lists with timestamps)

#### Part 2: Analysis Engine
Build analysis functions that:
- **Calculate** statistics (mean, median, mode) using lists
- **Group** data by categories using dictionaries
- **Find** common elements across datasets using sets
- **Generate** summaries using comprehensions

#### Part 3: Query System
Implement a query interface that can:
- **Filter** data based on conditions
- **Sort** results by any field
- **Join** data from multiple sources
- **Export** results in different formats

#### Part 4: Performance Monitor
Track system performance:
- **Measure** operation speeds (list vs set lookups)
- **Store** performance metrics (dictionaries)
- **Identify** bottlenecks (analyze with comprehensions)
- **Optimize** data structure choices

### Starter Code Structure:

► `part_1_python/chapter_04_data_structures/datamaster.py`

```python
# Initialize data structures for different purposes
datasets = {}      # Dictionary: store named datasets
unique_values = set()  # Set: track unique values
history = []       # List: record operations in order
metadata = {}      # Dictionary: store dataset info

# Load sample data (list of dictionaries)
sales_data = [
    {"product": "Widget A", "price": 29.99, "quantity": 10},
    {"product": "Widget B", "price": 49.99, "quantity": 5},
]
datasets["sales"] = sales_data

# Use SET to find unique products
unique_products = {record["product"] for record in sales_data}

# Use DICTIONARY to calculate revenue by product
revenue_by_product = {}
for record in sales_data:
    product = record["product"]
    revenue = record["price"] * record["quantity"]
    revenue_by_product[product] = revenue_by_product.get(product, 0) + revenue

# Use LIST comprehension to filter high-value sales
high_value = [r for r in sales_data if r["price"] * r["quantity"] > 100]
```

The starter code demonstrates:
- Using dictionaries to store and organize datasets
- Using sets to track unique values efficiently
- Using lists to maintain ordered records
- Using comprehensions to transform and filter data

### Challenge Levels:

#### Bronze Level: Basic Implementation
- Implement all basic methods
- Handle at least 2 datasets
- Use all 4 data structures appropriately
- Generate a simple text report

#### Silver Level: Enhanced Features
- Add data validation with meaningful errors
- Implement caching for expensive operations
- Support multiple file formats (CSV, JSON)
- Create performance comparison reports

#### Gold Level: Advanced System
- Real-time data updates with event tracking
- Complex multi-condition queries
- Data relationship mapping and visualization
- Export to multiple formats with formatting
- Performance optimization with benchmarks

### Success Criteria:

Your DataMaster system should:
- Use lists for ordered data and history
- Use tuples for immutable configuration
- Use dictionaries for lookups and mappings
- Use sets for uniqueness and comparisons
- Combine structures effectively (list of dicts, dict of sets, etc.)
- Utilize comprehensions for data transformation
- Choose the right structure for each task
- Handle errors gracefully
- Provide useful analysis insights

### Bonus Challenges:

**Memory Challenge**: Implement a memory limit system that automatically switches from lists to generators when data gets large

**Speed Challenge**: Create a benchmark suite that proves your data structure choices are optimal

**Visualization Challenge**: Add a simple text-based visualization of your data (bar charts using characters)

**AI Integration**: Use your data structures to prepare data for machine learning (feature vectors, normalized data)

### What You'll Learn:

This project will solidify your understanding of:
- When to use each data structure
- How to combine structures effectively
- Performance implications of your choices
- Real-world data processing patterns
- Writing clean, maintainable code

Remember: The best way to master data structures is to use them in a real project. This challenge gives you that opportunity while building something genuinely useful!
