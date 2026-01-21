# Chapter 17: Advanced LangGraph Patterns

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
mkdir part_4_langgraph\chapter_17_advanced_patterns
cd part_4_langgraph\chapter_17_advanced_patterns
```

**On Mac/Linux:**
```
mkdir -p part_4_langgraph/chapter_17_advanced_patterns
cd part_4_langgraph/chapter_17_advanced_patterns
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

You should see `(venv)` at the beginning of your terminal prompt. Perfect! You're ready to go.

6. Install the required packages for Chapter 17:

> `part_4_langgraph/chapter_17_advanced_patterns/requirements.txt`

Or copy and create the file yourself:

```
# requirements.txt
langgraph==1.0.4
langchain-openai==1.1.1
python-dotenv==1.2.1
tenacity==9.1.2
```

Then install with:

```bash
pip install -r requirements.txt
```

This will install:
- `langgraph` (1.0.4) - for building agent workflows with StateGraph, streaming, parallel execution, subgraphs, and human-in-the-loop patterns
- `langchain-openai` (1.1.1) - for ChatOpenAI LLM integration
- `python-dotenv` (1.2.1) - for loading environment variables from .env files
- `tenacity` (9.1.2) - for retry logic with exponential backoff in production patterns

7. Create your `.env` file with your API keys:

> `part_4_langgraph/chapter_17_advanced_patterns/.env.example`

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

### Section 17.1

**Exercise 1: Expense Approval System**

Build a workflow where:
- Expenses under $100 are auto-approved (no interrupt)
- Expenses $100-$1000 need manager approval
- Expenses over $1000 need manager AND finance approval
- Rejected expenses can be revised and resubmitted

Requirements:
- Track who approved at each stage
- Allow adding notes with approval/rejection
- Limit to 3 revision attempts
- Use `interrupt()` for human approval points

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_1_17_1_solution.py`

**Exercise 2: Content Moderation Pipeline**

Create a content moderation system that:
- AI first screens content for obvious violations
- Borderline content triggers `interrupt()` for human review
- Humans can approve, reject, or escalate
- Escalated content goes to senior moderators (another interrupt)

Requirements:
- Different severity levels (warning, removal, ban)
- Show AI's confidence score in the interrupt payload
- Allow moderators to override AI recommendations
- Track all decisions in an audit log

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_2_17_1_solution.py`

**Exercise 3: Interview Scheduling Assistant**

Build an interview scheduling workflow where:
- AI proposes time slots
- `interrupt()` for candidate to select preferred times
- `interrupt()` for interviewer to confirm
- Either party can request rescheduling

Requirements:
- Handle conflicts and unavailability
- Use interrupt payloads to present options clearly
- Allow up to 2 reschedule requests
- Track the full scheduling history

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_3_17_1_solution.py`

---

### Section 17.2

**Exercise 1: Research Assistant with Progress**

Build a research workflow that:
- Takes a topic and generates 3 questions about it
- Researches each question (simulated with LLM calls)
- Streams progress for each research step ("Researching question 1/3...")
- Compiles findings into a final report
- Streams the final report token-by-token

Requirements:
- Use `StreamWriter` for progress updates
- Use `astream_events` for token streaming
- Show percentage completion during research phase

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_1_17_2_solution.py`

**Exercise 2: File Processor Simulation**

Create a workflow that simulates processing multiple files:
- Accept a list of "filenames"
- Process each file with a progress bar
- Show status updates: "Validating...", "Processing...", "Saving..."
- Report any "errors" encountered (simulate randomly)
- Stream a summary report at the end

Requirements:
- Use custom streaming for progress bar effect
- Show `[====------] 40%` style progress
- Handle simulated errors gracefully
- Final summary shows success/failure counts

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_2_17_2_solution.py`

**Exercise 3: Multi-Step Form Validator**

Build a form validation workflow that:
- Takes form data (name, email, phone, address)
- Validates each field sequentially
- Streams validation status for each field
- Uses LLM to check if address looks valid
- Returns validation results with helpful messages

Requirements:
- Stream "Validating email..." type messages
- Show checkmark or X for each field as validated
- Stream the LLM's address analysis token-by-token
- Final summary shows all validation results

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_3_17_2_solution.py`

---

### Section 17.3

**Exercise 1: Multi-Source Fact Checker**

Build a fact-checking system that:
- Takes a claim to verify
- Searches 4 different "sources" in parallel (simulate with different LLM prompts)
- Each source rates the claim's accuracy (1-10) with reasoning
- Aggregates ratings and provides a final verdict with confidence level

Requirements:
- Use fan-out/fan-in for parallel searches
- Calculate average rating and standard deviation
- Final verdict should note if sources disagree significantly

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_1_17_3_solution.py`

**Exercise 2: Parallel Document Analyzer**

Create a document analysis pipeline that:
- Takes a list of documents
- For each document in parallel: extract key themes, identify sentiment, find action items
- Combines all results into a comprehensive report
- Groups similar themes across documents

Requirements:
- Use `Send` for dynamic parallelization
- Each document analysis should return structured data
- Final report should deduplicate and rank themes by frequency

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_2_17_3_solution.py`

