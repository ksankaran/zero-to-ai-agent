# Chapter 7: Introduction to AI and Large Language Models

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
mkdir part_2_ai_basics\chapter_07_intro_ai_llm
cd part_2_ai_basics\chapter_07_intro_ai_llm
```

**On Mac/Linux:**
```bash
mkdir -p part_2_ai_basics/chapter_07_intro_ai_llm
cd part_2_ai_basics/chapter_07_intro_ai_llm
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

6. Install the required packages for Chapter 8:

► `requirements.txt`

Or copy and create the file yourself:
```
# requirements.txt
openai==2.9.0
python-dotenv==1.2.1
anthropic==0.75.0
requests==2.32.5
google-generativeai==0.8.5
pandas==2.3.3
```

Then install with:
```
pip install -r requirements.txt
```

This will install:
- `openai` (2.9.3) - for making API calls to OpenAI's GPT models
- `python-dotenv` (1.2.1) - for managing API keys in .env files
- `anthropic` (0.75.0) - optional, for trying Claude as an alternative (section 8.1)
- `requests` (2.32.5) - HTTP requests for API calls
- `google-generativeai` (0.8.5) - For Google Gemini models
- `pandas` (2.2.3) - data manipulation and analysis for structured data

---

## Troubleshooting

### Common AI Misconceptions (Section 7.1)

- **Misconception:** "AI is sentient/conscious"
  **Reality:** AI has no consciousness, feelings, or self-awareness. Think: Sophisticated calculator, not electronic person.

- **Misconception:** "AI will replace all jobs tomorrow"
  **Reality:** AI augments human work, handles specific tasks. Think: Power tools for the mind, not replacement workers.

- **Misconception:** "AI always gives correct answers"
  **Reality:** AI makes mistakes, especially with unusual inputs. Think: Very smart assistant that still needs supervision.

- **Misconception:** "AI understands what it's saying"
  **Reality:** AI recognizes patterns but doesn't truly comprehend. Think: Google Translate - converts languages without understanding meaning.

- **Misconception:** "Building AI requires a PhD"
  **Reality:** You're doing it in this book with basic Python! Think: Using AI is like using any other API or library now.

### Common LLM Misconceptions (Section 7.2)

- **"LLMs understand what they're saying"**
  Reality: They predict patterns without true comprehension. Think: Sophisticated autocomplete, not consciousness.

- **"Bigger models are always better"**
  Reality: Depends on your task. Smaller, specialized models often faster and cheaper.

- **"LLMs can replace programmers"**
  Reality: They're powerful tools for programmers. You still need to understand, verify, and integrate code.

- **"LLMs always tell the truth"**
  Reality: They generate plausible text, not facts. Always verify important information.

- **"The same prompt gives the same result"**
  Reality: Only at temperature 0, and even then slight variations. Build systems that handle variation.

---

## Practice Exercises

### Section 7.1

**Exercise 1: AI or Not AI?**
Consider each system below. Is it using AI or traditional programming? Think about whether the system follows fixed rules or learns from patterns.

**Systems to evaluate:**
1. A calculator app that adds numbers
2. Google Photos finding all pictures of your dog
3. A website login that checks if password matches
4. Spotify creating your 'Discover Weekly' playlist
5. An alarm clock that rings at 7 AM
6. Your phone's face unlock
7. A thermostat that turns on at 70°F
8. Gmail's spam filter
9. A video game where enemies always patrol the same path
10. YouTube's recommendation algorithm

► `exercise_1_7_1_solution.py`

**Exercise 2: Categorizing AI Types**
Match each AI application to its learning type. Remember:
- **Supervised Learning**: Learns from labeled examples (like a teacher showing correct answers)
- **Unsupervised Learning**: Finds patterns without being told what to look for
- **Reinforcement Learning**: Learns through trial and error with rewards/penalties

**Applications to categorize:**

A. An email filter trained on examples of spam and not-spam emails
B. A system that groups customers by shopping behavior without predefined categories
C. A robot learning to walk by trying different movements and getting points for distance traveled
D. A model that predicts house prices from past sales data with known prices
E. An AI finding hidden patterns in genetic data without knowing what diseases to look for
F. A game-playing AI that improves by winning/losing thousands of games
G. A photo app that learned to identify faces after seeing millions of labeled face images

► `exercise_2_7_1_solution.py`

**Exercise 3: Design Your Own AI Application**
Think of a problem in your daily life that AI could solve. This is a thought exercise - no coding required!

Fill in these details for your AI idea:

📌 **Problem it solves:**
(What daily annoyance or challenge does it address?)

**Type of AI:**
(Supervised / Unsupervised / Reinforcement - and why?)

**Data it would need:**
(What information would it need to learn from?)

**Inputs:**
(What information does the user provide?)

**Outputs:**
(What does the AI produce or recommend?)

- **Why AI instead of traditional programming?**
(What makes this problem suitable for learning rather than rules?)

► `exercise_3_7_1_solution.py`

---

### Section 7.2

**Exercise 1: Token Estimation**
Estimate how many tokens each text would use (remember: ~4 characters or ¾ word per token):

