# From: Zero to AI Agent, Chapter 16, Section 16.6
# File: exercise_1_16_6_solution.py

"""
Exercise 1 Solution: State Audit

Analysis of the research team's ResearchState from Section 16.5.
This file documents which agent owns each field.
"""

# The state being audited:
"""
class ResearchState(TypedDict):
    topic: str                    
    questions: list[str]          
    findings: list[str]           
    insights: str                 
    report: str                   
    feedback: str
    revision_count: int
    approved: bool
"""

# =============================================================================
# STATE AUDIT TABLE
# =============================================================================

AUDIT = """
| Field           | Written By      | Read By                  | Replace/Accumulate |
|-----------------|-----------------|--------------------------|-------------------|
| topic           | User (input)    | Planner, Writer          | Replace (set once)|
| questions       | Planner         | Researcher               | Replace           |
| findings        | Researcher      | Analyst, Writer          | Replace*          |
| insights        | Analyst         | Writer                   | Replace           |
| report          | Writer          | Reviewer                 | Replace           |
| feedback        | Reviewer        | Writer                   | Replace           |
| revision_count  | Writer          | Routing function         | Replace (incr)    |
| approved        | Reviewer        | Routing function         | Replace           |

* findings could be Annotated[list, operator.add] if researcher runs multiple times
"""

# =============================================================================
# DATA FLOW DIAGRAM (ASCII)
# =============================================================================

DATA_FLOW = """
User Input
    │
    ▼ topic
┌─────────┐              ┌────────────┐            ┌────────────┐
│  START  │ ──────────►  │  Planner   │ ─────────► │ Researcher │
└─────────┘              └────────────┘            └────────────┘
                           questions                  findings
                                                        │
                                                        ▼
┌─────────┐    report    ┌────────────┐  insights  ┌────────────┐
│ Writer  │ ◄─────────── │   Analyst  │ ◄───────── │   Analyst  │
└─────────┘              └────────────┘            └────────────┘
    │
    │ report
    ▼
┌────────────┐  feedback   ┌─────────┐
│  Reviewer  │ ───────────►│ Writer  │ (revision loop)
└────────────┘             └─────────┘
    │
    │ approved
    ▼
┌─────────┐
│   END   │
└─────────┘
"""

# =============================================================================
# KEY OBSERVATIONS
# =============================================================================

OBSERVATIONS = """
Key Observations:

1. NO CONFLICTS: Each agent writes to its own field(s)
   - Planner → questions
   - Researcher → findings
   - Analyst → insights
   - Writer → report, revision_count
   - Reviewer → feedback, approved

2. READING IS SAFE: Multiple agents can read the same field
   - Both Analyst and Writer read 'findings'
   - Both Writer and routing function read 'approved'

3. REVISION LOOP uses:
   - feedback: Reviewer writes, Writer reads
   - revision_count: Writer increments, routing checks
   - approved: Reviewer sets, routing checks

4. POTENTIAL IMPROVEMENT:
   If Researcher ran multiple times (e.g., for different sources),
   'findings' should use: Annotated[list[str], operator.add]
"""

if __name__ == "__main__":
    print("=" * 60)
    print("EXERCISE 1 SOLUTION: State Audit")
    print("=" * 60)
    print(AUDIT)
    print("\n" + "=" * 60)
    print("DATA FLOW DIAGRAM")
    print("=" * 60)
    print(DATA_FLOW)
    print("\n" + "=" * 60)
    print("OBSERVATIONS")
    print("=" * 60)
    print(OBSERVATIONS)
