# Chapter 16: Multi-Agent Systems

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
mkdir part_4_langgraph\chapter_16_multi_agent
cd part_4_langgraph\chapter_16_multi_agent
```

**On Mac/Linux:**

```
mkdir -p part_4_langgraph/chapter_16_multi_agent
cd part_4_langgraph/chapter_16_multi_agent
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

You should see (`venv`) at the beginning of your terminal prompt. Perfect! You're ready to go.

6. Install the required packages for Chapter 16:

> `part_4_langgraph/chapter_16_multi_agent/requirements.txt`

Or copy and create the file yourself:

```
# requirements.txt
langgraph==1.0.4
langchain-openai==1.1.1
python-dotenv==1.2.1
```

Then install with:

```bash
pip install -r requirements.txt
```

This will install:
- `langgraph` (1.0.4) - for building multi-agent workflows with StateGraph
- `langchain-openai` (1.1.1) - for ChatOpenAI LLM integration
- `python-dotenv` (1.2.1) - for loading environment variables from .env files

7. Create your `.env` file with your API keys:

> `part_4_langgraph/chapter_16_multi_agent/.env.example`

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

### Section 16.1

**Exercise 1: Multi-Agent Decision Analysis**

You're designing an AI system for each scenario below. For each one, decide: single agent or multiple agents? If multiple, identify the agents you'd create.

Scenarios:
1. A chatbot that answers FAQs about a company's products
2. An AI that reviews legal contracts, checks for compliance issues, and suggests revisions
3. A customer service system that handles complaints, processes refunds, and escalates complex issues
4. A translation tool that converts English documents to Spanish
5. An AI research assistant that finds papers, summarizes them, identifies gaps, and suggests experiments

Write a brief justification for each decision.

> `part_4_langgraph/chapter_16_multi_agent/exercise_1_2_16_1_solutions.md`

**Exercise 2: Agent Boundary Design**

You're building an AI-powered content creation pipeline for a marketing team. The workflow is:

1. Research trending topics in the industry
2. Generate content ideas based on research
3. Write first draft of article
4. Review for factual accuracy
5. Edit for brand voice and style
6. Generate social media snippets

Design the agent architecture. For each agent you propose:
- What is its name and single responsibility?
- What tools would it need?
- What context/instructions would it have?
- What does it receive as input? What does it output?

Draw a simple diagram showing how information flows between agents.

> `part_4_langgraph/chapter_16_multi_agent/exercise_1_2_16_1_solutions.md`

**Exercise 3: Specialist vs. Generalist Comparison**

Create a practical comparison by implementing two approaches to this task:

*"Given a piece of code, identify bugs, suggest optimizations, and add documentation."*

1. Build a single-agent version that does all three tasks
2. Build a multi-agent version with three specialists (Bug Finder, Optimizer, Documenter)
3. Run both on the same sample code
4. Compare the quality and depth of outputs

Sample code to analyze:
```python
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total = total + numbers[i]
    average = total / len(numbers)
    return average
```

Document your observations about the differences in output quality.

> `part_4_langgraph/chapter_16_multi_agent/exercise_3_16_1_solution.py`

---

### Section 16.2

**Exercise 1: Document Processing Pipeline**

Build a sequential pipeline for processing documents with these stages:
1. **Extractor** - Pulls out key entities (people, places, dates)
2. **Classifier** - Categorizes the document type (legal, medical, financial, other)
3. **Summarizer** - Creates a summary appropriate for that document type

Test with a sample document of your choice.

> `part_4_langgraph/chapter_16_multi_agent/exercise_1_16_2_solution.py`

**Exercise 2: Multi-Perspective Analysis**

Create a broadcast pattern for analyzing a business decision. Three agents should provide different perspectives:
1. **Optimist** - Focuses on potential benefits and opportunities
2. **Pessimist** - Focuses on risks and potential problems
3. **Pragmatist** - Focuses on practical implementation concerns

Add an aggregator that synthesizes a balanced recommendation.

> `part_4_langgraph/chapter_16_multi_agent/exercise_2_16_2_solution.py`

**Exercise 3: Smart Router with Fallback**

Build a hierarchical system that routes questions to specialists:
- **Math Agent** - Handles calculations and math problems
- **History Agent** - Handles historical questions
- **Science Agent** - Handles science questions
- **Fallback Agent** - Handles anything that doesn't fit

The supervisor should route based on question content. Test with at least 5 different questions across categories.

> `part_4_langgraph/chapter_16_multi_agent/exercise_3_16_2_solution.py`

---

### Section 16.3

**Exercise 1: Customer Service Supervisor**

Build a supervisor-worker system for customer service with these workers:
- **Greeter** - Welcomes customer and classifies their issue
- **Billing Agent** - Handles payment and subscription issues
- **Tech Support** - Handles technical problems
- **Complaint Handler** - Handles complaints and escalations

The supervisor should:
1. Route to the appropriate specialist
2. If the specialist can't fully resolve, route to a human handoff message
3. Track the number of routing decisions made

> `part_4_langgraph/chapter_16_multi_agent/exercise_1_16_3_solution.py`

**Exercise 2: Document Processing Pipeline**

Create an iterative supervisor for document processing:
- **Extractor** - Pulls out key information
- **Validator** - Checks extracted info for completeness
- **Enricher** - Adds additional context

