# From: Zero to AI Agent, Chapter 17, Section 17.5
# Save as: conditional_assembly.py

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

class OrderState(TypedDict):
    order_type: str  # "standard", "express", "international"
    items: list[str]
    requires_approval: bool
    total_amount: float
    status: str
    audit_log: list[str]

def validate_order(state: OrderState) -> dict:
    return {"status": "validated", "audit_log": ["Order validated"]}

def check_inventory(state: OrderState) -> dict:
    return {"audit_log": ["Inventory checked - all items available"]}

def calculate_shipping(state: OrderState) -> dict:
    return {"audit_log": ["Shipping calculated"]}

def apply_express_handling(state: OrderState) -> dict:
    return {"audit_log": ["Express handling applied - priority queue"]}

def customs_declaration(state: OrderState) -> dict:
    return {"audit_log": ["Customs declaration prepared"]}

def manager_approval(state: OrderState) -> dict:
    return {"audit_log": ["Manager approval obtained"]}

def process_payment(state: OrderState) -> dict:
    return {"status": "paid", "audit_log": ["Payment processed"]}

def finalize_order(state: OrderState) -> dict:
    return {"status": "complete", "audit_log": ["Order finalized"]}

def build_order_graph(
    order_type: str,
    requires_approval: bool,
    amount: float
):
    """Build order processing graph based on conditions."""
    
    graph = StateGraph(OrderState)
    
    # Always include these
    graph.add_node("validate", validate_order)
    graph.add_node("inventory", check_inventory)
    graph.add_node("shipping", calculate_shipping)
    graph.add_node("payment", process_payment)
    graph.add_node("finalize", finalize_order)
    
    # Conditional nodes
    if order_type == "express":
        graph.add_node("express", apply_express_handling)
    
    if order_type == "international":
        graph.add_node("customs", customs_declaration)
    
    if requires_approval or amount > 1000:
        graph.add_node("approval", manager_approval)
    
    # Build edges based on what nodes exist
    graph.add_edge(START, "validate")
    graph.add_edge("validate", "inventory")
    
    # After inventory, handle express
    if order_type == "express":
        graph.add_edge("inventory", "express")
        next_after_inventory = "express"
    else:
        next_after_inventory = "shipping"
        graph.add_edge("inventory", "shipping")
    
    # Connect express to shipping if it exists
    if order_type == "express":
        graph.add_edge("express", "shipping")
    
    # After shipping, handle customs for international
    if order_type == "international":
        graph.add_edge("shipping", "customs")
        pre_payment = "customs"
    else:
        pre_payment = "shipping"
    
    # Handle approval if needed
    if requires_approval or amount > 1000:
        graph.add_edge(pre_payment, "approval")
        graph.add_edge("approval", "payment")
    else:
        graph.add_edge(pre_payment, "payment")
    
    graph.add_edge("payment", "finalize")
    graph.add_edge("finalize", END)
    
    return graph.compile()

def test_conditional_assembly():
    scenarios = [
        {
            "name": "Standard small order",
            "order_type": "standard",
            "requires_approval": False,
            "amount": 50.0
        },
        {
            "name": "Express order",
            "order_type": "express", 
            "requires_approval": False,
            "amount": 200.0
        },
        {
            "name": "International high-value",
            "order_type": "international",
            "requires_approval": False,
            "amount": 2500.0
        },
        {
            "name": "Standard with approval",
            "order_type": "standard",
            "requires_approval": True,
            "amount": 100.0
        }
    ]
    
    for scenario in scenarios:
        print("\n" + "=" * 60)
        print(f"📦 Scenario: {scenario['name']}")
        print("=" * 60)
        
        graph = build_order_graph(
            scenario["order_type"],
            scenario["requires_approval"],
            scenario["amount"]
        )
        
        result = graph.invoke({
            "order_type": scenario["order_type"],
            "items": ["Widget A", "Gadget B"],
            "requires_approval": scenario["requires_approval"],
            "total_amount": scenario["amount"],
            "status": "new",
            "audit_log": []
        })
        
        print(f"Status: {result['status']}")
        print("Audit trail:")
        for log in result["audit_log"]:
            print(f"  ✓ {log}")

if __name__ == "__main__":
    test_conditional_assembly()
