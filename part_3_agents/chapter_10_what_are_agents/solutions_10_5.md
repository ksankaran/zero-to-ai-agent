# Chapter 10, Section 10.5: When to Use Agents vs Simple LLM Calls - Exercise Solutions

## Exercise 1 Solution: Quick Decisions

1. **Generate 10 creative product names for a new smartphone**
   - **Decision:** Simple LLM Call
   - **Why:** Creative generation, single transformation, no external data needed

2. **Monitor competitor prices and alert when they change**
   - **Decision:** Agent
   - **Why:** Requires continuous monitoring, external data access, taking actions (alerts)

3. **Convert this Python code to JavaScript**
   - **Decision:** Simple LLM Call
   - **Why:** Single transformation, self-contained, one-shot task

4. **Debug this SQL query by trying different variations until it works**
   - **Decision:** Agent
   - **Why:** Requires iteration, testing against database, goal-oriented (works = success)

5. **Write a summary of this meeting transcript**
   - **Decision:** Simple LLM Call
   - **Why:** Single document processing, no external data, one pass sufficient

6. **Find and book the cheapest flight to Paris next month**
   - **Decision:** Agent
   - **Why:** Needs tools (search, compare, book), multiple steps, external APIs

7. **Explain what this error message means**
   - **Decision:** Simple LLM Call
   - **Why:** Knowledge-based response, no tools needed, single answer

8. **Automatically respond to customer emails based on their category**
   - **Decision:** Agent
   - **Why:** Needs email access, categorization logic, different responses, sending capability

## Exercise 2 Solution: Smart Documentation Assistant Design

**Feature Analysis:**

**1. Ask questions about docs**
- **Approach:** Simple LLM Call
- **Reasoning:** Q&A on existing content, no tools needed beyond semantic search
- **Implementation:** Embed docs once, use vector search + LLM for answers
- **Hybrid Note:** Could cache common questions for even simpler retrieval

**2. Request code examples**
- **Approach:** Simple LLM Call (mostly)
- **Reasoning:** Generate from knowledge or templates, single transformation
- **Hybrid Consideration:** Could become agent if examples need testing/validation
- **Implementation:** Template-based generation with LLM completion

**3. Report broken links**
- **Approach:** Agent
- **Reasoning:** Needs to check links, track reports, update issue tracker
- **Implementation:** Link checker tool + GitHub API integration
- **Workflow:** Check link → Verify broken → Create issue → Track status

**4. Suggest improvements**
- **Approach:** Hybrid
- **Reasoning:** Simple LLM for generating suggestions, Agent for implementing
- **Implementation Options:**
  - LLM Only: Generate suggestions as text
  - Agent Enhanced: Create PRs, update docs, track suggestions
- **Decision Factor:** Whether you want automated implementation or just ideas

**Overall Architecture:**
- Default to Simple LLM for most interactions (faster, cheaper)
- Trigger agent mode when action is needed (broken links, PR creation)
- Use smart routing based on user intent classification

## Exercise 3 Solution: Cost Analysis for Startup

**Startup Needs:**
1. Generate 100 product descriptions daily
2. Process 50 customer support tickets daily

**Analysis:**

### Need 1: Product Descriptions

**Approach:** Simple LLM Calls
- **Why:** Pure generation task, no iteration or tools needed
- **Implementation:** Batch processing with templates
- **Token Breakdown:**
  - Input prompt + product data: ~100 tokens
  - Generated description: ~200 tokens
  - Total per description: 300 tokens
- **Daily Usage:** 100 × 300 = 30,000 tokens
- **Daily Cost:** 30,000 × $0.00002 = $0.60
- **Monthly Cost:** $18

**Optimization Tips:**
- Use GPT-3.5-turbo instead of GPT-4
- Create templates to reduce prompt size
- Cache similar products' descriptions

### Need 2: Customer Support Tickets

**Smart Hybrid Approach:**

**Ticket Classification First (50 tickets):**
- Quick LLM call to categorize complexity
- 50 tokens per classification
- Cost: $0.05/day

**Tier 1: Simple Queries (30% = 15 tickets)**
- Type: Password resets, account info, order status
- Approach: Simple LLM Call
- Tokens: 200 each
- Daily tokens: 3,000
- Daily cost: $0.06

**Tier 2: Standard Issues (50% = 25 tickets)**
- Type: Billing questions, returns, feature help
- Approach: Light Agent (2-3 iterations)
- Tokens: 500 each
- Daily tokens: 12,500
- Daily cost: $0.25

**Tier 3: Complex Cases (20% = 10 tickets)**
- Type: Technical bugs, escalations, multi-issue
- Approach: Full Agent (5+ iterations)
- Tokens: 1,500 each
- Daily tokens: 15,000
- Daily cost: $0.30

**Support Total:**
- Classification: $0.05
- Tier 1: $0.06
- Tier 2: $0.25
- Tier 3: $0.30
- Daily Total: $0.66
- Monthly: $20

### Combined Analysis:

**Total Costs:**
- Product Descriptions: $18/month
- Customer Support: $20/month
- Total: $38/month

**Value Generated:**
- Time Saved: ~10 hours/week
- Human Cost Equivalent: 10 hrs × $25/hr × 4 weeks = $1,000/month
- ROI: 2,532% (!)

**Recommendation:**

**Phase 1 (Immediate):**
- Implement simple LLM for product descriptions
- Set up classification for support tickets
- Handle Tier 1 with simple LLM

**Phase 2 (Month 2):**
- Add light agent for Tier 2 support
- Optimize prompts based on data

**Phase 3 (Month 3):**
- Implement full agent for complex cases
- Add learning from resolved tickets

**Key Insight:**
The hybrid approach (using simple LLM where possible, agents only where needed) delivers maximum ROI. You're spending $38/month to save $1,000+ in human time - that's the 10x value rule in action!
