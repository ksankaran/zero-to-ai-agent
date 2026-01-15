# From: Building AI Agents, Chapter 14, Section 14.4
# File: exercise_3_14_4_solution.py (Code Review Agent - combines exercises 1, 2, 3)

"""
Complete Code Review Agent demonstrating:
- Exercise 1: State design with TypedDict
- Exercise 2: Node implementations
- Exercise 3: Graph construction with conditional edges

This agent analyzes code, identifies issues, suggests fixes for each,
and loops until all issues are addressed.
"""

from typing import TypedDict, Annotated, Optional
from operator import add
from langgraph.graph import StateGraph, END


# =============================================================================
# EXERCISE 1 SOLUTION: State Design
# =============================================================================

class CodeReviewState(TypedDict):
    # Input
    code: str                                    # The code to review
    language: str                                # Programming language
    
    # Analysis results
    issues: Annotated[list, add]                 # List of identified issues
                                                 # Each issue: {"id": str, "severity": str, 
                                                 #              "description": str, "line": int}
    
    # Fix tracking  
    suggested_fixes: Annotated[list, add]        # Fixes for issues
                                                 # Each fix: {"issue_id": str, "suggestion": str,
                                                 #            "fixed_code": str}
    
    addressed_issue_ids: Annotated[list, add]    # IDs of issues that have fixes
    
    # Control flow
    current_issue_index: int                     # Which issue we're working on
    review_complete: bool                        # Are we done?
    
    # Optional metadata
    summary: Optional[str]                       # Final review summary


# =============================================================================
# EXERCISE 2 SOLUTION: Node Implementations
# =============================================================================

def analyze_code(state: CodeReviewState) -> dict:
    """Analyze the code and identify issues."""
    code = state["code"]
    language = state["language"]
    
    # In reality, this would use an LLM or static analysis tool
    # Pseudocode for the logic:
    #
    # prompt = f"""Analyze this {language} code for issues:
    # {code}
    # 
    # Return a list of issues with severity (high/medium/low),
    # description, and line number."""
    # 
    # response = llm.invoke(prompt)
    # issues = parse_issues(response)
    
    # For demo, pretend we found some issues:
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
    code = state["code"]
    
    # Get the current issue
    current_issue = issues[current_index]
    
    # In reality, this would use an LLM:
    # prompt = f"""Given this code:
    # {code}
    # 
    # Suggest a fix for this issue:
    # {current_issue['description']} on line {current_issue['line']}
    # 
    # Return the suggested fix and corrected code snippet."""
    #
    # response = llm.invoke(prompt)
    # fix = parse_fix(response)
    
    # For demo:
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
    
    # Are all issues addressed?
    all_issue_ids = {issue["id"] for issue in issues}
    addressed_set = set(addressed_ids)
    
    is_complete = all_issue_ids == addressed_set
    
    # If complete, generate summary
    if is_complete:
        summary = f"Review complete. Found {len(issues)} issues, all addressed."
    else:
        summary = None  # Don't set summary until complete
    
    return {
        "review_complete": is_complete,
        "summary": summary if is_complete else state.get("summary")
    }


# =============================================================================
# EXERCISE 3 SOLUTION: Graph Construction
# =============================================================================

def should_continue(state: CodeReviewState) -> str:
    """Decide whether to continue or finish."""
    if state["review_complete"]:
        return "done"
    else:
        return "continue"


def build_code_review_graph():
    """Build and return the code review agent graph."""
    
    # Create the graph with our state type
    graph = StateGraph(CodeReviewState)
    
    # Add all nodes
    graph.add_node("analyze_code", analyze_code)
    graph.add_node("suggest_fix", suggest_fix)
    graph.add_node("check_complete", check_complete)
    
    # Set the entry point
    graph.set_entry_point("analyze_code")
    
    # Add edges
    graph.add_edge("analyze_code", "suggest_fix")
    graph.add_edge("suggest_fix", "check_complete")
    
    # Conditional edge from check_complete
    graph.add_conditional_edges(
        "check_complete",
        should_continue,
        {
            "done": END,
            "continue": "suggest_fix"  # Loop back
        }
    )
    
    # Compile and return
    return graph.compile()


# =============================================================================
# Main execution
# =============================================================================

if __name__ == "__main__":
    # Build the graph
    app = build_code_review_graph()
    
    # Example code to review
    sample_code = """
def process_data(data):
    unused_var = 42
    result = data.get('value')
    return result.upper()  # Potential None error
"""
    
    # Run the review
    result = app.invoke({
        "code": sample_code,
        "language": "python",
        "issues": [],
        "suggested_fixes": [],
        "addressed_issue_ids": [],
        "current_issue_index": 0,
        "review_complete": False
    })
    
    # Display results
    print("=" * 50)
    print("CODE REVIEW RESULTS")
    print("=" * 50)
    
    print(f"\n📋 Issues Found: {len(result['issues'])}")
    for issue in result['issues']:
        print(f"   [{issue['severity'].upper()}] Line {issue['line']}: {issue['description']}")
    
    print(f"\n🔧 Fixes Suggested: {len(result['suggested_fixes'])}")
    for fix in result['suggested_fixes']:
        print(f"   Issue {fix['issue_id']}: {fix['suggestion']}")
    
    print(f"\n✅ {result['summary']}")
