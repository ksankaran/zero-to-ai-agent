# From: Zero to AI Agent, Chapter 9, Section 9.4
# File: exercise_1_9_4_solution.py

"""
Match scenarios with appropriate prompting patterns
"""

# Scenario 1: Debug slow website
# Pattern: Chain-of-Thought + Recipe Pattern
# Reasoning: CoT breaks down debugging, Recipe provides steps

debug_website_prompt = """
Let's debug this slow website step by step.

For each potential cause, I'll:
1. Check the specific component
2. Explain how to test it
3. Describe what to look for
4. Provide the fix if this is the issue

Step 1: Network Issues
- Check: Open browser DevTools > Network tab
- Test: Reload the page and watch load times
- Look for: Red requests, long TTFB
- Fix: If TTFB > 2s, server issue

Step 2: Large Images
- Check: DevTools > Network > Filter by Img
- Test: Note file sizes
- Look for: Images over 500KB
- Fix: Compress images, use WebP
"""

# Scenario 2: Understand quantum computing
# Pattern: Alternative Approaches + Simplifier
# Reasoning: Show different perspectives at different levels

quantum_prompt = """
Explain quantum computing using 3 approaches:

Approach 1: The Physicist's View
- Focus: Superposition, entanglement
- Best for: Physics background

Approach 2: The Computer Scientist's View  
- Focus: Qubits vs bits, quantum gates
- Best for: Programmers

Approach 3: The Application View
- Focus: Drug discovery, cryptography
- Best for: General audience

For each, provide:
1. ELI5 version (no jargon)
2. Undergraduate level (some technical terms)
3. Graduate level (full technical detail)
"""

# Scenario 3: Email declining job offer
# Pattern: Role-Playing + Output Format + Constraint
# Reasoning: Role for tone, Format for structure, Constraints for brevity

decline_email_prompt = """
You are a professional who values relationships.

Write an email declining a job offer:

SUBJECT: [Professional, clear]
GREETING: [Warm, personal]
PARAGRAPH 1: [Thank them, mention positives]
PARAGRAPH 2: [Politely decline with brief reason]
PARAGRAPH 3: [Keep door open for future]
CLOSING: [Professional, warm]

Constraints:
- Under 150 words total
- Grateful tone throughout
- Clear decision
"""

# Scenario 4: Plan 3-day Paris trip
# Pattern: Recipe Pattern + Persona + Format
# Reasoning: Recipe for step-by-step, Persona for expertise, Format for organization

paris_trip_prompt = """
You are a seasoned travel planner.

Create a 3-day Paris itinerary:

DAY 1: Classic Paris
Morning (8am-12pm):
- Activity:
- Time needed:
- Insider tip:

Afternoon (12pm-5pm):
[same structure]

Evening (5pm-10pm):
[same structure]

Include for each day:
- Meal recommendations
- Transportation tips
- Walking distance
- Rain backup plan
"""

# Scenario 5: Analyze database systems
# Pattern: Alternative Approaches + Output Format + Reflection
# Reasoning: Compare options, structured format, critical reflection

database_analysis_prompt = """
Compare 3 databases for e-commerce:

For each (PostgreSQL, MongoDB, DynamoDB):

OVERVIEW: [2 sentences]
PROS:
• Performance
• Scalability
• Developer experience
• Cost

CONS:
• Limitations
• Complexity

BEST FOR: [use cases]
VERDICT: [1-10 rating]

REFLECTION:
1. What assumptions might change this?
2. What info would improve analysis?
3. Confidence level: [1-10] and why
"""