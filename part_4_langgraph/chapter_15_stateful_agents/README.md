# Chapter 15: Building Stateful Agents

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
mkdir part_4_langgraph\chapter_15_stateful_agents
cd part_4_langgraph\chapter_15_stateful_agents
```

**On Mac/Linux:**
```bash
mkdir -p part_4_langgraph/chapter_15_stateful_agents
cd part_4_langgraph/chapter_15_stateful_agents
```

5. Activate your virtual environment:

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

6. Install the required packages for Chapter 15:

> `part_4_langgraph/chapter_15_stateful_agents/requirements.txt`

Or copy and create the file yourself:
```
# requirements.txt
langgraph==1.0.4
langgraph-checkpoint-sqlite==3.0.0
langchain-openai==1.1.1
pydantic==2.12.5
python-dotenv==1.2.1
```

Then install with:
```bash
pip install -r requirements.txt
```

This will install:
- `langgraph` (1.0.4) - core framework for building stateful graphs (used in all sections)
- `langgraph-checkpoint-sqlite` (3.0.0) - SQLite persistence for state checkpointing (section 15.4)
- `langchain-openai` (1.1.1) - OpenAI integration for LLM-powered agents
- `pydantic` (2.12.5) - data validation for state schemas (section 15.2)
- `python-dotenv` (1.2.1) - for managing environment variables and API keys

7. Create your `.env` file with your API keys:

> `part_4_langgraph/chapter_15_stateful_agents/.env.example`

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

## Troubleshooting

**Problem:** "ModuleNotFoundError: No module named 'langgraph'"
**Solution:** Make sure your virtual environment is activated and run `pip install langgraph` again

**Problem:** Virtual environment not activating
**Solution:** You may need to create it first with `python -m venv venv`

---

## Practice Exercises

### Section 15.1

**Exercise 1: Conversation Counter**

Build a simple agent that:
- Tracks how many times a user has talked to it
- Greets returning users differently from new users
- Uses MemorySaver for persistence during the session

Try invoking it multiple times with the same thread_id and see the count increase.

> `part_4_langgraph/chapter_15_stateful_agents/exercise_1_15_1_solution.py`

**Exercise 2: Multi-User Tracker**

Create an agent that:
- Supports multiple users with separate thread_ids
- Tracks each user's visit count separately
- Demonstrates that thread_ids isolate state completely

Run it with "alice" and "bob" thread_ids and verify they have separate counts.

> `part_4_langgraph/chapter_15_stateful_agents/exercise_2_15_1_solution.py`

**Exercise 3: State History Explorer**

Build a 3-node workflow that:
- Each node adds something to the state
- After running, use `get_state_history()` to print all snapshots
- Show how state evolved through the graph

This helps you understand how checkpointing captures every step.

> `part_4_langgraph/chapter_15_stateful_agents/exercise_3_15_1_solution.py`

---

### Section 15.2

**Exercise 1: Validated User Profile**

Create a Pydantic model for a user profile with:
- Username (3-20 characters, alphanumeric only)
- Email (valid email format)
- Age (optional, but if provided must be 13-120)
- Membership level (enum: "free", "basic", "premium")

Test it with both valid and invalid data.

> `part_4_langgraph/chapter_15_stateful_agents/exercise_1_15_2_solution.py`

**Exercise 2: Chat Message Validation**

Build a LangGraph node that:
- Accepts raw message input
- Validates it with Pydantic (role must be "user" or "assistant", content not empty)
- Returns the validated message or an error

> `part_4_langgraph/chapter_15_stateful_agents/exercise_2_15_2_solution.py`

**Exercise 3: Order State Schema**

Design a complete state schema for an order processing agent:
- Order with id, items list, total price, and status
- Items with name, quantity (>0), and price (>0)
- Status enum (pending, processing, shipped, delivered, cancelled)
- Validation that total equals sum of item prices x quantities

> `part_4_langgraph/chapter_15_stateful_agents/exercise_3_15_2_solution.py`

---

### Section 15.3

**Exercise 1: Deduplicating Reducer**

Create a custom reducer that:
- Accumulates messages like `add` does
- But removes duplicates (same content)
- Preserves the order (first occurrence wins)

Test it with a graph where multiple nodes might add the same message.

> `part_4_langgraph/chapter_15_stateful_agents/exercise_1_15_3_solution.py`

**Exercise 2: Priority Queue Reducer**

Build a reducer that:
- Maintains a sorted list of tasks by priority
- Each task is `{"task": str, "priority": int}`
- Higher priority items come first
- New items are inserted in the correct position

> `part_4_langgraph/chapter_15_stateful_agents/exercise_2_15_3_solution.py`

**Exercise 3: Change Tracker**

Create a state schema that:
- Tracks the current value of several fields
- Also tracks a "changelog" of what changed and when
- Each node automatically logs its changes to the changelog

> `part_4_langgraph/chapter_15_stateful_agents/exercise_3_15_3_solution.py`

---

### Section 15.4

**Exercise 1: Multi-User Chat System**

Build a chat system that:
- Supports multiple users with separate thread IDs
- Persists all conversations to SQLite
- Can list all conversations for a given user
- Shows message count and last activity per conversation

> `part_4_langgraph/chapter_15_stateful_agents/exercise_1_15_4_solution.py`

**Exercise 2: Checkpoint Cleanup Utility**

Create a maintenance utility that:
- Reports total checkpoints and storage size
- Prunes old checkpoints (keep only last N per thread)
- Runs database VACUUM to reclaim space
- Shows before/after statistics

> `part_4_langgraph/chapter_15_stateful_agents/exercise_2_15_4_solution.py`

**Exercise 3: Conversation Export Tool**

Build export/import functionality:
- Export a conversation to JSON file
- Import JSON back into a new thread
- Support "forking" (copy conversation to new thread)
- Preserve all metadata through export/import

> `part_4_langgraph/chapter_15_stateful_agents/exercise_3_15_4_solution.py`

---

### Section 15.5

**Exercise 1: Smart Retry Decorator**

Create an improved `@with_retry` decorator that:
- Accepts a `RetryPolicy` object for configuration
- Only retries specific exception types
- Logs each retry attempt with timestamp
- Returns metadata about retries alongside the result

> `part_4_langgraph/chapter_15_stateful_agents/exercise_1_15_5_solution.py`

**Exercise 2: Circuit Breaker Pattern**

Implement a circuit breaker that:
- Tracks failure rate over recent calls
- "Opens" (stops calling) when failure rate exceeds threshold
- Automatically "closes" (resumes) after a cooldown period
- Integrate it with a LangGraph node

> `part_4_langgraph/chapter_15_stateful_agents/exercise_2_15_5_solution.py`

**Exercise 3: Retry Dashboard**

Build a simple monitoring system that:
- Tracks retry statistics across all nodes
- Reports which nodes fail most often
- Shows average retry count per successful operation
- Alerts when retry rate exceeds normal levels

> `part_4_langgraph/chapter_15_stateful_agents/exercise_3_15_5_solution.py`

---

### Section 15.6

**Exercise 1: Multi-Source Aggregator**

Build an agent that:
- Queries 4 different "data sources" (simulate with functions)
- 2 sources randomly fail
- Aggregates successful results
- Reports which sources failed and why
- Returns a confidence score based on how many succeeded

> `part_4_langgraph/chapter_15_stateful_agents/exercise_1_15_6_solution.py`

**Exercise 2: Fallback Chain**

Create a node with a chain of fallbacks:
- Try primary API (fails 70% of the time)
- If that fails, try secondary API (fails 40% of the time)
- If that fails, try cache (always succeeds but data is "stale")
- Track which source ultimately provided the data

> `part_4_langgraph/chapter_15_stateful_agents/exercise_2_15_6_solution.py`

**Exercise 3: Graceful Feature Degradation**

Build a "document analyzer" that:
- Always extracts word count (core feature)
- Optionally analyzes sentiment (fails sometimes)
- Optionally extracts keywords (fails sometimes)
- Optionally summarizes (fails sometimes)
- Returns whatever it could compute with clear status for each

> `part_4_langgraph/chapter_15_stateful_agents/exercise_3_15_6_solution.py`

---

### Section 15.7

**Exercise 1: State Diff Viewer**

Build a tool that:
- Compares two state snapshots
- Shows what changed between them (added, removed, modified)
- Formats the diff in a readable way
- Highlights significant changes

> `part_4_langgraph/chapter_15_stateful_agents/exercise_1_15_7_solution.py`

**Exercise 2: Performance Dashboard**

Create a monitoring dashboard that tracks:
- Node execution counts
- Average time per node
- Success/failure rates per node
- Slowest nodes ranking
- Print a formatted report after each run

> `part_4_langgraph/chapter_15_stateful_agents/exercise_2_15_7_solution.py`

**Exercise 3: Alert System**

Build a simple alerting system that:
- Monitors metrics against thresholds
- Triggers alerts when thresholds exceeded (e.g., error rate > 10%)
- Tracks alert history
- Supports different severity levels (warning, critical)

> `part_4_langgraph/chapter_15_stateful_agents/exercise_3_15_7_solution.py`
