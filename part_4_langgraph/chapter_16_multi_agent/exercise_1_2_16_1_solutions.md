## Section 16.1 Solutions: Exercises 1 & 2

**Exercise 1 Solution: Multi-Agent Decision Analysis**

Here's the analysis for each scenario, with justification for the architectural decision.

---

**Scenario 1: FAQ Chatbot**

**Decision:** Single Agent ✅

**Justification:** FAQs are a single domain with a unified knowledge base. The context is consistent (product information), and the task is straightforward retrieval and response. Adding multiple agents would create unnecessary coordination overhead.

---

**Scenario 2: Legal Contract Review**

**Decision:** Multiple Agents (3 agents) ✅

**Agents:**
| Agent | Responsibility |
|-------|----------------|
| **Compliance Checker** | Scans for regulatory issues, missing clauses, legal requirements |
| **Risk Analyst** | Identifies problematic terms, unfavorable conditions, liability exposure |
| **Revision Suggester** | Proposes alternative language, improved clauses |

**Justification:** Legal review requires different types of expertise. Compliance checking needs regulatory knowledge. Risk analysis needs business context. Revision writing needs legal drafting skills. These are distinct specialties that benefit from focused prompts and separate tools.

---

**Scenario 3: Customer Service System**

**Decision:** Multiple Agents (3-4 agents) ✅

**Agents:**
| Agent | Responsibility |
|-------|----------------|
| **Triage Agent** | Classifies incoming issues, routes to appropriate handler |
| **Complaint Handler** | Empathetic resolution of customer complaints |
| **Refund Processor** | Handles financial transactions, policy checks |
| **Escalation Agent** | Prepares complex cases for human review |

**Justification:** Different types of customer interactions require different tools (refund system vs. knowledge base) and different tones (empathetic vs. transactional). Escalation logic should be separate to ensure complex cases get proper handling.

---

**Scenario 4: Translation Tool**

**Decision:** Single Agent ✅ (possibly two for complex documents)

**Justification:** Translation is a focused, single-domain task. One agent with translation capabilities is sufficient. For very complex documents, you might add a second agent for quality review, but for most cases, single agent works well.

---

**Scenario 5: AI Research Assistant**

**Decision:** Multiple Agents (4 agents) ✅

**Agents:**
| Agent | Responsibility |
|-------|----------------|
| **Paper Finder** | Searches databases, filters by relevance, retrieves papers |
| **Summarizer** | Reads and condenses paper content |
| **Gap Analyst** | Identifies missing research, contradictions, opportunities |
| **Experiment Designer** | Suggests methodologies based on gaps |

**Justification:** This workflow spans distinct activities that require different tools and contexts. The paper finder needs database access, the summarizer needs reading skills, the gap analyst needs synthesis abilities, and the experiment designer needs domain methodology knowledge.

---

**Exercise 2 Solution: Agent Boundary Design**

Here's a complete agent architecture for the content creation pipeline:

**Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT CREATION PIPELINE                 │
└─────────────────────────────────────────────────────────────┘

     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
     │   Research   │────▶│   Ideation   │────▶│   Drafting   │
     │    Agent     │     │    Agent     │     │    Agent     │
     └──────────────┘     └──────────────┘     └──────────────┘
                                                      │
     ┌──────────────┐     ┌──────────────┐           │
     │    Social    │◀────│    Editor    │◀──────────┘
     │    Agent     │     │    Agent     │
     └──────────────┘     └──────────────┘
                                ▲
                                │
                          ┌──────────────┐
                          │    Fact      │
                          │   Checker    │
                          └──────────────┘
```

**Agent Specifications**

| Agent | Responsibility | Tools | Input | Output |
|-------|---------------|-------|-------|--------|
| **Research Agent** | Find trending industry topics | Web search, news APIs, social listening tools | Industry/topic keywords | List of trending topics with supporting data |
| **Ideation Agent** | Generate content ideas | Brainstorming prompts, competitor analysis | Trending topics list | Ranked content ideas with angles |
| **Drafting Agent** | Write first draft | Content templates, research notes | Selected content idea | Complete article draft |
| **Fact Checker Agent** | Verify claims and data | Fact-checking databases, source verification | Article draft | Annotated draft with verification notes |
| **Editor Agent** | Polish for brand voice | Style guide, brand tone examples | Verified draft | Publication-ready article |
| **Social Agent** | Create promotional snippets | Social templates, hashtag tools | Final article | Platform-specific social posts |

**System Prompts (abbreviated)**

**Research Agent:**
> You are an industry research specialist. Find trending topics using data and evidence. Output: JSON with topics, trend scores, and source links.

**Ideation Agent:**
> You are a creative content strategist. Generate compelling content angles from research. Output: Ranked list of ideas with headline and angle.

**Drafting Agent:**
> You are a professional content writer. Write engaging, informative articles. Output: Complete article draft in markdown.

**Fact Checker Agent:**
> You are a rigorous fact checker. Verify every claim, statistic, and quote. Output: Original text with [VERIFIED] or [NEEDS SOURCE] tags.

**Editor Agent:**
> You are a brand voice specialist. Our voice is: professional yet approachable, data-driven, optimistic. Output: Polished article matching brand guidelines.

**Social Agent:**
> You are a social media expert. Create platform-appropriate promotional content. Output: Posts for Twitter, LinkedIn, and Instagram.

---

**Key Concepts Demonstrated**

**Exercise 1 shows:**
- How to evaluate task complexity for architectural decisions
- The importance of considering domain overlap
- Identifying natural boundaries in workflows

**Exercise 2 shows:**
- Systematic agent boundary design
- How to define clear inputs/outputs for each agent
- Information flow mapping in multi-agent systems