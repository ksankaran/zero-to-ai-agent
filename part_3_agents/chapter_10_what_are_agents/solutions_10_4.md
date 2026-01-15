# Chapter 10, Section 10.4: Types of Agents - Exercise Solutions

## Exercise 1 Solution: Agent Type Matching

1. **Generating personalized workout plans based on user goals**
   - **Best Agent Type:** Plan-and-Execute
   - **Why:** Well-defined task with clear steps: assess fitness level, define goals, create weekly plan, adjust for equipment. The workflow is predictable and repeatable.

2. **Monitoring security cameras and alerting on suspicious activity**
   - **Best Agent Type:** Tool-Calling
   - **Why:** Minimal reasoning needed, mostly tool execution: monitor feed, detect anomalies, send alerts. Speed and efficiency are critical.

3. **Writing and refining product descriptions for an e-commerce site**
   - **Best Agent Type:** Reflexion
   - **Why:** Quality-critical creative task that benefits from iteration and self-improvement. Each revision can enhance clarity and persuasiveness.

4. **Orchestrating a complex CI/CD pipeline**
   - **Best Agent Type:** Plan-and-Execute
   - **Why:** Predictable workflow with defined steps that rarely change. Steps are sequential and dependencies are known.

5. **Providing therapy-like emotional support**
   - **Best Agent Type:** ReAct
   - **Why:** Needs to adapt to emotional responses, explain reasoning, handle unpredictable situations. Every conversation is unique.

6. **Conducting competitive analysis for a business**
   - **Best Agent Type:** Multi-Agent
   - **Why:** Complex task requiring different specializations: market research, financial analysis, product comparison. Benefits from parallel processing.

## Exercise 2 Solution: Hybrid Design Challenge - Travel Booking System

**System Components:**

**1. Preference Gathering (ReAct Agent)**
- **Handles:** Initial consultation, understanding vague preferences
- **Why ReAct:** Needs to ask clarifying questions adaptively
- **Example:** "Beach vacation" → "Tropical or Mediterranean?" → "All-inclusive or explore?"

**2. Search Execution (Tool-Calling Agent)**
- **Handles:** Searching flights, hotels, activities across providers
- **Why Tool-Calling:** Pure execution, minimal reasoning needed
- **Example:** Query 10 APIs in parallel for best prices

**3. Itinerary Planning (Plan-and-Execute Agent)**
- **Handles:** Creating daily schedules, optimizing routes
- **Why Plan-and-Execute:** Structured task with clear optimization goals
- **Example:** Day 1 → Morning museum → Lunch nearby → Afternoon beach

**4. Change Management (ReAct Agent)**
- **Handles:** Cancellations, rebooking, dealing with disruptions
- **Why ReAct:** Must adapt dynamically to changing situations
- **Example:** Flight cancelled → Check alternatives → Coordinate hotel change

**Information Sharing:**
- Central state store with user preferences, bookings, budget
- Each agent updates state before passing control
- Supervisor agent orchestrates which specialist to invoke
- Handoff protocol ensures context preservation

**When Agents Switch:**
- Preference Gathering completes → triggers Search Execution
- Search results ready → triggers Itinerary Planning
- User requests change → triggers Change Management
- Any agent can escalate to supervisor for routing

## Exercise 3 Solution: Cost-Performance Analysis

**Current Situation:**
- 1000 requests/day
- ReAct: 500 tokens/request, 85% satisfaction, $10/day
- Plan-Execute: 300 tokens/request, 75% satisfaction, $6/day
- Tool-Calling: 100 tokens/request, 60% satisfaction, $2/day

**Analysis:**

**Option 1: All ReAct**
- Cost: $10/day
- Satisfaction: 85%
- Pros: Best quality, handles edge cases
- Cons: Most expensive

**Option 2: All Plan-Execute**
- Cost: $6/day
- Satisfaction: 75%
- Pros: Good balance of cost and quality
- Cons: Struggles with complex issues

**Option 3: All Tool-Calling**
- Cost: $2/day
- Satisfaction: 60%
- Pros: Cheapest option
- Cons: Poor customer experience

**Recommended Hybrid Approach:**

**Intelligent Request Routing:**

1. **Tier 1: Tool-Calling (60% of requests = 600/day)**
   - Handle: FAQ, password resets, order status, hours
   - Cost: 600 × 100 tokens × $0.00002 = $1.20/day
   - Satisfaction: 95% (perfect for simple tasks)

2. **Tier 2: Plan-and-Execute (30% of requests = 300/day)**
   - Handle: Returns, standard complaints, account changes
   - Cost: 300 × 300 tokens × $0.00002 = $1.80/day
   - Satisfaction: 85% (good for structured processes)

3. **Tier 3: ReAct (10% of requests = 100/day)**
   - Handle: Complex issues, escalations, unique problems
   - Cost: 100 × 500 tokens × $0.00002 = $1.00/day
   - Satisfaction: 95% (excellent for complex cases)

**Total Results:**
- Daily Cost: $4.00 (60% reduction from all-ReAct)
- Weighted Satisfaction: (0.6 × 95%) + (0.3 × 85%) + (0.1 × 95%) = 91.5%
- Better satisfaction than any single approach!

**Implementation Strategy:**
1. Build classifier to route requests (adds ~50 tokens overhead)
2. Start with conservative routing, adjust based on data
3. Monitor satisfaction per tier and optimize thresholds
4. Consider time-of-day routing (more ReAct during peak hours)

**Conclusion:** 
The hybrid approach delivers superior results: 60% cost reduction while actually improving customer satisfaction from 85% to 91.5%. This demonstrates that matching agent type to task complexity is more effective than one-size-fits-all.
