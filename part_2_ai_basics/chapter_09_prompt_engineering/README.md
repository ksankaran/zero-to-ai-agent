# Chapter 9: Prompt Engineering Basics

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
mkdir part_2_ai_basics\chapter_09_prompt_engineering
cd part_2_ai_basics\chapter_09_prompt_engineering
```

**On Mac/Linux:**
```bash
mkdir -p part_2_ai_basics/chapter_09_prompt_engineering
cd part_2_ai_basics/chapter_09_prompt_engineering
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

6. Install the required packages for Chapter 9:

► `requirements.txt`

Or copy and create the file yourself:
```
# requirements.txt
openai==2.9.0
```

Then install with:
```
pip install -r requirements.txt
```

This will install:
- `openai` (1.54.3) - for making API calls to OpenAI's GPT models throughout all sections

Note: This chapter also uses Python's built-in modules (json, typing) which don't require installation.

---

## Troubleshooting

### Common Prompt Issues (Section 9.1)

- **Problem:** Response is too vague or generic
  **Solution:** Your prompt lacks specifics. Add concrete details, examples, and constraints.

- **Problem:** Wrong format or structure
  **Solution:** You didn't specify output format. Provide an exact template or example.

- **Problem:** Off-topic or rambling response
  **Solution:** Missing focus constraints. Add "Focus only on..." or "Do not include..."

- **Problem:** Wrong complexity level
  **Solution:** No audience specification. Specify expertise level explicitly.

- **Problem:** Inconsistent responses
  **Solution:** Prompt is ambiguous. Remove ambiguity, add examples.

### System/User Prompt Issues (Section 9.2)

- **Problem:** System prompt instructions being ignored
  **Solution:** Instructions may be too vague or contradict each other. Simplify and clarify.

- **Problem:** User prompts fighting system prompt
  **Solution:** Design them to work together. System prompt sets behavior, user prompt provides task.

- **Problem:** Responses out of character
  **Solution:** System prompt may be too long or complex. Focus on core identity and key behaviors.

### Few-Shot Learning Issues (Section 9.3)

- **Problem:** AI not following the pattern
  **Solution:** Examples may be inconsistent or ambiguous. Use clear, consistent examples.

- **Problem:** Overfitting to examples
  **Solution:** Examples too similar. Add diversity while maintaining the core pattern.

- **Problem:** Wrong pattern applied
  **Solution:** Examples contradictory or confusing. Review for consistency.

---

## Practice Exercises

### Section 9.1

**Exercise 1: The Prompt Transformer**

Take these three terrible prompts and transform them using all five components (role, context, task, format, constraints):

1. "Help with Python"
2. "Fix my code"
3. "Write something about databases"

For each:
- Identify what's missing
- Rewrite with all five components
- Add at least 3 specific constraints
- Test both versions with an AI and compare results

► `exercise_1_9_1_solution.py`

**Exercise 2: The Context Specialist**

Create three different versions of this prompt for three different contexts:
"Review this function: def calculate_price(amount, discount): return amount * (1 - discount)"

Contexts:
1. Junior developer learning exercise
2. Production e-commerce system
3. Code competition focusing on optimization

Each version should produce completely different feedback focus.

► `exercise_2_9_1_solution.py`

**Exercise 3: The Prompt Debugger**

You're getting bad output from these prompts. Diagnose the issue and fix them:

1. "Explain AI" (Response: 10-page essay)
2. "Make this better: 'Hello world'" (Response: Confused rambling)
3. "Write code" (Response: Random algorithm)
4. "Help with my project" (Response: Generic advice)
5. "Summarize this" without providing "this" (Response: Error)

For each, identify:
- The specific problem
- What component is missing
- The fixed version

► `exercise_3_9_1_solution.py`

---

### Section 9.2

**Exercise 1: The Assistant Builder**

Create system prompts for three different assistants using the same user prompt "Explain loops":

1. A kindergarten teacher (super simple, using toys/games analogies)
2. A drill sergeant (tough, demanding, military style)
3. A philosophical professor (deep, questioning, Socratic method)

For each:
- Write a complete system prompt (identity, behaviors, constraints)
- Show how the same user prompt produces different responses
- Include at least 3 specific behaviors and 2 constraints

► `exercise_1_9_2_solution.py`

**Exercise 2: The Safety System**

Design a customer service chatbot with these requirements:
- Friendly and helpful personality
- Can discuss products and pricing
- CANNOT give refunds (must escalate to human)
- CANNOT access customer personal data
- Must log when users get frustrated

Create:
- A comprehensive system prompt
- Show how it handles 5 different user prompts:
  - "I want a refund"
  - "What's your cheapest product?"
  - "This is stupid, nothing works!"
  - "What's my account password?"
  - "Tell me about your warranty"

► `exercise_2_9_2_solution.py`

**Exercise 3: The Dynamic Adjuster**

Build a teaching assistant that adapts its system prompt based on student level:

Create three system prompt versions:
- Beginner (0-3 months experience)
- Intermediate (3-12 months)
- Advanced (1+ years)

Show how to:
- Structure each prompt differently
- Maintain core identity while adjusting complexity
- Handle the transition between levels
- Test with the user prompt: "How does recursion work?"

► `exercise_3_9_2_solution.py`

