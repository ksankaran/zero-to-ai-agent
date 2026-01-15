# From: Zero to AI Agent, Chapter 17, Section 17.1
# File: exercise_1_17_1_solution.py
# Exercise: Expense Approval System

from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from datetime import datetime
import operator
from dotenv import load_dotenv

load_dotenv()

class ExpenseState(TypedDict):
    expense_id: str
    amount: float
    description: str
    submitter: str
    status: str
    revision_count: int
    max_revisions: int
    approval_log: Annotated[list[str], operator.add]


def submit_expense(state: ExpenseState) -> dict:
    """Initial expense submission."""
    print(f"\n📝 Expense submitted: ${state['amount']:.2f}")
    print(f"   Description: {state['description']}")
    print(f"   Submitter: {state['submitter']}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "status": "submitted",
        "approval_log": [f"[{timestamp}] Expense submitted by {state['submitter']}"]
    }


def check_amount_threshold(state: ExpenseState) -> str:
    """Route based on expense amount."""
    amount = state["amount"]
    if amount < 100:
        return "auto_approve"
    elif amount <= 1000:
        return "manager_review"
    else:
        return "manager_review"  # High amounts also start with manager


def auto_approve(state: ExpenseState) -> dict:
    """Auto-approve expenses under $100."""
    print(f"\n✅ Auto-approved: ${state['amount']:.2f} (under $100 threshold)")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "status": "approved",
        "approval_log": [f"[{timestamp}] Auto-approved (amount under $100)"]
    }


def manager_review(state: ExpenseState) -> dict:
    """Manager reviews the expense using interrupt()."""
    
    print(f"\n👔 Manager review required for ${state['amount']:.2f}")
    
    # Interrupt for manager approval
    decision = interrupt({
        "type": "manager_approval",
        "expense_id": state["expense_id"],
        "amount": state["amount"],
        "description": state["description"],
        "submitter": state["submitter"],
        "message": "Manager: Please review this expense report."
    })
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    approved = decision.get("approved", False)
    notes = decision.get("notes", "")
    approver = decision.get("approver", "Manager")
    
    if approved:
        print(f"✅ Manager approved")
        # Check if finance review is also needed
        if state["amount"] > 1000:
            return {
                "status": "pending_finance",
                "approval_log": [f"[{timestamp}] Manager ({approver}) approved: {notes}"]
            }
        else:
            return {
                "status": "approved",
                "approval_log": [f"[{timestamp}] Manager ({approver}) approved: {notes}"]
            }
    else:
        print(f"❌ Manager rejected")
        return {
            "status": "rejected",
            "approval_log": [f"[{timestamp}] Manager ({approver}) rejected: {notes}"]
        }


def finance_review(state: ExpenseState) -> dict:
    """Finance reviews high-value expenses using interrupt()."""
    
    print(f"\n💰 Finance review required for ${state['amount']:.2f}")
    
    # Interrupt for finance approval
    decision = interrupt({
        "type": "finance_approval",
        "expense_id": state["expense_id"],
        "amount": state["amount"],
        "description": state["description"],
        "submitter": state["submitter"],
        "message": "Finance: This expense exceeds $1000. Please review."
    })
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    approved = decision.get("approved", False)
    notes = decision.get("notes", "")
    approver = decision.get("approver", "Finance")
    
    if approved:
        print(f"✅ Finance approved")
        return {
            "status": "approved",
            "approval_log": [f"[{timestamp}] Finance ({approver}) approved: {notes}"]
        }
    else:
        print(f"❌ Finance rejected")
        return {
            "status": "rejected",
            "approval_log": [f"[{timestamp}] Finance ({approver}) rejected: {notes}"]
        }


def process_expense(state: ExpenseState) -> dict:
    """Process the fully approved expense."""
    print(f"\n🎉 Processing approved expense: ${state['amount']:.2f}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "status": "processed",
        "approval_log": [f"[{timestamp}] Expense processed for payment"]
    }


def handle_rejection(state: ExpenseState) -> dict:
    """Handle rejected expense - offer revision option."""
    
    if state["revision_count"] >= state["max_revisions"]:
        print(f"\n❌ Maximum revisions reached. Expense cancelled.")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        return {
            "status": "cancelled",
            "approval_log": [f"[{timestamp}] Expense cancelled - max revisions exceeded"]
        }
    
    print(f"\n🔄 Expense rejected. Revision {state['revision_count'] + 1}/{state['max_revisions']} available.")
    
    # Interrupt to ask if user wants to revise
    decision = interrupt({
        "type": "revision_option",
        "expense_id": state["expense_id"],
        "current_amount": state["amount"],
        "current_description": state["description"],
        "revisions_remaining": state["max_revisions"] - state["revision_count"],
        "message": "Would you like to revise and resubmit this expense?"
    })
    
    if decision.get("revise", False):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_amount = decision.get("new_amount", state["amount"])
        new_description = decision.get("new_description", state["description"])
        
        return {
            "amount": new_amount,
            "description": new_description,
            "status": "revised",
            "revision_count": state["revision_count"] + 1,
            "approval_log": [f"[{timestamp}] Expense revised: ${new_amount:.2f} - {new_description}"]
        }
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        return {
            "status": "cancelled",
            "approval_log": [f"[{timestamp}] Expense cancelled by submitter"]
        }


