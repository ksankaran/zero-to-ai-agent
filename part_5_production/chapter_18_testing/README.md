# Chapter 18: Testing and Evaluation

## System Check

Before we dive in, let's make sure you're all set up:

1. Open VS Code

2. Open your terminal (Terminal → New Terminal or `Ctrl+`` on Windows/Linux, `Cmd+`` on Mac)

3. Navigate to your project folder:

**On Windows:**
```
cd %USERPROFILE%\Desktop\ai_agents_complete
```

**On Mac/Linux:**
```
cd ~/Desktop/ai_agents_complete
```

4. Create a folder for this chapter and navigate into it:

**On Windows:**
```
mkdir part_5_production\chapter_18_testing
cd part_5_production\chapter_18_testing
```

**On Mac/Linux:**
```
mkdir -p part_5_production/chapter_18_testing
cd part_5_production/chapter_18_testing
```

5. Create a virtual environment for this chapter:

**On Windows:**
```
python -m venv venv
venv/Scripts/Activate.ps1
```

**On Mac/Linux:**
```
python -m venv venv
source venv/bin/activate
```

You should see (venv) at the beginning of your terminal prompt. Perfect! You're ready to go.

6. Install the required packages for Chapter 18:

> `part_5_production/chapter_18_testing/requirements.txt`

Or copy and create the file yourself:

```
# requirements.txt
pytest==9.0.2
pytest-asyncio==1.3.0
langgraph==1.0.4
langchain-core==1.2.0
langchain-openai==1.1.1
python-dotenv==1.2.1
httpx==0.28.1
numpy==2.3.5
scipy==1.16.3
```

Then install with:

```bash
pip install -r requirements.txt
```

This will install:
- `pytest` (9.0.2) - Python testing framework
- `pytest-asyncio` (1.3.0) - Async test support for pytest
- `langgraph` (1.0.4) - For building agent workflows with StateGraph
- `langchain-core` (1.2.0) - Core LangChain abstractions and interfaces
- `langchain-openai` (1.1.1) - For ChatOpenAI and OpenAIEmbeddings
- `python-dotenv` (1.2.1) - For loading environment variables from .env files
- `httpx` (0.28.1) - Async HTTP client (used in mocking examples)
- `numpy` (2.3.5) - For numerical operations (cosine similarity in evaluation)
- `scipy` (1.16.3) - For statistical tests (chi-squared in A/B testing)

7. Create your `.env` file with your API keys:

> `part_5_production/chapter_18_testing/.env.example`

Or copy and create the file yourself:

```
# .env
# OpenAI API Key (required)
# Get your key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here
```

Rename `.env.example` to `.env` and replace with your actual API key.

**Important:** Never commit your `.env` file to version control. Add it to `.gitignore`.

---

## Practice Exercises

### Section 18.1

**Exercise 1: Testing a Validation Tool**

Create a tool function called `validate_email` that checks if an email address is valid. It should return a dictionary with `valid` (boolean), `error` (string or None), and `normalized` (the email in lowercase). Write at least 5 unit tests covering valid emails, invalid emails, edge cases like empty strings, and emails with unusual but valid characters.

> `part_5_production/chapter_18_testing/exercise_1_18_1_solution.py`

**Exercise 2: Testing State Helpers**

Create a set of helper functions for managing a "shopping cart" state that includes `items` (list of dicts with name and quantity), `total` (float), and `coupon_code` (string or None). Write functions for `add_item`, `remove_item`, `apply_coupon`, and `calculate_total`. Write unit tests for each function, including edge cases like removing an item that doesn't exist or applying an invalid coupon.

> `part_5_production/chapter_18_testing/exercise_2_18_1_solution.py`

**Exercise 3: Mocking an API Tool**

You have a tool that calls a weather API to get the current temperature for a city. Write the tool function and then write tests using mocks that verify:
- The function correctly parses a successful API response
- The function handles a 404 (city not found) gracefully
- The function handles network timeouts gracefully
- The correct city name is passed to the API

> `part_5_production/chapter_18_testing/exercise_3_18_1_solution.py`

---

