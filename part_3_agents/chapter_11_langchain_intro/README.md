# Chapter 11: Introduction to LangChain

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
mkdir part_3_agents\chapter_11_langchain_intro
cd part_3_agents\chapter_11_langchain_intro
```

**On Mac/Linux:**
```bash
mkdir -p part_3_agents/chapter_11_langchain_intro
cd part_3_agents/chapter_11_langchain_intro
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

6. Install the required packages for Chapter 11:

► `part_3_agents/chapter_11_langchain_intro/requirements.txt`

Or copy and create the file yourself:
```txt
# requirements.txt
langchain==1.1.3
langchain-openai==1.1.1
langchain-google-genai==4.0.0
langchain-anthropic==1.2.0
langchain-community==0.4.1
langchain-core==1.1.3
python-dotenv==1.2.1
pydantic==2.12.5
tavily-python==0.5.0
wikipedia-api==0.7.1
ollama==0.4.4
```

Then install with:
```bash
pip install -r requirements.txt
```

This will install:
- `langchain` (1.1.3) - Core LangChain framework for building agents
- `langchain-openai` (1.1.1) - OpenAI integration for GPT models
- `langchain-google-genai` (4.0.0) - Google Gemini integration
- `langchain-anthropic` (1.2.0) - Anthropic Claude integration
- `langchain-community` (0.4.1) - Community tools and integrations
- `langchain-core` (1.1.3) - Core components like prompts and output parsers
- `python-dotenv` (1.2.1) - Environment variable management for API keys
- `pydantic` (2.12.5) - Data validation for structured outputs
- `tavily-python` (0.5.0) - Web search tool integration
- `wikipedia-api` (0.7.1) - Wikipedia tool for research assistant
- `ollama` (0.4.4) - Local model support

**Note:** LangChain Classic is installed automatically as a dependency when needed for memory components.

7. Create your `.env` file with your API keys:

► `part_4_langgraph/chapter_11_langchain_intro/.env.example`

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

### Section 11.1

**Exercise 1: Framework Exploration**
Visit the LangChain documentation (python.langchain.com). Find and list:
- Three different agent types available
- Five different tool integrations
- Three memory types
- Two vector store options
Write a brief note about which ones interest you most and why.

► `part_3_agents/chapter_11_langchain_intro/exercise_1_11_1_solution.md`

**Exercise 2: Use Case Planning**
Think about three real problems in your life or work that an AI agent could solve. For each one, write:
- What the problem is
- What tools the agent would need
- What type of memory would be helpful
- How LangChain could help build it

► `part_3_agents/chapter_11_langchain_intro/exercise_2_11_1_solution.md`

**Exercise 3: Code Comparison**
Look at your chatbot code from Chapter 8. List five specific things that were challenging or repetitive (like managing message history, handling errors, formatting prompts). For each one, research how LangChain handles it. Would it simplify your code?

► `part_3_agents/chapter_11_langchain_intro/exercise_3_11_1_solution.py`

---

### Section 11.2

**Exercise 1: Environment Detective**
Create a script that reports on your setup:
- Python version
- LangChain version
- Whether API key is present (not the key itself!)
- Current working directory
- List of installed packages

Save it as `debug/environment_report.py` - you'll use this whenever something goes wrong!

► `part_3_agents/chapter_11_langchain_intro/exercise_1_11_2_solution.py`

**Exercise 2: Setup Automation**
Create a simple bash script that:
- Creates a new project folder
- Sets up a virtual environment
- Installs the basic packages
- Creates template `.env` and `.gitignore` files

This will save you time on future projects!

► `part_3_agents/chapter_11_langchain_intro/exercise_2_11_2_solution.sh`

**Exercise 3: Connection Tester**
Write a script that:
- Tries to connect to OpenAI
- Handles errors gracefully
- Reports success or explains what went wrong
- Suggests fixes for common problems

This becomes your go-to diagnostic tool.

► `part_3_agents/chapter_11_langchain_intro/exercise_3_11_2_solution.py`

---

### Section 11.3

**Exercise 1: Prompt Variations**
Create three different prompt templates for the same task (summarizing text):
- One for technical audiences
- One for children
- One for business executives

Test all three with the same input text. Save as `basics/prompt_variations.py`.

► `part_3_agents/chapter_11_langchain_intro/exercise_1_11_3_solution.py`

**Exercise 2: Chain Builder**
Build a chain that:
1. Takes a topic as input
2. Generates three questions about that topic
3. Picks the most interesting question
4. Answers it

Use separate chains for each step. Save as `basics/question_chain.py`.

► `part_3_agents/chapter_11_langchain_intro/exercise_2_11_3_solution.py`

**Exercise 3: Model Comparison**
Create a script that:
- Sends the same prompt to two different temperature settings
- Compares the outputs
- Counts how many words differ

This will help you understand temperature's impact. Save as `basics/model_comparison.py`.

► `part_3_agents/chapter_11_langchain_intro/exercise_3_11_3_solution.py`

---

### Section 11.4

**Exercise 1: Specialized Assistant**
Create an assistant with three specialized modes:
- Translator mode (translates to different styles: formal, casual, technical)
- Summarizer mode (creates different length summaries)
- Analyzer mode (provides different types of analysis)

Each mode should have clear, distinct behavior. Save as `first_app/specialized_assistant.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_1_11_4_solution.py`

