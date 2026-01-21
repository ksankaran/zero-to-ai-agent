# Chapter 14: Introduction to LangGraph

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
mkdir part_4_langgraph\chapter_14_langgraph_intro
cd part_4_langgraph\chapter_14_langgraph_intro
```

**On Mac/Linux:**
```bash
mkdir -p part_4_langgraph/chapter_14_langgraph_intro
cd part_4_langgraph/chapter_14_langgraph_intro
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

6. Install the required packages for Chapter 14:

► `part_4_langgraph/chapter_14_langgraph_intro/requirements.txt`

Or copy and create the file yourself:
```
# requirements.txt
langgraph==1.0.4
langchain-openai==1.1.1
python-dotenv==1.2.1
```

Then install with:
```
pip install -r requirements.txt
```

This will install:
- `langgraph` (1.0.4) - the core LangGraph framework for building graph-based agents
- `langchain-openai` (1.1.1) - for OpenAI LLM integration with LangChain
- `python-dotenv` (1.2.1) - for managing your API keys securely

7. Create your `.env` file with your API keys:

► `part_4_langgraph/chapter_14_langgraph_intro/.env.example`

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

### Section 14.1

**Exercise 1: Identify Chain Limitations**

Think of an AI application you'd like to build (or pick one: email assistant, study tutor, recipe suggester). Write down:

1. What steps would it need to perform?
2. Where might it need to loop back (retry or refine)?
3. Where might it need to branch (handle different cases)?
4. What information would it need to track across steps?

► See `Chapter_14.1_Solutions.md` for a sample answer using a Smart Study Tutor.

**Exercise 2: Flowchart Design**

Draw a flowchart (on paper or describe it in text) for a "Smart Email Responder" that:

- Reads an incoming email
- Classifies it (urgent, normal, spam)
- For urgent: drafts an immediate response
- For normal: adds to a queue
- For spam: archives it
- For drafted responses: gets human approval
- If human requests changes: loops back to redraft

Identify which parts would be impossible or messy with a simple chain.

► See `Chapter_14.1_Solutions.md` for a sample flowchart and analysis.

**Exercise 3: Analyze the Pattern**

Look at this pseudo-code:

```python
def smart_assistant(task):
    plan = create_plan(task)

    while not is_complete(plan):
        next_step = get_next_step(plan)
        result = execute_step(next_step)

        if result.failed:
            if result.retryable:
                continue  # Try same step again
            else:
                plan = revise_plan(plan, result.error)
        else:
            update_plan(plan, result)

    return summarize_results(plan)
```

Explain why this would be difficult with simple chains. Identify: the loops, the branching points, and what state needs to persist.

► See `Chapter_14.1_Solutions.md` for a detailed breakdown of loops, branches, and state requirements.

---

### Section 14.2

**Exercise 1: Pattern Recognition**

For each scenario, identify which pattern(s) would be most appropriate:

1. An agent that translates a document from English to Spanish
2. An agent that keeps asking clarifying questions until it understands the user's request
3. An agent that checks the weather in three cities simultaneously
4. An agent that writes code, runs tests, and fixes bugs until all tests pass
5. An agent that drafts a legal contract and requires lawyer approval before finalizing

► See `Chapter_14.2_Solutions.md` for pattern identification with explanations.

**Exercise 2: Design a Recipe Agent**

Design a graph for a cooking assistant agent that:
- Takes a dish the user wants to make
- Checks what ingredients the user has available
- Finds a suitable recipe (might need to search multiple times for alternatives)
- Adjusts the recipe based on available ingredients
- Generates step-by-step cooking instructions
- Can answer questions during cooking (loops back to handle questions)

Sketch the graph and identify: the nodes, the decision points, any loops, and what state you'd need.

► See `Chapter_14.2_Solutions.md` for a complete graph design with nodes, decisions, loops, and state.

**Exercise 3: Identify the State**

For the customer service agent designed in this section, list all the pieces of information that should be in the state. For each piece, explain which node(s) would write to it and which node(s) would read from it.

► See `Chapter_14.2_Solutions.md` for a detailed state table showing read/write relationships.

---

### Section 14.3

**Exercise 1: Environment Exploration**

Run `pip list` in your terminal and find all the packages that were installed as dependencies of LangGraph. Count how many there are. Then look up what three of them do (pick ones with interesting names).

► See `Chapter_14.3_Solutions.md` for a discussion of interesting dependencies like tiktoken, pydantic, and tenacity.

**Exercise 2: API Key Security**

Explain in your own words why we use a `.env` file instead of putting the API key directly in our code. What could go wrong if you accidentally committed an API key to a public GitHub repository?

► See `Chapter_14.3_Solutions.md` for a comprehensive discussion of API key security risks.

**Exercise 3: Create a Setup Checker**

Combine all three verification scripts into one comprehensive `setup_check.py` that:
- Checks all package installations
- Verifies the API key exists and has the right format
- Tests the API connection
- Reports a summary at the end with overall pass/fail

