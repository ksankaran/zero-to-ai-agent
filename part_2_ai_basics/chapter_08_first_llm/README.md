# Chapter 8: Your First LLM Integration

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
mkdir part_2_ai_basics\chapter_08_first_llm
cd part_2_ai_basics\chapter_08_first_llm
```

**On Mac/Linux:**
```bash
mkdir -p part_2_ai_basics/chapter_08_first_llm
cd part_2_ai_basics/chapter_08_first_llm
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
```txt
# requirements.txt
openai==2.9.0
python-dotenv==1.2.1
anthropic==0.75.0
```

Then install with:
```bash
pip install -r requirements.txt
```

This will install:
- `openai` (2.9.3) - for making API calls to OpenAI's GPT models
- `python-dotenv` (1.2.1) - for managing API keys in .env files
- `anthropic` (0.75.0) - optional, for trying Claude as an alternative (section 8.1)

7. Create your `.env` file with your API keys:

► `.env.example`

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

### API Setup Issues (Section 8.1)

- **Problem:** "Invalid API key"
  **Solution:** Double-check your key in .env - make sure there are no extra spaces

- **Problem:** "Rate limit exceeded"
  **Solution:** Wait a minute and try again, or upgrade your OpenAI plan

- **Problem:** ImportError: No module named 'openai'
  **Solution:** Run `pip install openai` again

### API Call Errors (Section 8.4)

- **Problem:** AuthenticationError
  **Solution:** Check your API key is correct and not expired

- **Problem:** RateLimitError
  **Solution:** Too many requests - implement retry with exponential backoff

- **Problem:** BadRequestError
  **Solution:** Invalid parameters - check your message format and model name

- **Problem:** APIConnectionError
  **Solution:** Network issue - check your internet connection and retry

### Response Issues (Section 8.3)

- **Problem:** Response cut off mid-sentence
  **Solution:** Check the finish_reason - if "length", increase max_tokens parameter

- **Problem:** Unexpected token counts
  **Solution:** Remember: 1 token ≈ 4 characters. Code and special characters use more tokens.

- **Problem:** Inconsistent responses
  **Solution:** Lower the temperature for more consistent output (try 0.2-0.5)

---

## Practice Exercises

### Section 8.1

**Exercise 1: Personality Bot**
Create a chatbot that:
- Has a specific personality (like a pirate, poet, or chef)
- Maintains that personality throughout the conversation
- Remembers previous messages
- Can switch personalities on command

► `exercise_1_8_1_solution.py`

**Exercise 2: Conversation Saver**
Build a chat program that:
- Saves each conversation to a text file
- Names the file with the current date and time
- Can load and continue a previous conversation
- Shows how many messages have been exchanged

► `exercise_2_8_1_solution.py`

**Exercise 3: Simple API Cost Calculator**
Create a tool that:
- Counts how many tokens you use in each message
- Estimates the cost of each API call
- Keeps a running total of your spending
- Warns you when you've spent more than $1

► `exercise_3_8_1_solution.py`

---

### Section 8.2

**Exercise 1: Temperature Tester**
Create a simple tool that:
- Takes one prompt from the user
- Generates 3 responses at different temperatures (0, 0.7, 1.5)
- Shows all three responses
- Lets the user pick their favorite

► `exercise_1_8_2_solution.py`

**Exercise 2: Conversation Counter**
Build a chatbot that:
- Counts how many messages have been sent
- Shows the word count of each response
- Estimates the cost (roughly $0.002 per 1000 tokens)
- Saves the conversation when you quit

► `exercise_2_8_2_solution.py`

**Exercise 3: Personality Switcher**
Create a chatbot that:
- Has 3 different personalities (your choice!)
- Lets you switch between them with a command
- Each personality has a different temperature setting
- Shows which personality is currently active

► `exercise_3_8_2_solution.py`

