## 14.4 Core Concepts: Nodes, Edges, and State

**Exercise 1 Solution:**

```python
from typing import TypedDict, Annotated, Optional
from operator import add

class CodeReviewState(TypedDict):
    # Input
    code: str                                    # The code to review
    language: str                                # Programming language
    
    # Analysis results
    issues: Annotated[list[dict], add]          # List of identified issues
                                                 # Each issue: {"id": str, "severity": str, 
                                                 #              "description": str, "line": int}
    
    # Fix tracking  
    suggested_fixes: Annotated[list[dict], add]  # Fixes for issues
                                                  # Each fix: {"issue_id": str, "suggestion": str,
                                                  #            "fixed_code": str}
    
    addressed_issue_ids: Annotated[list[str], add]  # IDs of issues that have fixes
    
    # Control flow
    current_issue_index: int                     # Which issue we're working on
    review_complete: bool                        # Are we done?
    
    # Optional metadata
    summary: Optional[str]                       # Final review summary
```

**Design decisions explained:**

- `issues`, `suggested_fixes`, and `addressed_issue_ids` all use `Annotated[list, add]` because they accumulate over time. We find issues one by one, suggest fixes one by one, and mark them addressed one by one.

- `current_issue_index` is a plain `int` that gets replaced each time. It tracks which issue we're currently processing.

- `review_complete` is a boolean flag for the conditional edge to check.

- Each issue has an `id` so we can match fixes to issues without relying on list indices (which could shift).

- `summary` is `Optional` because it only exists at the end.

---

**Exercise 2 Solution:**

```python
def analyze_code(state: CodeReviewState) -> dict:
    """Analyze the code and identify issues."""
    code = state["code"]
    language = state["language"]
    
    # In reality, this would use an LLM or static analysis tool
    issues = [
        {"id": "issue_1", "severity": "high", 
         "description": "Potential null pointer", "line": 15},
        {"id": "issue_2", "severity": "medium",
         "description": "Unused variable", "line": 8},
    ]
    
    return {
        "issues": issues,
        "current_issue_index": 0,  # Start with first issue
        "review_complete": False
    }


def suggest_fix(state: CodeReviewState) -> dict:
    """Suggest a fix for the current issue."""
    issues = state["issues"]
    current_index = state["current_issue_index"]
    current_issue = issues[current_index]
    
    # In reality, this would use an LLM
    fix = {
        "issue_id": current_issue["id"],
        "suggestion": f"Fix for {current_issue['description']}",
        "fixed_code": "# corrected code here"
    }
    
    return {
        "suggested_fixes": [fix],
        "addressed_issue_ids": [current_issue["id"]],
        "current_issue_index": current_index + 1  # Move to next issue
    }


def check_complete(state: CodeReviewState) -> dict:
    """Check if all issues have been addressed."""
    issues = state["issues"]
    addressed_ids = state["addressed_issue_ids"]
    
    all_issue_ids = {issue["id"] for issue in issues}
    addressed_set = set(addressed_ids)
    is_complete = all_issue_ids == addressed_set
    
    summary = f"Review complete. Found {len(issues)} issues, all addressed." if is_complete else None
    
    return {
        "review_complete": is_complete,
        "summary": summary if is_complete else state.get("summary")
    }
```

**Key observations:**

- `analyze_code` reads `code` and `language`, writes `issues` and initializes control fields
- `suggest_fix` reads `issues` and `current_issue_index`, writes `suggested_fixes`, `addressed_issue_ids`, and updates `current_issue_index`
- `check_complete` reads `issues` and `addressed_issue_ids`, writes `review_complete` and optionally `summary`

Each node has a clear, single responsibility and only writes what it's responsible for.

---

**Exercise 3 Solution:**

📥 **Download:** `part_4_langgraph/chapter_14_langgraph_intro/exercise_3_14_4_solution.py`

**Graph sketch:**

```
START
   │
   ▼
┌──────────────┐
│ analyze_code │
└──────────────┘
   │
   ▼
┌─────────────┐     ┌─────────────────┐
│ suggest_fix │ ←───┤ (more issues?)  │
└─────────────┘     │    yes          │
   │                └─────────────────┘
   ▼                         ▲
┌────────────────┐           │
│ check_complete │───────────┘
└────────────────┘
   │
   │ (no more issues)
   ▼
  END
```

**The flow:**
1. Start at `analyze_code`
2. Go to `suggest_fix` 
3. Go to `check_complete`
4. If more issues remain, loop back to `suggest_fix`
5. If all issues addressed, go to END

**Key graph construction code:**

```python
# Create the graph
graph = StateGraph(CodeReviewState)

# Add nodes
graph.add_node("analyze_code", analyze_code)
graph.add_node("suggest_fix", suggest_fix)
graph.add_node("check_complete", check_complete)

# Set entry and edges
graph.set_entry_point("analyze_code")
graph.add_edge("analyze_code", "suggest_fix")
graph.add_edge("suggest_fix", "check_complete")

# Conditional edge for the loop
graph.add_conditional_edges(
    "check_complete",
    should_continue,
    {"done": END, "continue": "suggest_fix"}
)
```

The complete runnable solution is in the download file, which combines the state design, node implementations, and graph construction.