# Chapter 13: Agent Memory Systems

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
mkdir part_3_agents\chapter_13_agent_memory
cd part_3_agents\chapter_13_agent_memory
```

**On Mac/Linux:**
```bash
mkdir -p part_3_agents/chapter_13_agent_memory
cd part_3_agents/chapter_13_agent_memory
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

6. Install the required packages for Chapter 13:

► `part_3_agents/chapter_13_agent_memory/requirements.txt`

Or copy and create the file yourself:
```
# requirements.txt
python-dotenv==1.2.1
openai==2.9.0
chromadb==1.3.5
numpy==2.3.5
langchain==1.1.3
langchain-openai==1.1.1
langchain-community==0.4.1
langchain-classic==1.0.0
```

Then install with:
```bash
pip install -r requirements.txt
```

This will install:
- `python-dotenv` (1.2.1) - for loading environment variables from .env file
- `openai` (2.9.0) - for LLM API calls and embeddings
- `chromadb` (1.3.5) - vector database for semantic memory
- `numpy` (2.3.5) - numerical operations for embedding similarity
- `langchain` (1.1.3) - core LangChain framework
- `langchain-openai` (1.1.1) - OpenAI integration for LangChain
- `langchain-community` (0.4.1) - community integrations (SQLChatMessageHistory)
- `langchain-classic` (1.0.0) - classic agent patterns (create_react_agent, AgentExecutor)

7. Create your `.env` file with your API keys:

► `part_3_agents/chapter_13_agent_memory/.env.example`

Or copy and create the file yourself:

```
# .env
OPENAI_API_KEY=your-openai-api-key-here
LANGSMITH_API_KEY=your-langsmith-api-key-here
```

**Note:** Get your OpenAI API key from https://platform.openai.com/api-keys. The LangSmith API key is optional but recommended for debugging LangChain applications - get it from https://smith.langchain.com/.

---

## Practice Exercises

### Section 13.1

> **Note**: This section covers conceptual foundations. The exercises below are design and analysis exercises rather than coding exercises. You'll start writing code in Section 13.2.

**Exercise 1: Memory Classification**

For each scenario below, identify whether the information would best be stored in short-term memory, long-term memory, or both. Explain your reasoning.

1. The user says: "Let's talk about my upcoming trip to Paris."
2. The user mentions: "I'm allergic to peanuts."
3. The user asks: "What did I just say about the hotel?"
4. The agent calculates an intermediate result while solving a math problem.
5. The user says: "Remember, I prefer bullet points over long paragraphs."
6. The user shares: "Today's weather is really nice."

► `part_3_agents/chapter_13_agent_memory/exercise_1_13_1_solution.md`

**Exercise 2: Design a Memory Schema**

You're building a personal finance assistant agent. Design a memory schema that specifies:

1. **What to store in short-term memory** during a conversation about budgeting
2. **What to store in long-term memory** across sessions
3. **How information might move** from short-term to long-term storage
4. **What should probably NOT be stored** (and why)

Write out your schema as a structured outline or diagram. Think about data types, categories, and how you'd organize the information.

► `part_3_agents/chapter_13_agent_memory/exercise_2_13_1_solution.md`

**Exercise 3: Memory Retrieval Strategy**

Consider this scenario: You have a personal assistant agent with long-term memory containing hundreds of stored facts about a user. The user asks: "What restaurant should I try this weekend?"

Design a retrieval strategy that answers:

1. What memory categories might be relevant to this question?
2. How would you decide which specific memories to retrieve? (You can't load them all into context)
3. How would you handle conflicting or outdated information?
4. How would you format the retrieved memories for the LLM to use effectively?

Write out your strategy as a step-by-step algorithm or flowchart, with explanations for each decision.

► `part_3_agents/chapter_13_agent_memory/exercise_3_13_1_solution.md`

---

### Section 13.2

**Exercise 1: Basic Memory Implementation**

Create a simple conversation memory system that:
1. Stores messages in a list
2. Includes a system prompt: "You are a helpful math tutor."
3. Has a `chat()` function that maintains history
4. Prints the total message count after each exchange

Test it with this sequence:
- "What is 5 + 3?"
- "Now multiply that by 2"
- "What were we calculating?"

► `part_3_agents/chapter_13_agent_memory/exercise_1_13_2_solution.py`

**Exercise 2: Smart Trimming**

Extend the basic memory system to implement token-aware trimming:
1. Count tokens using a simple approximation (words × 1.3)
2. Set a maximum token limit of 500 tokens
3. When trimming, keep the system prompt and most recent messages
4. Print a warning when trimming occurs

Test with a conversation that would exceed 500 tokens to verify trimming works.

► `part_3_agents/chapter_13_agent_memory/exercise_2_13_2_solution.py`

**Exercise 3: Conversation Analytics**

Build a ConversationMemory class that includes analytics:
1. Track message counts by role (user vs assistant)
2. Track average message length
3. Store timestamps and calculate conversation duration
4. Identify the longest message in the conversation
5. Provide a `get_stats()` method returning all analytics

Create a sample conversation and display the statistics.

► `part_3_agents/chapter_13_agent_memory/exercise_3_13_2_solution.py`

---

### Section 13.3

**Exercise 1: Basic Summarization**

Write a function `summarize_messages(messages)` that:
1. Takes a list of message dictionaries (role/content)
2. Formats them into readable text
3. Uses an LLM to generate a summary
4. Returns the summary string

Test it with a sample 5-message conversation about planning a vacation.

► `part_3_agents/chapter_13_agent_memory/exercise_1_13_3_solution.py`

**Exercise 2: Triggered Summarization**

Build a `SmartMemory` class that:
1. Tracks messages normally
2. Automatically triggers summarization when message count exceeds 15
3. Keeps the 5 most recent messages intact
4. Stores the summary as a system message
5. Prints a notification when summarization occurs

Test with a conversation that grows past the threshold.

► `part_3_agents/chapter_13_agent_memory/exercise_2_13_3_solution.py`

**Exercise 3: Domain-Specific Summaries**

Create a summarization system for a **medical consultation assistant** that:
1. Uses a specialized summary prompt that extracts:
   - Symptoms mentioned
   - Duration of symptoms
   - Medications discussed
   - Recommendations given
   - Follow-up items
2. Structures the summary in a specific format (not free-form prose)
3. Validates that key medical information isn't lost
4. Includes a `get_medical_summary()` method returning structured data

Test with a mock medical consultation conversation.

► `part_3_agents/chapter_13_agent_memory/exercise_3_13_3_solution.py`

---

### Section 13.4

**Exercise 1: Basic Entity Extraction**

Write a function that extracts entities from a message and prints them. Test with: "John from marketing wants to discuss the Phoenix project with the Tokyo team next Tuesday."

► `part_3_agents/chapter_13_agent_memory/exercise_1_13_4_solution.py`

**Exercise 2: Entity Memory Class**

Create an `EntityMemory` class that:
1. Stores entities with names, types, and facts
2. Updates existing entities with new information
3. Retrieves entities by name
4. Formats relevant entities for LLM context

Test by processing 3-4 messages that mention overlapping entities.

► `part_3_agents/chapter_13_agent_memory/exercise_2_13_4_solution.py`

**Exercise 3: Entity-Aware Agent**

Build a simple agent that:
1. Maintains conversation history
2. Extracts and stores entities from each exchange
3. Retrieves relevant entity context before responding
4. Shows what entities it knows when asked "What do you know about [name]?"

Keep the implementation focused - under 80 lines total.

► `part_3_agents/chapter_13_agent_memory/exercise_3_13_4_solution.py`

---

### Section 13.5

**Exercise 1: Basic Semantic Search**

Create a `SemanticMemory` class that:
1. Stores text with embeddings using ChromaDB
2. Has `add(text)` and `search(query)` methods
3. Returns the top 3 most similar results

Test by adding 5 facts about different topics and searching for related concepts.

► `part_3_agents/chapter_13_agent_memory/exercise_1_13_5_solution.py`

**Exercise 2: Memory with Categories**

Extend your semantic memory to:
1. Store memories with a "category" metadata field
2. Add a `search_category(query, category)` method that filters by category
3. Track how many memories exist per category

Test with memories in categories like "work", "personal", "ideas".

► `part_3_agents/chapter_13_agent_memory/exercise_2_13_5_solution.py`

**Exercise 3: Conversational Agent with Semantic Recall**

Build an agent that:
1. Maintains conversation history
2. Stores each exchange in semantic memory
3. Retrieves relevant past conversations when responding
4. Has a `remember(fact)` method for explicit memory storage
5. Shows retrieved memories in debug output

Test with a multi-turn conversation where later questions relate to earlier topics.

► `part_3_agents/chapter_13_agent_memory/exercise_3_13_5_solution.py`

---

### Section 13.6

**Exercise 1: Basic Chat with Memory**

Create a chat using `RunnableWithMessageHistory` that:
1. Uses in-memory `ChatMessageHistory`
2. Remembers the user's name across 3 messages
3. Prints the full history at the end

► `part_3_agents/chapter_13_agent_memory/exercise_1_13_6_solution.py`

**Exercise 2: Windowed Memory**

Build a chatbot that:
1. Uses `trim_messages` to keep only ~100 tokens
2. Has a 6-message conversation
3. Demonstrates early messages are forgotten
4. Shows what the bot remembers at the end

► `part_3_agents/chapter_13_agent_memory/exercise_2_13_6_solution.py`

**Exercise 3: Agent with Memory Management**

Create an agent that:
1. Has 2 tools (calculator, weather)
2. Manages memory with automatic summarization
3. Keeps only recent messages after summarizing
4. Demonstrates memory works across tool calls

► `part_3_agents/chapter_13_agent_memory/exercise_3_13_6_solution.py`

---

## Challenge Project: Personal AI Assistant with Production-Ready Memory

Time to put everything together! Build a complete personal AI assistant with production-ready memory management.

> `part_3_agents/chapter_13_agent_memory/personal_assistant_challenge.py`

### Requirements:

Your assistant must:
1. **Remember conversations** across sessions (persistence)
2. **Track entities** mentioned in conversations
3. **Use tools** (at least 2: calculator and weather)
4. **Implement semantic search** to recall past conversations
5. **Auto-summarize** when conversations get long
6. **Handle privacy** with PII filtering
7. **Implement cleanup** with 30-day retention
8. **Support multiple users** with isolated memories

### Bonus Challenges:
- Add a "remember" command for explicit fact storage
- Implement importance-based cleanup
- Add conversation export (GDPR compliance)
- Build a simple CLI interface
- Track and report memory metrics

### Evaluation Criteria:
- Does it remember across sessions?
- Can it use tools correctly?
- Does semantic search find relevant past conversations?
- Are entities tracked properly?
- Does summarization trigger appropriately?
- Is PII filtered before storage?