The supervisor should:
1. Run extractor first
2. Check validator - if incomplete, run extractor again (max 2 retries)
3. Only proceed to enricher when validator passes
4. Compile final structured document

> `part_4_langgraph/chapter_16_multi_agent/exercise_2_16_3_solution.py`

**Exercise 3: Quality Control Supervisor**

Build a supervisor with quality control loops:
- **Writer** - Creates content
- **Critic** - Scores content 1-10 with feedback
- **Improver** - Revises based on feedback

The supervisor should:
1. Start with writer
2. Get critic score
3. If score < 7, send to improver, then back to critic
4. Loop until score >= 7 or max 3 improvement rounds
5. Return final content with score history

> `part_4_langgraph/chapter_16_multi_agent/exercise_3_16_3_solution.py`

---

### Section 16.4

**Exercise 1: Three-Way Debate**

Extend the debate pattern to include three agents:
- **Optimist** - Focuses on opportunities and benefits
- **Pessimist** - Focuses on risks and problems
- **Realist** - Tries to find middle ground

Each agent should respond to the others' arguments. The judge should identify where all three perspectives align.

> `part_4_langgraph/chapter_16_multi_agent/exercise_1_16_4_solution.py`

**Exercise 2: Review Committee**

Build a collaborative review system with three reviewers:
- **Technical Reviewer** - Checks accuracy and technical correctness
- **Style Reviewer** - Checks clarity and readability
- **Audience Reviewer** - Checks if it's appropriate for target audience

They should each provide feedback, then collaboratively create a consolidated review with prioritized recommendations.

> `part_4_langgraph/chapter_16_multi_agent/exercise_2_16_4_solution.py`

**Exercise 3: Negotiation Simulation**

Create two agents that negotiate a deal:
- **Buyer Agent** - Wants lowest price, best terms
- **Seller Agent** - Wants highest price, favorable terms

They should:
1. Each state their initial position
2. Exchange counter-offers (max 3 rounds)
3. Try to find a mutually acceptable deal
4. Report final outcome (deal reached or impasse)

Track concessions made by each side.

> `part_4_langgraph/chapter_16_multi_agent/exercise_3_16_4_solution.py`

---

### Section 16.5

**Exercise 1: Add a Fact-Checker**

Add a fact-checker agent between the researcher and analyst that:
- Reviews each finding for plausibility
- Flags any claims that seem questionable
- Adds confidence levels (high/medium/low) to findings

The analyst should then weight its analysis based on confidence levels.

> `part_4_langgraph/chapter_16_multi_agent/exercise_1_16_5_solution.py`

**Exercise 2: Parallel Research**

Modify the researcher to gather information from two different "perspectives":
- **Academic perspective** - Focus on research and studies
- **Practical perspective** - Focus on real-world applications

Run both in parallel, then have the analyst synthesize both viewpoints.

> `part_4_langgraph/chapter_16_multi_agent/exercise_2_16_5_solution.py`

**Exercise 3: Automatic Gap Detection**

Add a "gap detector" agent after the analyst that:
- Reviews the insights and identifies topics that need deeper research
- Automatically triggers additional research on weak areas
- Limits to one round of additional research

The gap detector should check if any of the original questions weren't fully answered and request targeted follow-up research.

> `part_4_langgraph/chapter_16_multi_agent/exercise_3_16_5_solution.py`

---

### Section 16.6

**Exercise 1: State Audit**

Review the research team from Section 16.5. For each field in `ResearchState`:
1. Which agent writes to it?
2. Which agents read from it?
3. Is it replaced or accumulated?

Create a simple diagram showing the data flow.

> `part_4_langgraph/chapter_16_multi_agent/exercise_1_16_6_solution.py`

**Exercise 2: Fix the Bug**

This state has a problem when used with parallel agents. Identify and fix it:

```python
class AnalysisState(TypedDict):
    data: str
    result: str  # Both analyzers write here!

def technical_analyzer(state) -> dict:
    return {"result": f"Technical: {analyze(state['data'])}"}

def business_analyzer(state) -> dict:
    return {"result": f"Business: {analyze(state['data'])}"}
```

> `part_4_langgraph/chapter_16_multi_agent/exercise_2_16_6_solution.py`

**Exercise 3: Design a State**

Design a state schema for a content moderation system with these agents:
- **Toxicity Checker** - Scores content for toxic language
- **Spam Detector** - Checks if content is spam
- **PII Scanner** - Finds personal information
- **Decision Maker** - Makes final allow/block decision

Consider: What fields does each agent need? How should scores be stored? What does the decision maker need to see?

> `part_4_langgraph/chapter_16_multi_agent/exercise_3_16_6_solution.py`

---

### Section 16.7

**Exercise 1: Add Monitoring**

Take the research team from Section 16.5 and add:
- Logging for each agent (start/complete/duration)
- A simple metrics report at the end
- Error counting per agent

> `part_4_langgraph/chapter_16_multi_agent/exercise_1_16_7_solution.py`

**Exercise 2: Implement Timeout**

Create a wrapper that:
- Gives each agent a maximum time to complete
- Returns a default response if timeout is exceeded
- Logs timeout events

> `part_4_langgraph/chapter_16_multi_agent/exercise_2_16_7_solution.py`

**Exercise 3: Build a Health Check**

Create a health check system that:
- Tests each agent with a simple input
- Reports which agents are working
- Flags agents with high error rates

> `part_4_langgraph/chapter_16_multi_agent/exercise_3_16_7_solution.py`