def route_after_manager(state: ExpenseState) -> str:
    """Route after manager review."""
    if state["status"] == "approved":
        return "process"
    elif state["status"] == "pending_finance":
        return "finance"
    else:
        return "rejection"


def route_after_finance(state: ExpenseState) -> str:
    """Route after finance review."""
    if state["status"] == "approved":
        return "process"
    else:
        return "rejection"


def route_after_rejection(state: ExpenseState) -> str:
    """Route after rejection handling."""
    if state["status"] == "revised":
        return "submit"  # Go back to start
    else:
        return "end"


def build_expense_workflow():
    """Build the expense approval workflow."""
    workflow = StateGraph(ExpenseState)
    
    # Add nodes
    workflow.add_node("submit", submit_expense)
    workflow.add_node("auto_approve", auto_approve)
    workflow.add_node("manager", manager_review)
    workflow.add_node("finance", finance_review)
    workflow.add_node("process", process_expense)
    workflow.add_node("rejection", handle_rejection)
    
    # Flow
    workflow.add_edge(START, "submit")
    
    # Route by amount after submission
    workflow.add_conditional_edges(
        "submit",
        check_amount_threshold,
        {
            "auto_approve": "auto_approve",
            "manager_review": "manager"
        }
    )
    
    # Auto-approve goes straight to process
    workflow.add_edge("auto_approve", "process")
    
    # Manager review routing
    workflow.add_conditional_edges(
        "manager",
        route_after_manager,
        {
            "process": "process",
            "finance": "finance",
            "rejection": "rejection"
        }
    )
    
    # Finance review routing
    workflow.add_conditional_edges(
        "finance",
        route_after_finance,
        {
            "process": "process",
            "rejection": "rejection"
        }
    )
    
    # Rejection handling routing
    workflow.add_conditional_edges(
        "rejection",
        route_after_rejection,
        {
            "submit": "submit",
            "end": END
        }
    )
    
    # Terminal
    workflow.add_edge("process", END)
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def run_expense_approval():
    """Interactive runner for expense approval."""
    app = build_expense_workflow()
    config = {"configurable": {"thread_id": "expense-001"}}
    
    # Get expense details
    print("\n🧾 New Expense Submission")
    print("=" * 50)
    
    try:
        amount = float(input("Amount: $"))
    except ValueError:
        amount = 150.0
        print(f"Using default amount: ${amount}")
    
    description = input("Description: ") or "Office supplies"
    
    initial_state = {
        "expense_id": f"EXP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "amount": amount,
        "description": description,
        "submitter": "John Smith",
        "status": "new",
        "revision_count": 0,
        "max_revisions": 3,
        "approval_log": []
    }
    
    result = app.invoke(initial_state, config)
    
    # Handle interrupts
    while "__interrupt__" in str(result) or (hasattr(result, 'get') and result.get("__interrupt__")):
        interrupt_data = result.get("__interrupt__", [])
        if not interrupt_data:
            break
            
        payload = interrupt_data[0].value
        
        print("\n" + "=" * 50)
        print(f"📋 {payload.get('type', 'REVIEW').upper().replace('_', ' ')}")
        print("=" * 50)
        print(f"Expense ID: {payload.get('expense_id')}")
        print(f"Amount: ${payload.get('amount', payload.get('current_amount', 0)):.2f}")
        print(f"Description: {payload.get('description', payload.get('current_description', ''))}")
        print(f"\n{payload.get('message', 'Please review')}")
        print("-" * 50)
        
        if payload.get("type") == "revision_option":
            print("\nOptions: [r]evise, [c]ancel")
            choice = input("Your choice: ").strip().lower()
            
            if choice == 'r':
                try:
                    new_amount = float(input(f"New amount (current ${payload['current_amount']:.2f}): $") or payload['current_amount'])
                except ValueError:
                    new_amount = payload['current_amount']
                new_desc = input(f"New description (current: {payload['current_description']}): ") or payload['current_description']
                
                result = app.invoke(
                    Command(resume={"revise": True, "new_amount": new_amount, "new_description": new_desc}),
                    config
                )
            else:
                result = app.invoke(
                    Command(resume={"revise": False}),
                    config
                )
        else:
            # Approval decision
            print("\nOptions: [a]pprove, [r]eject")
            choice = input("Your choice: ").strip().lower()
            notes = input("Notes (optional): ").strip()
            approver = input("Your name: ").strip() or "Reviewer"
            
            result = app.invoke(
                Command(resume={
                    "approved": choice == 'a',
                    "notes": notes,
                    "approver": approver
                }),
                config
            )
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 EXPENSE SUMMARY")
    print("=" * 50)
    print(f"Final Status: {result.get('status', 'unknown').upper()}")
    print(f"Amount: ${result.get('amount', 0):.2f}")
    print(f"Revisions: {result.get('revision_count', 0)}")
    print("\n📜 Approval Log:")
    for entry in result.get("approval_log", []):
        print(f"  {entry}")
    
    return result


if __name__ == "__main__":
    run_expense_approval()
