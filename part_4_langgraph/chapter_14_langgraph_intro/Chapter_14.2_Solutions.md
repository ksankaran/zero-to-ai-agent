## 14.2 Graph-Based Agent Architectures

**Exercise 1 Solution:**

1. **Translating a document from English to Spanish** → **Sequential**. This is a straightforward transformation with no decisions or loops needed. Input goes in, translation comes out.

2. **Keeps asking clarifying questions until it understands** → **Looping**. The agent asks a question, evaluates the answer, and either continues asking (loop back) or proceeds (exit loop).

3. **Checks weather in three cities simultaneously** → **Parallel (fan-out/fan-in)**. Three independent API calls can happen at the same time, then results are merged.

4. **Writes code, runs tests, fixes bugs until all tests pass** → **Looping + Agent Loop (ReAct)**. The agent thinks about what to fix, makes changes (act), runs tests (observe), and repeats until tests pass. This is iterative refinement.

5. **Drafts legal contract requiring lawyer approval** → **Human-in-the-Loop**. The agent does its work, then pauses for human review. If rejected, it revises and loops back for another review.

---

**Exercise 2 Solution:**

**Recipe Agent Graph Design**

**Nodes:**
- Get User Request (what dish they want)
- Check Available Ingredients
- Search Recipes
- Evaluate Recipe Match
- Adjust Recipe
- Generate Instructions
- Handle Question
- Finish

**Decision Points:**
- After Search: Did we find a suitable recipe?
- After Evaluate: Does the recipe work with available ingredients?
- During Cooking: Is the user asking a question or indicating they're done?

**Loops:**
- If no suitable recipe found → refine search and try again (max 3 times)
- If recipe doesn't match ingredients → search for alternative
- During cooking → answer questions and loop back to wait for more questions

**Sketch:**
```
START → Get Request → Check Ingredients → Search Recipes
                                              │
                                              ▼
                                     (found recipe?) ──no──→ Refine Search ──┐
                                              │                              │
                                             yes                             │
                                              │    ┌─────────────────────────┘
                                              ▼    ▼
                                        Evaluate Match
                                              │
                                     (works with ingredients?)
                                         │         │
                                        yes        no
                                         │         │
                                         │         └──→ Search Alternatives ───┐
                                         │                                     │
                                         ▼    ┌────────────────────────────────┘
                                   Adjust Recipe
                                         │
                                         ▼
                                Generate Instructions
                                         │
                                         ▼
                                ┌──→ Wait for User ←──────────────┐
                                │        │                        │
                                │   (question or done?)           │
                                │     │           │               │
                                │  question      done             │
                                │     │           │               │
                                │     ▼           ▼               │
                                │  Handle Q → ───┘           END  │
                                │     │                           │
                                └─────┘                           
```

**State needed:**
- Desired dish
- Available ingredients list
- Recipes found (list)
- Selected recipe
- Adjusted recipe
- Generated instructions
- Conversation history (for questions)
- Search attempt count

---

**Exercise 3 Solution:**

**Customer Service Agent State**

| State Field | Written By | Read By |
|------------|-----------|---------|
| `ticket_text` | Read Ticket node | Classify, Search, Generate Response |
| `classification` (category, urgency, complexity) | Classify node | Routing decision, Search (to tailor query), Generate Response |
| `can_bot_handle` | Classify node | Routing decision (branch to Search or Escalate) |
| `search_queries` (list of queries tried) | Search node, Refine Search node | Refine Search (to avoid repeats), Generate Response |
| `search_results` | Search node | Evaluate search decision, Generate Response |
| `found_sufficient_info` | Evaluation after Search | Routing decision (continue or refine search) |
| `search_attempt_count` | Search node | Routing decision (give up after N attempts) |
| `response_draft` | Generate Response node | Quality check, Send Response |
| `response_quality_ok` | Quality check evaluation | Routing decision (send or regenerate) |
| `generation_attempt_count` | Generate Response node | Routing decision (give up after N attempts) |
| `final_response` | Generate Response (when approved) | Send Response node |
| `escalation_reason` | Classify node (if escalating) | Escalate node |

The key insight is that state flows through the graph. Early nodes write information that later nodes need to read. The classification informs search strategy. Search results inform response generation. And counters track loop iterations to prevent infinite loops.