**Exercise 2: Learning Tracker**
Build an assistant that:
- Remembers topics you're learning
- Can quiz you on previous topics
- Tracks your progress
- Provides encouragement

Focus on using memory effectively. Save as `first_app/learning_tracker.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_2_11_4_solution.py`

**Exercise 3: Writing Workshop**
Create an assistant that helps with writing by:
- Offering different improvement styles (clarity, creativity, conciseness)
- Remembering your writing goals
- Providing consistent feedback
- Tracking common issues

Keep each function simple and focused. Save as `first_app/writing_workshop.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_3_11_4_solution.py`

---

### Section 11.5

**Exercise 1: Cost Tracker**
Build an assistant that:
- Tracks spending across all models
- Shows cost per conversation
- Switches to cheaper models when budget is low
- Provides daily spending reports

Save as `providers/cost_tracker.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_1_11_5_solution.py`

**Exercise 2: Speed Optimizer**
Create a system that:
- Measures response time for each model
- Automatically picks the fastest available model
- Falls back to slower models if fast ones fail
- Shows performance statistics

Save as `providers/speed_optimizer.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_2_11_5_solution.py`

**Exercise 3: Privacy Guardian**
Build an assistant that:
- Detects if a question contains private information
- Uses local models for private questions
- Uses cloud models for general questions
- Logs which model was used and why

Save as `providers/privacy_guardian.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_3_11_5_solution.py`

---

### Section 11.6

**Exercise 1: Email Analyzer**
Build a parser that extracts from emails:
- Sender details (name, email, company)
- Email category (support, sales, complaint)
- Sentiment (positive, negative, neutral)
- Action required (yes/no)
- Priority level (high, medium, low)

Save as `parsers/email_analyzer.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_1_11_6_solution.py`

**Exercise 2: Meeting Notes Parser**
Create a system that extracts from meeting notes:
- Attendees list
- Key decisions made
- Action items with owners
- Follow-up dates
- Main topics discussed

Save as `parsers/meeting_parser.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_2_11_6_solution.py`

**Exercise 3: Product Review Extractor**
Build a parser that extracts from reviews:
- Overall rating (1-5)
- Pros list
- Cons list
- Would recommend (yes/no)
- Key product features mentioned

Save as `parsers/review_parser.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_3_11_6_solution.py`

---

### Section 11.7

**Exercise 1: Debug Dashboard**
Create a dashboard that:
- Shows chain component status
- Displays performance metrics
- Tracks error rates
- Provides quick fixes
- Generates health reports

Save as `debug/debug_dashboard.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_1_11_7_solution.py`

**Exercise 2: Performance Monitor**
Build a system that:
- Tracks execution time for each chain component
- Identifies slow parts
- Suggests optimizations
- Creates performance graphs
- Alerts on slowdowns

Save as `debug/performance_monitor.py`

► `part_3_agents/chapter_11_langchain_intro/exercise_2_11_7_solution.py`

**Exercise 3: Error Recovery System**
Create a wrapper that:
- Catches common errors
- Attempts automatic fixes
- Retries with exponential backoff
- Logs all attempts
- Falls back to simpler methods

Save as `debug/error_recovery.py`

> **New Type Hint: `Callable`**
> The solution uses `Callable` from the `typing` module. This type hint indicates a function or callable object. For example, `-> Callable` means "returns a function." This is useful when methods return other functions as recovery strategies.

► `part_3_agents/chapter_11_langchain_intro/exercise_3_11_7_solution.py`

---

## Challenge Project: Build Your Smart Study Assistant

Time to put everything together! Create an intelligent study assistant using chains, prompts, and structured outputs.

> `part_3_agents/chapter_11_langchain_intro/challenge_project_starter.py`

### Requirements:

**1. Multi-Provider Support**
- Use GPT-3.5 for simple explanations
- Use GPT-4 for complex topics
- Use local models for private notes
- Automatically select based on complexity

**2. Smart Chain Modes**
- Teacher Mode: Patient explanations with examples
- Quiz Mode: Test your knowledge with questions
- Summary Mode: Create concise study notes
- Discussion Mode: Socratic dialogue for deeper understanding

**3. Memory Management**
- Remember topics you're studying
- Track what you've already learned
- Maintain conversation context
- Save and load study sessions

**4. Structured Output**
- Parse explanations into key points
- Extract important terms and definitions
- Create formatted study guides
- Generate quiz questions with answers

**5. Production Quality**
- Comprehensive error handling
- Fallback to simpler models if primary fails
- Performance monitoring with response times
- Debug mode for troubleshooting
- Clean, interactive command-line interface

### Core Features to Implement:
- Topic classifier that routes to appropriate chains
- Different prompt templates for each mode
- Conversation memory that persists between sessions
- Output parsers for structured study materials
- Cost tracking across different models
- Automatic model selection based on query complexity

### Bonus Challenges:
- Add a "learning path" that sequences topics
- Create flashcards from conversations
- Generate practice problems
- Track learning progress over time
- Export study materials to markdown

### Success Criteria:
- Handles at least 4 different study modes
- Switches seamlessly between providers
- Maintains context across 20+ message conversations
- Produces structured, parseable output
- Never crashes on errors (graceful fallbacks)
- Actually helps you learn something!
