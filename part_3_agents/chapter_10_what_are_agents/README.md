# Chapter 10: What Are AI Agents?

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
mkdir part_3_agents\chapter_10_what_are_agents
cd part_3_agents\chapter_10_what_are_agents
```

**On Mac/Linux:**
```bash
mkdir -p part_3_agents/chapter_10_what_are_agents
cd part_3_agents/chapter_10_what_are_agents
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

6. Install the required packages for Chapter 10:

► `part_3_agents/chapter_10_what_are_agents/requirements.txt`

Or copy and create the file yourself:
```
# requirements.txt
# Chapter 10 is conceptual - no external packages required!
# All examples use Python built-in functionality only.

# Optional: If you want to experiment with the concepts discussed,
# you might want these in preparation for Chapter 11:
# openai>=2.9.0
# python-dotenv>=1.2.1
```

Then install with:
```
pip install -r requirements.txt
```

This chapter focuses on understanding agent concepts rather than implementation:
- All code examples are conceptual demonstrations
- Exercise solutions use only Python standard library
- Actual agent building with dependencies starts in Chapter 11

---

## Practice Exercises

### Section 10.1

**Exercise 1: Agent or Chatbot?**

For each scenario below, decide whether a chatbot or agent would be better suited, and explain why:

1. Customer asking about store hours
2. Planning a multi-city business trip with specific requirements
3. Answering FAQ questions on a website
4. Monitoring server logs and responding to errors
5. Having a philosophical discussion about consciousness
6. Managing inventory and automatically reordering supplies
7. Providing emotional support and listening
8. Coordinating a team meeting across multiple time zones

► `part_3_agents/chapter_10_what_are_agents/solutions_10_1.md#exercise-1-solution`

**Exercise 2: Design an Agent Loop**

Choose one of these tasks and sketch out how an agent would handle it (just the concept, no code needed):
- Booking a restaurant reservation for 6 people with dietary restrictions
- Finding and summarizing the top 5 news articles about a company
- Organizing a birthday party within a budget

Your design should include:
- What the agent observes
- How it reasons about the task
- What tools it might need
- What decisions it makes
- How it knows when it's done

► `part_3_agents/chapter_10_what_are_agents/solutions_10_1.md#exercise-2-solution`

**Exercise 3: Autonomy Level Assessment**

For each agent description, assign it an autonomy level (1-5) and explain your reasoning:

1. An email filter that marks messages as spam
2. A trading bot that buys and sells stocks based on patterns
3. A writing assistant that suggests grammar corrections
4. A personal assistant that manages your entire calendar
5. A customer service agent that can process refunds up to $100
6. A research assistant that writes complete reports on topics

► `part_3_agents/chapter_10_what_are_agents/solutions_10_1.md#exercise-3-solution`

---

### Section 10.2

**Exercise 1: Component Identification**

For each agent behavior below, identify which component(s) are primarily responsible:

1. Remembering that a user prefers morning meetings
2. Deciding to check weather before suggesting outdoor activities
3. Using a calculator to split a restaurant bill
4. Learning from a failed attempt and trying a different approach
5. Knowing which API to call for stock prices
6. Maintaining conversation context across multiple turns

► `part_3_agents/chapter_10_what_are_agents/solutions_10_2.md#exercise-1-solution`

**Exercise 2: Design Challenge**

Design an agent to help with meal planning. Specify:
- What reasoning patterns it would use
- What tools it would need
- What types of memory would be most important

Consider these scenarios:
- User has dietary restrictions
- Budget constraints exist
- Previous meals should influence suggestions
- Needs to check ingredient availability

► `part_3_agents/chapter_10_what_are_agents/solutions_10_2.md#exercise-2-solution`

**Exercise 3: Component Interaction Mapping**

A user asks: "Book a flight to Seattle for my conference"

Map out how the three components would interact:
1. What would reasoning determine first?
2. What memory would be relevant?
3. What sequence of tools would be needed?
4. How would they work together to handle complications (like sold out flights)?

► `part_3_agents/chapter_10_what_are_agents/solutions_10_2.md#exercise-3-solution`

---

### Section 10.3

**Exercise 1: Loop Stage Identification**

For each action below, identify which loop stage it represents (Observe/Think/Act/Reflect/Learn):

1. Checking if a file exists before trying to read it
2. Deciding to use a web search tool for current information
3. Calling an API to get weather data
4. Noting that the last approach didn't work
5. Updating memory with a new user preference discovered during conversation
6. Reading the user's question at the start

► `part_3_agents/chapter_10_what_are_agents/solutions_10_3.md#exercise-1-solution`

**Exercise 2: Loop Design Challenge**

Design an agent loop to handle: "Order pizza for the office party"

For each loop iteration, specify:
- What triggers the next iteration
- What state needs to be tracked
- What would cause the loop to end
- How to handle common problems (restaurant closed, items unavailable)

Include at least 4 iterations showing different scenarios.

► `part_3_agents/chapter_10_what_are_agents/solutions_10_3.md#exercise-2-solution`

**Exercise 3: Loop Problem Diagnosis**

