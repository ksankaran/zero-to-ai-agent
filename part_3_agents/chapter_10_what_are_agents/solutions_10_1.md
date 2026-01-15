# Chapter 10, Section 10.1: From Chatbots to Agents - Exercise Solutions

## Exercise 1 Solution: Agent or Chatbot?

1. **Customer asking about store hours**
   - **Choice:** Chatbot
   - **Reasoning:** Simple information retrieval, no decision-making needed, single response suffices

2. **Planning a multi-city business trip with specific requirements**
   - **Choice:** Agent
   - **Reasoning:** Requires coordination of multiple elements (flights, hotels, transportation), needs to make decisions based on constraints, must use multiple tools and maintain state

3. **Answering FAQ questions on a website**
   - **Choice:** Chatbot
   - **Reasoning:** Straightforward Q&A format, no actions needed beyond providing information

4. **Monitoring server logs and responding to errors**
   - **Choice:** Agent
   - **Reasoning:** Requires continuous monitoring, must make decisions about severity, needs to take actions (alerts, restarts, escalation)

5. **Having a philosophical discussion about consciousness**
   - **Choice:** Chatbot
   - **Reasoning:** Conversational and exploratory, no tools or actions needed, just dialogue

6. **Managing inventory and automatically reordering supplies**
   - **Choice:** Agent
   - **Reasoning:** Needs to track state (inventory levels), must make decisions (when to reorder), requires tool use (placing orders)

7. **Providing emotional support and listening**
   - **Choice:** Chatbot
   - **Reasoning:** Focus is on conversation and empathy, no external actions required

8. **Coordinating a team meeting across multiple time zones**
   - **Choice:** Agent
   - **Reasoning:** Must check multiple calendars, needs to calculate time zones, takes action to send invites

## Exercise 2 Solution: Design an Agent Loop

**Task Chosen:** Finding and summarizing the top 5 news articles about a company

**Agent Loop Design:**

**Iteration 1: Initial Search**
- Observe: User wants news summary about TechCorp
- Think: Need to search multiple news sources, should look for recent articles (last 7 days)
- Act: Search for "TechCorp news" with date filter
- Result: Found 47 articles

**Iteration 2: Filter and Rank**
- Observe: Have 47 articles, too many to process
- Think: Need to filter for relevance and recency
- Act: Rank by relevance score and publication date
- Result: Narrowed to 23 highly relevant articles

**Iteration 3: Fetch Content**
- Observe: Have list of 23 articles
- Think: Need full content to properly summarize
- Act: Fetch full text of top 10 articles
- Result: Retrieved 10 articles (3 were paywalled)

**Iteration 4: Select Top 5**
- Observe: Have 10 full articles
- Think: Must select the most newsworthy and diverse
- Act: Rank by importance and select top 5
- Result: Top 5 articles identified

**Iteration 5: Summarize**
- Observe: Have 5 selected articles
- Think: Need to extract key points from each
- Act: Generate summary for each article
- Result: Individual summaries created

**Iteration 6: Create Report**
- Observe: Have 5 individual summaries
- Think: Need cohesive overall summary
- Act: Create unified report with key themes
- Result: Final summary delivered
- Completion: Task complete!

## Exercise 3 Solution: Autonomy Level Assessment

1. **An email filter that marks messages as spam**
   - **Level:** 1 (Notification Bot)
   - **Reasoning:** Just classifies and notifies, doesn't take independent action, no real decision-making

2. **A trading bot that buys and sells stocks based on patterns**
   - **Level:** 4 (Delegated Agent)
   - **Reasoning:** Operates independently within defined parameters, makes complex decisions, executes trades autonomously

3. **A writing assistant that suggests grammar corrections**
   - **Level:** 2 (Suggestion Assistant)
   - **Reasoning:** Provides suggestions but doesn't act, user must accept/reject, advisory role only

4. **A personal assistant that manages your entire calendar**
   - **Level:** 4 (Delegated Agent)
   - **Reasoning:** Handles complex scheduling autonomously, makes decisions about conflicts, acts independently within its domain

5. **A customer service agent that can process refunds up to $100**
   - **Level:** 3 (Supervised Agent)
   - **Reasoning:** Can act independently for small amounts, requires approval for larger refunds, supervised autonomy

6. **A research assistant that writes complete reports on topics**
   - **Level:** 4-5 (Delegated to Autonomous)
   - **Reasoning:** Level 4 if it waits for requests, Level 5 if it proactively identifies research needs