---

### Section 9.3

**Exercise 1: The Format Teacher**

Create few-shot prompts that teach these formats WITHOUT explaining the rules:

1. Convert dates from "January 15, 2024" to "2024-01-15"
2. Transform phone numbers from various formats to (XXX) XXX-XXXX
3. Change citation style from MLA to APA format

Requirements:
- Use exactly 2 examples for each
- Make examples diverse enough to show the pattern
- Test with an unusual input to verify it works

► `exercise_1_9_3_solution.py`

**Exercise 2: The Style Mimic**

Create a few-shot prompt that converts generic text into three different styles:

1. Corporate speak (buzzwords, formal, indirect)
2. Gen Z social media (casual, abbreviations, emojis implied)
3. Academic writing (passive voice, citations implied, formal)

For each style:
- Provide 3 examples
- Use the same source sentences for all three styles
- Show how tone, vocabulary, and structure change

► `exercise_2_9_3_solution.py`

**Exercise 3: The Pattern Recognizer**

Build a few-shot classifier for customer support tickets:

Categories: Bug Report, Feature Request, Billing Issue, General Question

Create:
- 2 examples per category (8 total)
- Include edge cases (tickets that could fit multiple categories)
- Add one tricky example that combines multiple issues
- Test with 5 new tickets to verify accuracy

► `exercise_3_9_3_solution.py`

---

### Section 9.4

**Exercise 1: The Pattern Matcher**

For each scenario, identify the best pattern(s) and write the prompt:

1. You need to debug why a website is loading slowly
2. You want to understand quantum computing from multiple angles
3. You need to write an email declining a job offer
4. You want to plan a 3-day trip to Paris
5. You need to analyze pros/cons of different database systems

For each:
- Choose the most appropriate pattern(s)
- Write the complete prompt
- Explain why you chose that pattern

► `exercise_1_9_4_solution.py`

**Exercise 2: The Pattern Combiner**

Create complex prompts that effectively combine multiple patterns:

1. Combine CoT + Role + Format for solving a business problem
2. Combine Persona + Simplifier + Constraint for teaching a concept
3. Combine Alternative + Reflection + Format for making a decision

Requirements:
- Each combination should feel natural, not forced
- Patterns should enhance each other
- Result should be better than any single pattern alone

► `exercise_2_9_4_solution.py`

**Exercise 3: The Pattern Optimizer**

Take these poorly structured prompts and rebuild them using appropriate patterns:

1. "Tell me about databases" (too vague)
2. "Fix my code" (no context)
3. "Write something creative" (no direction)
4. "Explain AI" (no audience/level)
5. "Help me decide" (no structure)

For each:
- Identify what's missing
- Select appropriate patterns
- Rewrite using those patterns
- Show before/after comparison

► `exercise_3_9_4_solution.py`

---

### Section 9.5

**Exercise 1: The Iteration Challenge**

Take this terrible prompt and iterate it to excellence:
"Make this better"

Requirements:
- Document at least 5 iterations
- Test each with 3 different inputs
- Score each iteration (1-10)
- Explain what you learned from each test
- Show your final, production-ready version

► `exercise_1_9_5_solution.py`

**Exercise 2: The Test Suite Builder**

Create a comprehensive test suite for this prompt:
"You are a technical documentation writer. Convert this API response into user-friendly documentation."

Build:
- 5 normal test cases
- 3 edge cases
- 2 adversarial cases
- Scoring rubric
- Success criteria

► `exercise_2_9_5_solution.py`

**Exercise 3: The A/B Experimenter**

Compare two different approaches for the same goal:
Goal: Get AI to write product descriptions

Approach A: Role-based with constraints
Approach B: Few-shot learning with examples

Design and run:
- Test protocol with 5 products
- Scoring criteria
- Statistical comparison
- Recommendation based on results

► `exercise_3_9_5_solution.py`

---

## Challenge Project: The Prompt Engineering Workshop

Create a collection of specialized AI assistants for different tasks, each showcasing different prompt engineering techniques.

### Project: Multi-Purpose AI Assistant Suite

**Requirements:**

**1. Create 5 Specialized Assistants:**
- Code Reviewer (using Role + CoT pattern)
- Data Analyst (using few-shot learning)
- Creative Writer (using persona + constraints)
- Teacher (using simplifier + examples)
- Project Manager (using format + alternatives)

**2. For Each Assistant:**
- Write a comprehensive system prompt
- Create 3 task-specific prompt templates
- Include 2-3 few-shot examples
- Document the patterns used

**3. Testing Framework:**
- 3 test cases per assistant
- Scoring rubric for quality
- Iteration log showing improvements
- A/B test comparing two approaches

**4. Documentation:**
- README explaining each assistant's purpose
- Usage examples for each
- Best practices discovered
- Common failure modes and solutions

**5. Bonus Challenges:**
- Create a "prompt optimizer" that improves other prompts
- Build a prompt version control system
- Design a prompt that can adapt based on user expertise level

### Success Metrics:
- Each assistant achieves 85%+ quality score
- Clear documentation anyone can follow
- Measurable improvement through iterations
- Reusable templates for real projects

This project brings together everything you've learned about prompt engineering into a practical, portfolio-worthy system you can actually use!