**BONUS CHALLENGE: Complete the Mini ChatGPT!**
Take the MiniChatGPT class boilerplate from the chapter and implement all the methods to create a full ChatGPT clone with:
- Multiple conversation threads (like ChatGPT's sidebar!)
- Ability to switch between conversations
- List all your conversations
- Save everything to a file
- Each conversation remembers its own history

---

### Section 8.3

**Exercise 1: Token Predictor**
Create a tool that:
- Takes a prompt from the user
- Predicts how many tokens it will use
- Makes the API call
- Compares prediction vs actual
- Keeps score of your accuracy

► `exercise_1_8_3_solution.py`

**Exercise 2: Response Time Tracker**
Build a simple tool that:
- Measures how long API calls take
- Tests different prompt lengths
- Shows if longer prompts take more time
- Finds the sweet spot for speed vs detail

► `exercise_2_8_3_solution.py`

**Exercise 3: Model Comparison**
Create a comparison tool that:
- Sends the same prompt to different models (if available)
- Compares token usage
- Compares costs
- Shows the differences in responses

► `exercise_3_8_3_solution.py`

---

### Section 8.4

**Exercise 1: Error Logger**
Create a tool that:
- Logs all API errors to a file
- Tracks error frequency
- Identifies patterns (like rate limits at certain times)
- Generates an error report

► `exercise_1_8_4_solution.py`

**Exercise 2: Resilient Caller**
Build a function that:
- Tries different models if one fails
- Falls back to simpler requests on errors
- Maintains a "health score" for the API
- Automatically adjusts behavior based on errors

► `exercise_2_8_4_solution.py`

**Exercise 3: Circuit Breaker**
Implement a circuit breaker pattern that:
- Stops making requests after repeated failures
- Waits before trying again
- Gradually increases request rate when healthy
- Provides status updates to the user

► `exercise_3_8_4_solution.py`

---

### Section 8.5

**Exercise 1: Topic Tracker**
Create a module that:
- Tracks what topics have been discussed
- Counts how often each topic appears
- Can report on conversation themes

► `exercise_1_8_5_solution.py`

**Exercise 2: Response Timer**
Create a module that:
- Times how long API calls take
- Tracks average response time
- Warns if responses are slow

► `exercise_2_8_5_solution.py`

**Exercise 3: Mood Detector**
Create a module that:
- Analyzes user message sentiment
- Adjusts bot personality based on mood
- Tracks mood over the conversation

► `exercise_3_8_5_solution.py`

---

### Section 8.6

**Exercise 1: Export Master**
Create a tool that can export conversations to:
- HTML format with nice formatting
- CSV for spreadsheet analysis
- Markdown for documentation
- PDF for sharing (bonus challenge!)

► `exercise_1_8_6_solution.py`

**Exercise 2: Smart Organizer**
Build a system that:
- Automatically organizes conversations by topic
- Groups related conversations together
- Creates daily/weekly summaries
- Suggests titles based on content

► `exercise_2_8_6_solution.py`

**Exercise 3: History Analytics**
Create an analyzer that shows:
- Your most common topics
- Average conversation length
- Most active times of day
- Conversation trends over time

► `exercise_3_8_6_solution.py`

---

## Challenge Project: Build "ARIA" - Your Adaptive Research & Information Assistant

Build a complete AI assistant that combines EVERYTHING you've learned:

### Core Requirements:

**1. Multi-Mode Operation**
- Research Mode: Helps with learning and research
- Creative Mode: Assists with writing and brainstorming
- Code Mode: Helps with programming tasks
- Analysis Mode: Analyzes data and provides insights

**2. Smart Conversation Management**
- Automatic session creation with meaningful titles
- Conversation search across all sessions
- Auto-save every 5 messages
- Daily summaries of conversations

**3. Robust Error Handling**
- Gracefully handle all API errors
- Implement exponential backoff for retries
- Rate limit awareness
- User-friendly error messages

**4. Cost Consciousness**
- Track tokens per conversation
- Show cost estimates in real-time
- Daily/weekly cost summaries
- Warning when approaching budget limits

**5. Export Capabilities**
- Export conversations to HTML, Markdown, and JSON
- Generate conversation summaries
- Create weekly activity reports

### Bonus Challenges:

**Level 1**: Add conversation templates (interview prep, brainstorming session, code review)

**Level 2**: Implement conversation merging (combine related conversations into one)

**Level 3**: Add a "memory" system where ARIA remembers key facts across conversations

### Starter Structure:

```python
# aria.py - Your Adaptive Research & Information Assistant

class ARIA:
    """Your personal AI assistant that never forgets"""

    def __init__(self):
        # Initialize all components you've learned
        pass

    def run(self):
        """Main assistant loop"""
        print(" ARIA - Adaptive Research & Information Assistant")
        print("=" * 60)
        print("I'm your AI assistant with perfect memory!")
        # Your implementation here
```

### Success Criteria:

Your ARIA should:
- Never crash (handles all errors gracefully)
- Remember everything (saves all conversations)
- Be helpful in multiple contexts (different modes)
- Be cost-effective (tracks and reports costs)
- Be searchable (find any past conversation)