1. "Hello, world!"
2. "The quick brown fox jumps over the lazy dog."
3. A typical email (200 words)
4. This entire section you're reading
5. "def calculate\_sum(a, b): return a + b"

*Estimates below - try it yourself first!*

► `exercise_1_7_2_solution.py`

**Exercise 2: Choosing the Right Parameters**
For each scenario, what temperature would you choose and why?

A. Writing legal contract language
B. Generating creative story ideas
C. Translating technical documentation
D. Writing varied product descriptions
E. Solving coding problems
F. Brainstorming business names

*Think about the tradeoff between consistency and creativity.*

► `exercise_2_7_2_solution.py`

**Exercise 3: Identifying Good vs Bad LLM Tasks**
Categorize each task as "Great for LLMs," "Okay with Caveats," or "Bad Idea":

1. Writing a first draft of a blog post
2. Calculating compound interest over 30 years
3. Checking if an email sounds professional
4. Getting today's stock prices
5. Explaining a complex concept simply
6. Generating test data for your application
7. Making medical diagnoses
8. Summarizing a long document
9. Checking if a password is secure
10. Writing poetry in Shakespeare's style

*Consider: Does it need real-time data? Precise calculations? Creative language?*

► `exercise_3_7_2_solution.py`

---

### Section 7.3

**Exercise 1: Trace the Flow**
Walk through what happens with this prompt: "The weather today is"

Consider:
1. How does it become tokens?
2. What patterns might activate?
3. What completions are likely?
4. What information is missing?

*Think through each step before checking the solution.*

► `exercise_1_7_3_solution.py`

**Exercise 2: Context Window Planning**
You have a 4,000 token context window. Design an approach for:

A. Having a 10,000 token conversation
B. Analyzing a 50,000 token document
C. Maintaining chat history over multiple sessions

*Consider: What to keep, what to summarize, what to drop?*

► `exercise_2_7_3_solution.py`

**Exercise 3: Understanding Failures**
For each scenario, explain why the LLM fails using what you learned:

1. Can't do exact arithmetic on large numbers
2. Makes up fake citations
3. Contradicts itself in long conversations
4. Can't learn your preferences permanently
5. Sometimes says factually wrong things confidently

*Hint: Think about the mechanism - pattern matching, no memory, statistical training.*

► `exercise_3_7_3_solution.py`

---

### Section 7.4

**Exercise 1: Prompt Improvement Challenge**
Take these weak prompts and improve them using the techniques you've learned:

1. "Write about space"
2. "Fix this: def func(x): return x/0"
3. "Translate: Hello"
4. "Make a list"
5. "Explain AI"

► `exercise_1_7_4_solution.py`

**Exercise 2: Few-Shot Template Creation**
Create a few-shot prompt template for:
- Extracting dates from text
- Classifying customer support tickets
- Converting informal text to formal business language

► `exercise_2_7_4_solution.py`

**Exercise 3: Role-Based Prompting**
Write system prompts for these AI assistants:
- A Socratic tutor who guides through questions
- A code reviewer focusing on security
- A creative writing partner for brainstorming

► `exercise_3_7_4_solution.py`

**Exercise 4: Completion Control Experiment**
Using the same base prompt, experiment with:
- Different temperatures (0, 0.5, 1.0, 1.5)
- Different max\_tokens (50, 200, 500)
- Different stop sequences

Document how each parameter changes the output.

► `exercise_4_7_4_solution.py`

---

### Section 7.5

**Exercise 1: Cost Calculator**
Create a function that calculates monthly costs for different providers based on usage patterns. Consider a chatbot that handles varying message volumes.

► `exercise_1_7_5_solution.py`

**Exercise 2: Provider Comparison Matrix**
Build a comparison matrix for your specific use case. Include factors like cost, performance, features, and limitations.

► `exercise_2_7_5_solution.py`

**Exercise 3: Migration Planning**
Design a migration plan from OpenAI to an open-source model. What challenges would you face? How would you handle them?

► `exercise_3_7_5_solution.py`

**Exercise 4: API Abstraction**
Write a simple wrapper class that can work with both OpenAI and Anthropic APIs, allowing easy switching between providers.

► `exercise_4_7_5_solution.py`

---

### Section 7.6

**Exercise 1: Secure Key Storage**
Create a complete key management system that:
- Loads keys from multiple sources (.env, environment, config file)
- Validates key format
- Provides fallback options
- Never exposes keys in logs or errors

► `exercise_1_7_6_solution.py`

**Exercise 2: Multi-Provider Authentication**
Build a class that can authenticate with multiple providers and automatically failover if one is unavailable.

► `exercise_2_7_6_solution.py`

**Exercise 3: Rate Limit Handler**
Implement a robust rate limit handler that:
- Tracks requests per minute
- Automatically throttles when approaching limits
- Provides helpful feedback about wait times
- Works with any API provider

► `exercise_3_7_6_solution.py`

**Exercise 4: API Key Audit Tool**
Create a tool that:
- Scans a project for exposed API keys
- Checks Git history for accidentally committed keys
- Validates that all keys in use are properly secured
- Generates a security report

► `exercise_4_7_6_solution.py`