An agent tasked with "Schedule a meeting with all team members" exhibits these behaviors:
- Keeps asking for team member names even after being told
- Checks the same calendar repeatedly
- Never actually sends the meeting invite
- Eventually times out after 50 iterations

What loop problems are occurring? How would you fix each one?

► `part_3_agents/chapter_10_what_are_agents/solutions_10_3.md#exercise-3-solution`

---

### Section 10.4

**Exercise 1: Agent Type Matching**

For each scenario, identify the best agent type and explain why:

1. Generating personalized workout plans based on user goals
2. Monitoring security cameras and alerting on suspicious activity
3. Writing and refining product descriptions for an e-commerce site
4. Orchestrating a complex CI/CD pipeline
5. Providing therapy-like emotional support
6. Conducting competitive analysis for a business

► `part_3_agents/chapter_10_what_are_agents/solutions_10_4.md#exercise-1-solution`

**Exercise 2: Hybrid Design Challenge**

Design a hybrid agent for a travel booking system that:
- Takes user preferences (budget, dates, interests)
- Searches for flights and hotels
- Plans daily itineraries
- Handles changes and cancellations

Specify:
- Which agent type handles which part
- When to switch between types
- How they share information

► `part_3_agents/chapter_10_what_are_agents/solutions_10_4.md#exercise-2-solution`

**Exercise 3: Cost-Performance Analysis**

You're building a customer service system that handles 1000 requests/day. Compare:
- ReAct agent: 500 tokens average per request
- Plan-and-Execute: 300 tokens average per request
- Tool-Calling: 100 tokens average per request

If each provides 85%, 75%, and 60% customer satisfaction respectively, which would you choose and why? Consider both cost and quality.

► `part_3_agents/chapter_10_what_are_agents/solutions_10_4.md#exercise-3-solution`

---

### Section 10.5

**Exercise 1: Quick Decisions**

For each task, decide: Simple LLM Call or Agent? Explain why.

1. Generate 10 creative product names for a new smartphone
2. Monitor competitor prices and alert when they change
3. Convert this Python code to JavaScript
4. Debug this SQL query by trying different variations until it works
5. Write a summary of this meeting transcript
6. Find and book the cheapest flight to Paris next month
7. Explain what this error message means
8. Automatically respond to customer emails based on their category

► `part_3_agents/chapter_10_what_are_agents/solutions_10_5.md#exercise-1-solution`

**Exercise 2: Design Challenge**

You're building a "Smart Documentation Assistant". Users can:
- Ask questions about your docs
- Request code examples
- Report broken links
- Suggest improvements

For each feature:
- Decide: LLM call or agent?
- Explain your reasoning
- Consider hybrid approaches

► `part_3_agents/chapter_10_what_are_agents/solutions_10_5.md#exercise-2-solution`

**Exercise 3: Cost Analysis**

Your startup has two needs:
1. Generate 100 product descriptions daily
2. Process customer support tickets (50/day)

Compare costs and design:
- All simple LLM calls where possible
- All agents where beneficial
- Calculate token usage difference
- Recommend optimal approach

► `part_3_agents/chapter_10_what_are_agents/solutions_10_5.md#exercise-3-solution`

---

### Section 10.6

**Exercise 1: Industry Analysis**

Pick an industry not covered above (agriculture, logistics, hospitality, etc.) and design an agent application:
- What problem would it solve?
- What tools would it need?
- What type of agent architecture fits best?
- What would be the success metrics?
- What are the main challenges?

► `part_3_agents/chapter_10_what_are_agents/solutions_10_6.md#exercise-1-solution`

**Exercise 2: Agent Improvement**

Choose one of the real-world examples above and identify:
- Three limitations it probably has
- How you would improve it
- What additional capabilities would make it more valuable
- Potential risks to watch for

► `part_3_agents/chapter_10_what_are_agents/solutions_10_6.md#exercise-2-solution`

**Exercise 3: Build Your Business Case**

You want to implement an agent at your work (or imaginary company):
- Define the specific problem
- Calculate potential ROI
- Identify required integrations
- List success criteria
- Create implementation phases

► `part_3_agents/chapter_10_what_are_agents/solutions_10_6.md#exercise-3-solution`

---

### Section 10.7

**Exercise 1: Failure Mode Analysis**

Design an agent for scheduling meetings. List:
- Five ways it could fail
- The impact of each failure
- How you'd detect each failure
- Your mitigation strategy

► `part_3_agents/chapter_10_what_are_agents/solutions_10_7.md#exercise-1-solution`

**Exercise 2: Cost Optimization**

Your agent currently:
- Uses 2000 tokens per customer query
- Handles 1000 queries per day
- Costs $20/day in API fees

Create a plan to reduce costs by 50% while maintaining quality.

► `part_3_agents/chapter_10_what_are_agents/solutions_10_7.md#exercise-2-solution`

**Exercise 3: Debugging Scenario**

Your e-commerce agent successfully processes orders 95% of the time but fails mysteriously for 5%. Design:
- What logging you'd implement
- How you'd identify patterns in failures
- Your debugging process
- Prevention strategies

► `part_3_agents/chapter_10_what_are_agents/solutions_10_7.md#exercise-3-solution`
