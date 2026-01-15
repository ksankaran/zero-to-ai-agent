# From: Zero to AI Agent, Chapter 17, Section 17.5
# Save as: exercise_2_17_5_solution.py
# Exercise 2: Dynamic Approval Workflow

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class ApprovalState(TypedDict):
    request_type: str  # "vacation", "expense", "hiring"
    amount: float  # For expense requests
    requester: str
    description: str
    approvals: list[dict]
    status: str

# Approval functions
def employee_submit(state: ApprovalState) -> dict:
    return {
        "approvals": [{
            "role": "Employee",
            "action": "submitted",
            "by": state["requester"]
        }],
        "status": "pending"
    }

def manager_approval(state: ApprovalState) -> dict:
    return {
        "approvals": [{
            "role": "Manager",
            "action": "approved",
            "by": "John Manager"
        }]
    }

def finance_approval(state: ApprovalState) -> dict:
    return {
        "approvals": [{
            "role": "Finance",
            "action": "approved",
            "by": "Sarah Finance"
        }]
    }

def director_approval(state: ApprovalState) -> dict:
    return {
        "approvals": [{
            "role": "Director",
            "action": "approved",
            "by": "Mike Director"
        }]
    }

def hr_approval(state: ApprovalState) -> dict:
    return {
        "approvals": [{
            "role": "HR",
            "action": "approved",
            "by": "Lisa HR"
        }]
    }

def vp_approval(state: ApprovalState) -> dict:
    return {
        "approvals": [{
            "role": "VP",
            "action": "approved",
            "by": "Tom VP"
        }]
    }

def finalize_request(state: ApprovalState) -> dict:
    return {"status": "approved"}

def build_approval_workflow(request_type: str, amount: float = 0):
    """
    Build approval workflow based on request type and amount.
    
    Chains:
    - "vacation": Employee → Manager → END
    - "expense" (< $100): Employee → Manager → END
    - "expense" (>= $100): Employee → Manager → Finance → END
    - "expense" (>= $1000): Employee → Manager → Finance → Director → END
    - "hiring": HR → Manager → Director → VP → END
    """
    
    graph = StateGraph(ApprovalState)
    
    # Always start with submission
    graph.add_node("submit", employee_submit)
    graph.add_node("finalize", finalize_request)
    
    # Build the approval chain based on type
    if request_type == "vacation":
        # Simple chain: Manager only
        graph.add_node("manager", manager_approval)
        
        graph.add_edge(START, "submit")
        graph.add_edge("submit", "manager")
        graph.add_edge("manager", "finalize")
        graph.add_edge("finalize", END)
    
    elif request_type == "expense":
        graph.add_node("manager", manager_approval)
        
        if amount >= 1000:
            # Full chain: Manager → Finance → Director
            graph.add_node("finance", finance_approval)
            graph.add_node("director", director_approval)
            
            graph.add_edge(START, "submit")
            graph.add_edge("submit", "manager")
            graph.add_edge("manager", "finance")
            graph.add_edge("finance", "director")
            graph.add_edge("director", "finalize")
            graph.add_edge("finalize", END)
        
        elif amount >= 100:
            # Medium chain: Manager → Finance
            graph.add_node("finance", finance_approval)
            
            graph.add_edge(START, "submit")
            graph.add_edge("submit", "manager")
            graph.add_edge("manager", "finance")
            graph.add_edge("finance", "finalize")
            graph.add_edge("finalize", END)
        
        else:
            # Simple chain: Manager only
            graph.add_edge(START, "submit")
            graph.add_edge("submit", "manager")
            graph.add_edge("manager", "finalize")
            graph.add_edge("finalize", END)
    
    elif request_type == "hiring":
        # Full hiring chain: HR → Manager → Director → VP
        graph.add_node("hr", hr_approval)
        graph.add_node("manager", manager_approval)
        graph.add_node("director", director_approval)
        graph.add_node("vp", vp_approval)
        
        graph.add_edge(START, "submit")
        graph.add_edge("submit", "hr")
        graph.add_edge("hr", "manager")
        graph.add_edge("manager", "director")
        graph.add_edge("director", "vp")
        graph.add_edge("vp", "finalize")
        graph.add_edge("finalize", END)
    
    else:
        raise ValueError(f"Unknown request type: {request_type}")
    
    return graph.compile()

def test_approval_workflows():
    test_cases = [
        {
            "name": "Vacation request",
            "request_type": "vacation",
            "amount": 0,
            "description": "2 weeks vacation in August"
        },
        {
            "name": "Small expense ($50)",
            "request_type": "expense",
            "amount": 50,
            "description": "Office supplies"
        },
        {
            "name": "Medium expense ($500)",
            "request_type": "expense",
            "amount": 500,
            "description": "Team lunch"
        },
        {
            "name": "Large expense ($2500)",
            "request_type": "expense",
            "amount": 2500,
            "description": "Conference registration"
        },
        {
            "name": "Hiring request",
            "request_type": "hiring",
            "amount": 0,
            "description": "Senior Developer position"
        }
    ]
    
    for test in test_cases:
        print("\n" + "=" * 60)
        print(f"📋 {test['name']}")
        print(f"   Type: {test['request_type']}, Amount: ${test['amount']}")
        print("=" * 60)
        
        graph = build_approval_workflow(
            test["request_type"],
            test["amount"]
        )
        
        result = graph.invoke({
            "request_type": test["request_type"],
            "amount": test["amount"],
            "requester": "Alice Employee",
            "description": test["description"],
            "approvals": [],
            "status": "new"
        })
        
        print(f"\nFinal Status: {result['status']}")
        print("\nApproval Chain:")
        for i, approval in enumerate(result["approvals"], 1):
            print(f"  {i}. {approval['role']}: {approval['action']} by {approval['by']}")

if __name__ == "__main__":
    test_approval_workflows()
