# Chapter 12: Tools and Function Calling

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
mkdir part_3_agents\chapter_12_tools_functions
cd part_3_agents\chapter_12_tools_functions
```

**On Mac/Linux:**
```bash
mkdir -p part_3_agents/chapter_12_tools_functions
cd part_3_agents/chapter_12_tools_functions
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

6. Install the required packages for Chapter 12:

► `part_3_agents/chapter_12_tools_functions/requirements.txt`

Or copy and create the file yourself:
```
# requirements.txt
langchain==1.1.3
langchain-openai==1.1.1
langchain-community==0.4.1
langchain-core==1.1.3
langchain-classic==1.0.0
langsmith==0.4.57
duckduckgo-search==8.1.1
ddgs==9.9.3
wikipedia-api==0.8.1
python-dotenv==1.2.1
pydantic==2.12.5
```

Then install with:
```bash
pip install -r requirements.txt
```

This will install:
- `langchain` (1.1.3) - core framework for building agents
- `langchain-openai` (1.1.1) - OpenAI integration for ChatGPT
- `langchain-community` (0.4.1) - community tools (DuckDuckGo, Wikipedia)
- `langchain-core` (1.1.3) - core abstractions for tools and prompts
- `langchain-classic` (1.0.0) - classic agents (create_react_agent, AgentExecutor)
- `langsmith` (0.4.57) - for pulling ReAct prompt templates
- `duckduckgo-search` (8.1.1) - web search capability for agents
- `ddgs` (9.9.3) - DuckDuckGo search for agent tools
- `wikipedia-api` (0.8.1) - Wikipedia integration for research tools
- `python-dotenv` (1.2.1) - for loading environment variables from .env files
- `pydantic` (2.12.5) - structured tool inputs and validation

7. Create your `.env` file with your API keys:

► `part_3_agents/chapter_12_tools_functions/.env.example`

Or copy and create the file yourself:
```
# .env
# OpenAI API Key (required)
# Get your key at: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# LangSmith API Key (required for Section 12.7)
# Get your key at: https://smith.langchain.com/ (Settings → API Keys)
LANGSMITH_API_KEY=ls-your-langsmith-api-key-here
```

Rename `.env.example` to `.env` and replace with your actual API keys.

**Important:** Never commit your `.env` file to version control. Add it to `.gitignore`.

---

## Troubleshooting

### Common Tool Issues (Section 12.1)

- **Problem:** "Why isn't the agent using my tool?"
  **Solution:** The LLM decides whether to use tools based on: the tool's name (make it clear!), the tool's description (be specific!), and the user's request (does it match the tool's purpose?).

- **Problem:** "The agent seems slow"
  **Solution:** When using tools, the agent is actually doing work! Search tool: Making real web requests. Calculator: Running computations. File tools: Actual I/O operations. This is normal!

- **Problem:** "Tool executed but agent gave wrong answer"
  **Solution:** Check that your tool returns clear, string responses that the LLM can understand.

### Custom Tool Issues (Section 12.2)

- **Problem:** "Tool function crashes and breaks the agent"
  **Solution:** Always wrap your tool logic in try/except blocks! Return error messages as strings rather than raising exceptions.

- **Problem:** "LLM passes wrong format to tool"
  **Solution:** Your description needs examples! Instead of "Enter date", use "Enter date in format YYYY-MM-DD like 2024-03-15".

- **Problem:** "Tool returns too much data"
  **Solution:** Keep responses concise. If you must return lots of data, summarize it and offer details only if asked.

### Built-in Tool Issues (Section 12.3)

- **Problem:** "ImportError: cannot import name 'ToolName'"
  **Solution:** Some tools moved between packages. Use `from langchain_community.tools import ...` for community tools, `from langchain_experimental.tools import ...` for experimental ones.

- **Problem:** "Search returns too much/too little"
  **Solution:** Many tools have configuration options: `DuckDuckGoSearchRun(max_results=3)`, `WikipediaAPIWrapper(doc_content_chars_max=500)`.

- **Problem:** "Python REPL doesn't work"
  **Solution:** Make sure you have `langchain-experimental` installed. Use in a safe environment only!

### Function Calling Issues (Section 12.4)

- **Problem:** "This model doesn't support function calling"
  **Solution:** Not all models support function calling! Supported: OpenAI GPT-3.5-turbo and GPT-4, Anthropic Claude-3 models.

- **Problem:** "Tool calls are empty even though they should work"
  **Solution:** Make sure you're using `bind_tools()` not just passing tools to the agent.

- **Problem:** "Arguments don't match function signature"
  **Solution:** Use Pydantic models or clear type hints. The clearer your function signature, the better the LLM understands it!

### Tool Selection Issues (Section 12.5)

- **Problem:** "Agent always picks the same tool"
  **Solution:** Your tool descriptions might be too similar or one might be too generic. Make descriptions more specific and differentiate use cases clearly.

- **Problem:** "Agent uses tools in wrong order"
  **Solution:** Tools should indicate dependencies in their descriptions. For example: "Use after getting date from get_current_date tool"