**Exercise 3: Competitive Analysis System**

Build a system that analyzes competitors in parallel:
- Takes a company name and list of competitors
- For each competitor in parallel: analyze strengths, weaknesses, market position
- Generates a comparative matrix
- Produces strategic recommendations

Requirements:
- Use `Send` to handle variable number of competitors
- Each analysis should follow a consistent structure
- Final output should include a ranking

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_3_17_3_solution.py`

---

### Section 17.4

**Exercise 1: Content Processing Pipeline**

Build a modular content processing system with these subgraphs:
- **InputValidator** - Checks content length, detects language
- **ContentEnricher** - Adds metadata, extracts entities
- **OutputFormatter** - Formats for different outputs (JSON, Markdown, plain text)

Requirements:
- Each subgraph should be independently testable
- Parent graph should compose them sequentially
- Use shared state schema
- Add a configuration option to skip enrichment

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_1_17_4_solution.py`

**Exercise 2: Multi-Format Translator**

Create a translation system using subgraphs with different state schemas:
- **Parent state**: `source_text`, `source_lang`, `target_langs`, `translations`
- **Translation subgraph state**: `text`, `from_lang`, `to_lang`, `result`
- Translate to multiple languages using dynamic Send + subgraph

Requirements:
- Subgraph has different state schema than parent
- Create wrapper function for state transformation
- Support translating to 3+ languages in parallel
- Combine all translations in parent state

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_2_17_4_solution.py`

**Exercise 3: Document Review System**

Build a hierarchical document review system:
- **Level 1**: DocumentReviewer (orchestrates everything)
- **Level 2**: TechnicalReview, EditorialReview subgraphs
- **Level 3**: Within TechnicalReview: FactChecker, CodeValidator

Requirements:
- At least 3 levels of nesting
- Technical and Editorial reviews run in parallel
- Each subgraph should have clear input/output
- Final output combines all review feedback

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_3_17_4_solution.py`

---

### Section 17.5

**Exercise 1: Configurable Report Generator**

Build a report generator where users configure which sections to include:
- Executive summary (optional)
- Data analysis (always included)
- Visualizations (optional)
- Recommendations (optional)
- Appendix (optional)

Requirements:
- Accept config: `{"sections": ["summary", "analysis", "recommendations"]}`
- Build graph with only requested sections
- Each section is a node that processes input data
- Handle empty config gracefully

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_1_17_5_solution.py`

**Exercise 2: Dynamic Approval Workflow**

Create an approval system that builds different chains based on request type:
- "vacation": Employee → Manager → END
- "expense" (< $100): Employee → Manager → END
- "expense" (>= $100): Employee → Manager → Finance → END
- "expense" (>= $1000): Employee → Manager → Finance → Director → END
- "hiring": HR → Manager → Director → VP → END

Requirements:
- Factory function takes request type and amount
- Build minimal approval chain needed
- Track who approved at each step
- Return final approval status

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_2_17_5_solution.py`

**Exercise 3: LLM-Designed Research Assistant**

Build a research assistant where the LLM designs its own workflow:
- User provides research question
- LLM decides what steps are needed (search, analyze, compare, synthesize, etc.)
- System builds and executes the planned graph
- LLM can include 2-5 steps based on complexity

Requirements:
- LLM outputs JSON plan with step names and descriptions
- Graph is built from LLM's plan
- Each step uses LLM with appropriate prompt
- Final step synthesizes all results

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_3_17_5_solution.py`

---

### Section 17.6

**Exercise 1: Essay Improver**

Build an essay improvement system that:
- Takes a rough draft as input
- Scores it on: thesis clarity, evidence quality, writing style, conclusion strength
- Iterates until all scores >= 7 OR max 4 iterations
- Shows score progression across iterations
- Produces final improved essay

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_1_17_6_solution.py`

**Exercise 2: Bug-Fixing Agent**

Create a code debugging agent that:
- Takes buggy code and expected behavior as input
- Attempts to run the code
- If it fails, analyzes the error and attempts a fix
- Tracks what fixes were attempted
- Stops when code runs correctly OR after 5 attempts
- Reports what bug was found and how it was fixed

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_2_17_6_solution.py`

**Exercise 3: Fact-Checked Article Generator**

Build an article generator with fact-checking:
- Generate article on given topic
- Extract 3-5 key claims from the article
- "Verify" each claim (simulate with LLM evaluation)
- If any claims are questionable, revise the article
- Track which claims were revised
- Continue until all claims pass OR max 3 iterations

> `part_4_langgraph/chapter_17_advanced_patterns/exercise_3_17_6_solution.py`