Make it user-friendly with clear instructions if anything fails.

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_3_14_3_solution.py`

---

### Section 14.4

**Exercise 1: Design a State**

Design the state TypedDict for a "Code Review Agent" that:
- Receives code to review
- Identifies issues (could be multiple)
- Suggests fixes for each issue
- Tracks which issues have been addressed
- Knows when the review is complete

Think about: What fields do you need? Which should be lists? Which need the `add` reducer?

► See `Chapter_14.4_Solutions.md` for the complete state design with explanations.

**Exercise 2: Write the Nodes**

Using the state you designed in Exercise 1, write pseudocode (or real code) for three nodes:
- `analyze_code`: Looks at the code and identifies issues
- `suggest_fix`: Takes one issue and suggests a fix
- `check_complete`: Determines if all issues are addressed

Focus on: What does each node read from state? What does it write back?

► See `Chapter_14.4_Solutions.md` for complete node implementations.

**Exercise 3: Draw the Graph**

Sketch the graph (on paper or ASCII art) for the Code Review Agent. Include:
- Where it starts
- The flow between nodes
- Any conditional edges (what are the conditions?)
- Where loops occur
- Where it ends

Then write the LangGraph code to build this graph structure (just the graph building part - nodes can be placeholder functions).

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_3_14_4_solution.py`

---

### Section 14.5

**Exercise 1: Add Draft History**

Modify the writer to keep a history of all drafts, not just the current one. You'll need to:
- Change the state to use `Annotated[list, add]` for drafts
- Update nodes to append drafts rather than replace
- Display all versions at the end

This lets you see how the writing evolved through revisions.

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_1_14_5_solution.py`

**Exercise 2: Quality Scoring**

Add a numeric quality score (1-10) to the process:
- Add a `quality_score` field to state
- Modify `critique_draft` to also output a score
- Update `should_continue` to use the score (stop when score >= 8)
- Display the score progression at the end

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_2_14_5_solution.py`

**Exercise 3: Different Writing Styles**

Add a `style` parameter that changes how the writer works:
- "formal": Professional, business-like tone
- "casual": Friendly, conversational tone
- "creative": Artistic, expressive tone

Modify the prompts in each node to respect the chosen style. Test with the same topic but different styles.

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_3_14_5_solution.py`

---

### Section 14.6

**Exercise 1: Email Classifier**

Build a graph that classifies incoming emails and routes them to specialized handlers:
- URGENT → Generate quick acknowledgment
- MEETING → Extract date, time, participants
- NEWSLETTER → Archive it
- PERSONAL → Flag for personal review
- SPAM → Delete it

Your graph should have:
- One classification node
- Five different handler nodes
- A routing function that maps categories to handlers

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_1_14_6_solution.py`

**Exercise 2: Multi-Stage Interview**

Create an interview bot with three stages:
- Stage 1: Basic info (name, background)
- Stage 2: Technical questions (different paths for engineer vs designer)
- Stage 3: Behavioral questions

Requirements:
- Only advance when current stage is complete
- Engineers and designers get different technical questions
- End with a summary of the interview

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_2_14_6_solution.py`

**Exercise 3: Retry with Backoff**

Enhance a research assistant to handle poor-quality results:
- If search quality is LOW, retry with a modified query
- Track retries per search (max 2 retries)
- If still low after retries, move on to next search
- Add `retry_count` and `current_quality` to state

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_3_14_6_solution.py`

---

### Section 14.7

**Exercise 1: Add Debugging to the Ticket Router**

Take the ticket router from section 14.6 and add:
- Debug output for every node
- State tracking
- A loop counter safety valve
- Graph visualization at startup

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_1_14_7_solution.py`

**Exercise 2: Find the Bug**

Here's a buggy graph with 3 bugs. Use debugging techniques to find and fix:
1. List not accumulating (missing `Annotated[list, add]`)
2. KeyError on state access (missing `.get()` with default)
3. Routing mismatch (return values don't match mapping keys)

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_2_14_7_solution.py`

**Exercise 3: Build a Debug Dashboard**

Create a function that produces a summary report:
- Total nodes visited
- Time spent
- State changes for each field
- Fields that never changed
- Routing decisions made

► `part_4_langgraph/chapter_14_langgraph_intro/exercise_3_14_7_solution.py`

---

## Challenge Project: Build a Multi-Stage Document Analyzer

Put everything together by building a sophisticated document analysis agent.

> `part_4_langgraph/chapter_14_langgraph_intro/document_analyzer_challenge.py`

### Requirements:
- At least 6 nodes
- Multi-way branching based on document type (4+ branches)
- A quality-check loop (generate → evaluate → maybe regenerate)
- Maximum iteration limits

### State Must Include:
- Document text and classification
- Extracted information (`Annotated[list, add]`)
- Quality scores and iteration counters

### Document Type Handlers:
- **Technical**: Extract methods, findings, technologies
- **Business**: Extract metrics, decisions, action items
- **Legal**: Extract parties, obligations, dates
- **Academic**: Extract thesis, methodology, conclusions

### Evaluation Criteria:
- Does classification correctly identify document types?
- Does routing send documents to the correct extraction node?
- Does the quality loop retry when extraction is poor?
- Does it respect the maximum iteration limit?
- Are extracted items accumulating (not replacing)?

This project uses everything from Chapter 14: state design, multiple nodes, multi-way branching, looping, and debugging.
