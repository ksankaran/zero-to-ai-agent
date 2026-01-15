# From: Zero to AI Agent, Chapter 17, Section 17.1
# File: order_approval.py

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
import operator
from dotenv import load_dotenv

load_dotenv()

class OrderState(TypedDict):
    item: str
    quantity: int
    price: float
    total: float
    order_id: str
    status: str
    rejection_reason: str
    messages: Annotated[list[str], operator.add]  # Audit trail


def calculate_order(state: OrderState) -> dict:
    """Calculate order details."""
    total = state["quantity"] * state["price"]
    
    print(f"\n💰 Order calculated: {state['quantity']}x {state['item']} = ${total:.2f}")
    
    return {
        "total": total,
        "status": "pending_approval",
        "messages": [f"Order {state['order_id']} created: ${total:.2f}"]
    }


def request_approval(state: OrderState) -> dict:
    """Request human approval for the order."""
    
    print(f"\n⏸️  Requesting approval for order {state['order_id']}...")
    
    # Interrupt with full order details
    decision = interrupt({
        "type": "order_approval",
        "order_id": state["order_id"],
        "item": state["item"],
        "quantity": state["quantity"],
        "unit_price": state["price"],
        "total": state["total"],
        "options": ["approve", "reject", "modify"]
    })
    
    # Process the decision
    action = decision.get("action", "reject")
    
    if action == "approve":
        return {
            "status": "approved",
            "messages": [f"Order approved by {decision.get('approver', 'unknown')}"]
        }
    elif action == "modify":
        # Human wants to change the quantity
        new_qty = decision.get("new_quantity", state["quantity"])
        return {
            "quantity": new_qty,
            "status": "modified",
            "messages": [f"Order modified: quantity changed to {new_qty}"]
        }
    else:
        return {
            "status": "rejected",
            "rejection_reason": decision.get("reason", "No reason provided"),
            "messages": [f"Order rejected: {decision.get('reason', 'No reason')}"]
        }


def process_order(state: OrderState) -> dict:
    """Process the approved order."""
    print(f"\n✅ Processing order {state['order_id']}...")
    return {
        "status": "processed",
        "messages": ["Order processed and sent to fulfillment"]
    }

def cancel_order(state: OrderState) -> dict:
    """Cancel the rejected order."""
    print(f"\n❌ Cancelling order {state['order_id']}: {state['rejection_reason']}")
    return {
        "status": "cancelled",
        "messages": [f"Order cancelled: {state['rejection_reason']}"]
    }

def recalculate_order(state: OrderState) -> dict:
    """Recalculate after modification."""
    new_total = state["quantity"] * state["price"]
    print(f"\n🔄 Recalculating: {state['quantity']}x {state['item']} = ${new_total:.2f}")
    return {
        "total": new_total,
        "status": "pending_approval",
        "messages": [f"Order recalculated: ${new_total:.2f}"]
    }


def route_after_approval(state: OrderState) -> str:
    """Route based on approval decision."""
    status = state["status"]
    if status == "approved":
        return "process"
    elif status == "modified":
        return "recalculate"
    elif status == "rejected":
        return "cancel"
    else:
        return "approve"  # Stay in approval

def build_order_workflow():
    workflow = StateGraph(OrderState)
    
    workflow.add_node("calculate", calculate_order)
    workflow.add_node("approve", request_approval)
    workflow.add_node("process", process_order)
    workflow.add_node("cancel", cancel_order)
    workflow.add_node("recalculate", recalculate_order)
    
    workflow.add_edge(START, "calculate")
    workflow.add_edge("calculate", "approve")
    
    workflow.add_conditional_edges(
        "approve",
        route_after_approval,
        {
            "process": "process",
            "cancel": "cancel",
            "recalculate": "recalculate",
            "approve": "approve"
        }
    )
    
    # After recalculation, go back for approval
    workflow.add_edge("recalculate", "approve")
    
    workflow.add_edge("process", END)
    workflow.add_edge("cancel", END)
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


if __name__ == "__main__":
    app = build_order_workflow()
    config = {"configurable": {"thread_id": "order-001"}}
    
    initial_state = {
        "item": "Laptop",
        "quantity": 5,
        "price": 999.99,
        "total": 0.0,
        "order_id": "ORD-001",
        "status": "new",
        "rejection_reason": "",
        "messages": []
    }
    
    result = app.invoke(initial_state, config)
    print(f"Final status: {result.get('status')}")