- **Problem:** "Too many tool calls for simple tasks"
  **Solution:** Check if your tools are too granular. Sometimes combining related functionality into one tool is better than having many micro-tools.

### Error Handling Issues (Section 12.6)

- **Problem:** "Tool returns 'None' on error"
  **Solution:** Always return a string! Even on error: `return "Error: Operation failed"` not `return None`.

- **Problem:** "Errors are too technical for users"
  **Solution:** Translate technical errors. Use "Unable to connect to service. Please try again." instead of "ConnectionRefusedError: [Errno 111]".

- **Problem:** "Tool gets stuck retrying forever"
  **Solution:** Always set maximum retry attempts and timeouts: `MAX_RETRIES = 3` and `TIMEOUT = 5`.

---

## Practice Exercises

### Section 12.1

**Exercise 1: Tool or No Tool?**

For each scenario below, decide whether you need a tool or if pure LLM is sufficient. Explain why!

1. Write a haiku about summer
2. Get today's date
3. Explain quantum physics
4. Check if a file exists
5. Translate 'hello' to Spanish
6. Find the latest news about AI
7. Generate a business name
8. Calculate compound interest

For each one, answer:
- **Tool or No Tool?**
- **Why?** What makes you choose one over the other?
- **If tool needed:** What kind of tool would you use?
- **If no tool:** What would happen if you tried to use a tool anyway?

► `part_3_agents/chapter_12_tools_functions/exercise_1_12_1_solution.md`

**Exercise 2: Trace the Tool Flow**

Given this conversation, trace what happens at each step behind the scenes:
```
User: "Search for information about LangChain and calculate 15% of 2000"

AI: "I'll help you with both tasks.

LangChain is a framework for developing applications powered by
language models. It was created by Harrison Chase and provides
tools for building context-aware reasoning applications.

15% of 2000 is 300."
```

Write out each step that happened:
- Step 1: User sends message with two requests
- Step 2: AI recognizes... [continue]
- Step 3: ...
- Step 4: ...

Think about:
- How did the AI know to use two different tools?
- Which tool was called first? Why?
- How did the AI combine the results into one response?

► `part_3_agents/chapter_12_tools_functions/exercise_2_12_1_solution.md`

**Exercise 3: Design a Tool Set**

You're building an AI assistant for a small business (a local bakery). Design 5 tools it would need:

For each tool, describe:
- **Tool name:** What you'd call it
- **Purpose:** What it does
- **When used:** Example user requests that would trigger it
- **Inputs:** What information it needs
- **Outputs:** What it returns
- **Safety considerations:** What could go wrong and how to prevent it

► `part_3_agents/chapter_12_tools_functions/exercise_3_12_1_solution.md`

---

### Section 12.2

**Exercise 1: Unit Converter Tool (Easy)**
Create a tool that converts between units (meters to feet, kg to pounds, etc.):
- Handle at least 3 types of conversions
- Parse input like "5 meters to feet"
- Return clear, formatted results
- Handle invalid conversions gracefully

► `part_3_agents/chapter_12_tools_functions/exercise_1_12_2_solution.py`

**Exercise 2: Text Processor Tool Suite (Medium)**
Build three related tools that work together:
1. `text_stats`: Returns word count, sentence count, average word length
2. `extract_keywords`: Finds the 5 most common meaningful words
3. `summarize`: Creates a one-sentence summary

Make sure the outputs of one can be inputs to another!

► `part_3_agents/chapter_12_tools_functions/exercise_2_12_2_solution.py`

**Exercise 3: Smart File Manager (Hard)**
Create a tool that manages a simple file system:
- Commands: "create file.txt with [content]", "read file.txt", "list files", "delete file.txt"
- Store files in a dictionary (simulate a file system)
- Add safety: prevent overwriting without confirmation
- Return user-friendly messages
- Bonus: Add a search function to find files containing specific text

► `part_3_agents/chapter_12_tools_functions/exercise_3_12_2_solution.py`

---

### Section 12.3

**Exercise 1: Tool Explorer (Easy)**
Test each tool type and document what it returns:
- Use DuckDuckGo to search for 3 different types of queries (news, facts, tutorials)
- Use Wikipedia to look up 3 topics (person, place, concept)
- Compare the type and quality of information each provides
- Which tool would be better for which type of question?

► `part_3_agents/chapter_12_tools_functions/exercise_1_12_3_solution.py`

**Exercise 2: Research Workflow (Medium)**
Create a research workflow using tools directly (not with an agent):
- Pick a technology topic (like "quantum computing" or "blockchain")
- Use Wikipedia to get foundational information
- Use DuckDuckGo to find recent developments
- Use file tools to create a structured report
- Save the report with clear sections for "Background" and "Recent News"

► `part_3_agents/chapter_12_tools_functions/exercise_2_12_3_solution.py`

**Exercise 3: Data Processing Pipeline (Hard)**
Build a data processing workflow:
- Use the Python REPL tool to generate sample data (like 100 random numbers)
- Use the Python REPL to calculate statistics (mean, median, mode, std deviation)
- Create a formatted report of the analysis
- Use file tools to save both the raw data and the analysis report
- Test edge cases: What happens with empty data? Invalid calculations?