### Section 18.2

**Exercise 1: Testing a Multi-Node Workflow**

Create a simple order processing graph with three nodes: `validate_order` (checks if order data is valid), `calculate_total` (computes total with tax), and `confirm_order` (generates confirmation). Write integration tests that verify: (1) valid orders flow through all three nodes, (2) invalid orders stop at validation, and (3) state accumulates correctly through the workflow.

> `part_5_production/chapter_18_testing/exercise_1_18_2_solution.py`

**Exercise 2: Testing Branching Logic**

Build a graph that routes customer messages to different handlers based on sentiment (positive, negative, neutral). The routing should happen after a classification node. Write integration tests that verify each branch is taken for appropriate inputs, and that the correct handler is invoked. Use mocks to make tests deterministic.

> `part_5_production/chapter_18_testing/exercise_2_18_2_solution.py`

**Exercise 3: Testing Conversation Context**

Create a simple FAQ agent that answers questions differently based on conversation history. For example, if the user already asked about pricing, a follow-up question like "what about discounts?" should be understood in context. Write integration tests that verify context is maintained across turns and influences responses appropriately.

> `part_5_production/chapter_18_testing/exercise_3_18_2_solution.py`

---

### Section 18.3

**Exercise 1: Custom Evaluation Rubric**

Create an evaluation rubric for a customer service agent that rates responses on four criteria: accuracy (factual correctness), empathy (emotional tone), actionability (does it help solve the problem?), and policy compliance (stays within company guidelines). Build an LLMJudge-based evaluator that scores each criterion and returns detailed feedback.

> `part_5_production/chapter_18_testing/exercise_1_18_3_solution.py`

**Exercise 2: Comparative Evaluation**

Build an evaluator that compares two different agent responses to the same question and decides which is better. It should explain its reasoning and output a clear winner (or tie). This is useful for A/B testing different agent versions.

> `part_5_production/chapter_18_testing/exercise_2_18_3_solution.py`

**Exercise 3: Evaluation Dashboard**

Create a simple evaluation reporting function that takes a list of evaluation results and generates a summary report. The report should include: overall pass rate, breakdown by criterion, the worst-performing cases (for debugging), and trend information if historical data is available.

> `part_5_production/chapter_18_testing/exercise_3_18_3_solution.py`

---

## Challenge Project: Build a Quality Dashboard for Your Agent

### The Challenge

Create a comprehensive testing and evaluation system for an agent of your choice. This project integrates everything you've learned into a working quality management system.

### Requirements

**1. The Agent**

Either use an agent you've built in previous chapters or create a simple one for this exercise. A customer service agent or FAQ bot works well.

**2. Unit Test Suite**

Create unit tests covering:
- At least 3 tool functions
- State transformation logic
- Routing decisions
- At least one test with a mocked LLM

**3. Integration Test Suite**

Create integration tests covering:
- A complete happy-path workflow
- Error handling scenarios
- At least one multi-turn conversation test

**4. Evaluation Dataset**

Build a test dataset with:
- At least 20 test cases
- Cases organized by category
- Expected outputs or evaluation criteria for each
- A mix of easy, medium, and hard cases

**5. Evaluation Pipeline**

Implement an evaluation system that:
- Runs your agent against the test dataset
- Evaluates responses using at least two criteria
- Produces aggregate metrics (pass rate, average score)
- Identifies worst-performing cases

**6. Quality Report**

Generate a report showing:
- Overall metrics
- Breakdown by category
- Specific failures to investigate
- Trend data (if you run evaluation multiple times)

### Bonus Challenges

**Level 1**: Add an A/B testing capability that can compare two versions of a prompt

**Level 2**: Implement automated daily evaluation that logs results to a file

**Level 3**: Build a simple web dashboard that visualizes metrics over time

### Success Criteria

Your quality system should be able to:
- Tell you the current accuracy of your agent (overall and by category)
- Identify the specific cases where your agent struggles
- Detect if a change makes things better or worse
- Run automatically without manual intervention

This project transforms you from someone who builds agents to someone who builds *reliable* agents - and that's what production systems require.