► `part_3_agents/chapter_12_tools_functions/exercise_3_12_3_solution.py`

---

### Section 12.4

**Exercise 1: Weather Assistant with Units (Easy)**
Create a weather tool that:
- Accepts city and temperature unit (Celsius/Fahrenheit)
- Uses function calling for structured inputs
- Returns formatted weather data
- Test with: "What's the weather in London in Celsius?"

> **New Type Hint: `Literal`**
> The solution uses `Literal` from the `typing` module with Pydantic. `Literal["celsius", "fahrenheit", "kelvin"]` means the value must be exactly one of those strings - nothing else is allowed.

► `part_3_agents/chapter_12_tools_functions/exercise_1_12_4_solution.py`

**Exercise 2: Multi-Step Calculator (Medium)**
Build a calculator that can:
- Handle multiple operations in one request
- Use parallel function calls for independent calculations
- Return all results together
- Test with: "Calculate 15*4, 100/5, and 78+22"

► `part_3_agents/chapter_12_tools_functions/exercise_2_12_4_solution.py`

**Exercise 3: Smart Task Manager (Hard)**
Create a task management system with function calling:
- Add tasks with title, priority, and due date
- List tasks (all, by priority, by date)
- Mark tasks complete
- Use structured inputs for all operations
- Handle errors gracefully (invalid dates, missing tasks)
- Test with complex requests like "Add a high priority task to call mom tomorrow"

► `part_3_agents/chapter_12_tools_functions/exercise_3_12_4_solution.py`

---

### Section 12.5

**Exercise 1: Tool Naming Challenge (Easy)**
You have 5 search-related functions. Create clear, distinctive names and descriptions for each:
- General web search
- News search
- Academic paper search
- Local business search
- Social media search

Make sure the agent would never confuse them!

► `part_3_agents/chapter_12_tools_functions/exercise_1_12_5_solution.py`

**Exercise 2: Loop Prevention (Medium)**
Create a scenario with 3 tools where one might cause loops:
- A question-answering tool
- A clarification tool (potential loop risk!)
- A definition tool

Implement strategies to prevent the agent from getting stuck asking for clarification repeatedly. Test with various queries.

► `part_3_agents/chapter_12_tools_functions/exercise_2_12_5_solution.py`

**Exercise 3: Complex Orchestration (Hard)**
Build a travel planning system with 6+ tools:
- Date/time tools
- Weather checking
- Flight searching
- Hotel searching
- Activity recommendations
- Itinerary creation

Create an agent that can handle: "Plan a 3-day trip to Tokyo next month"
The agent should orchestrate all tools to create a complete plan!

► `part_3_agents/chapter_12_tools_functions/exercise_3_12_5_solution.py`

---

### Section 12.6

**Exercise 1: Robust URL Fetcher (Easy)**
Create a tool that fetches webpage content with:
- URL validation (must start with http:// or https://)
- Timeout handling (max 5 seconds)
- Retry logic (up to 2 retries)
- Helpful error messages for common issues

Test with valid URLs, invalid URLs, and slow/failing endpoints.

► `part_3_agents/chapter_12_tools_functions/exercise_1_12_6_solution.py`

**Exercise 2: Smart Data Processor (Medium)**
Build a tool that processes CSV data with multiple fallback strategies:
- Try to parse as CSV
- If that fails, try TSV (tab-separated)
- If that fails, try space-separated
- Return helpful error with sample of expected format

Include validation for minimum/maximum rows and columns.

► `part_3_agents/chapter_12_tools_functions/exercise_2_12_6_solution.py`

**Exercise 3: Resilient API Client (Hard)**
Create a tool that calls an external API with:
- Rate limiting (max 10 calls per minute)
- Exponential backoff on failures
- Circuit breaker pattern (stop trying after 5 consecutive failures)
- Cache successful responses for 5 minutes
- Detailed logging of all attempts

Simulate various failure scenarios and verify your tool handles them all.

► `part_3_agents/chapter_12_tools_functions/exercise_3_12_6_solution.py`

---

## Challenge Project: Build a Personal Assistant Agent

Create a comprehensive personal assistant that can:

### Required Features:

**1. Time Management**
- Tell current time in different timezones
- Calculate time differences
- Set reminders (save to file)

**2. Information Retrieval**
- Search the web for current info
- Look up facts on Wikipedia
- Provide definitions

**3. Task Management**
- Create todo lists (save to file)
- Mark tasks complete
- Show pending tasks

**4. Calculations**
- Basic math operations
- Unit conversions (meters to feet, etc.)
- Currency conversion (simulated)

**5. Weather & Location**
- Get weather for any city
- Compare weather between cities
- Suggest clothing based on weather

► `part_3_agents/chapter_12_tools_functions/personal_assistant_solution.py`

### Example Interaction:

```
User: "What's the weather in Paris and New York, which is warmer,
      and add 'pack umbrella' to my todo list if either is rainy"

Agent: [Uses weather tool twice, compares, conditionally uses todo tool]
```

This project brings together EVERYTHING from Chapter 12. Build it, and you'll have created a genuinely useful AI assistant!
