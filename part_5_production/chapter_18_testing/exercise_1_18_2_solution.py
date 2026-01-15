# From: AI Agents Book, Chapter 18, Section 18.2
# File: exercise_1_18_2_solution.py
# Description: Exercise 1 Solution - Order processing workflow with integration tests

import pytest
from unittest.mock import MagicMock
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END


# State definition
class OrderState(TypedDict):
    order_id: str
    items: list[dict]
    subtotal: float | None
    tax: float | None
    total: float | None
    is_valid: bool | None
    error: str | None
    confirmation_message: str | None


# Node functions
def validate_order(state: OrderState) -> dict:
    """Validate order data."""
    errors = []
    
    if not state.get("order_id"):
        errors.append("Order ID is required")
    
    if not state.get("items") or len(state["items"]) == 0:
        errors.append("Order must have at least one item")
    
    for item in state.get("items", []):
        if item.get("quantity", 0) <= 0:
            errors.append(f"Invalid quantity for {item.get('name', 'unknown item')}")
        if item.get("price", 0) <= 0:
            errors.append(f"Invalid price for {item.get('name', 'unknown item')}")
    
    if errors:
        return {"is_valid": False, "error": "; ".join(errors)}
    
    return {"is_valid": True, "error": None}


def calculate_total(state: OrderState) -> dict:
    """Calculate order total with tax."""
    subtotal = sum(
        item["price"] * item["quantity"] 
        for item in state["items"]
    )
    tax_rate = 0.08  # 8% tax
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)
    
    return {
        "subtotal": subtotal,
        "tax": tax,
        "total": total
    }


def confirm_order(state: OrderState) -> dict:
    """Generate order confirmation."""
    message = (
        f"Order {state['order_id']} confirmed! "
        f"Total: ${state['total']:.2f} (includes ${state['tax']:.2f} tax)"
    )
    return {"confirmation_message": message}


def route_after_validation(state: OrderState) -> str:
    """Route based on validation result."""
    if state.get("is_valid"):
        return "calculate_total"
    else:
        return END


def build_order_graph():
    """Build the order processing graph."""
    graph = StateGraph(OrderState)
    
    graph.add_node("validate_order", validate_order)
    graph.add_node("calculate_total", calculate_total)
    graph.add_node("confirm_order", confirm_order)
    
    graph.add_edge(START, "validate_order")
    graph.add_conditional_edges("validate_order", route_after_validation)
    graph.add_edge("calculate_total", "confirm_order")
    graph.add_edge("confirm_order", END)
    
    return graph.compile()


# Integration tests
class TestOrderProcessingWorkflow:
    """Integration tests for the complete order processing workflow."""
    
    @pytest.fixture
    def graph(self):
        return build_order_graph()
    
    def test_valid_order_flows_through_all_nodes(self, graph):
        """Test that valid orders complete the full workflow."""
        initial_state = {
            "order_id": "ORD-001",
            "items": [
                {"name": "Widget", "price": 10.00, "quantity": 2},
                {"name": "Gadget", "price": 25.00, "quantity": 1}
            ],
            "subtotal": None,
            "tax": None,
            "total": None,
            "is_valid": None,
            "error": None,
            "confirmation_message": None
        }
        
        result = graph.invoke(initial_state)
        
        # Verify validation passed
        assert result["is_valid"] is True
        assert result["error"] is None
        
        # Verify calculation happened
        assert result["subtotal"] == 45.00  # (10*2) + (25*1)
        assert result["tax"] == 3.60  # 45 * 0.08
        assert result["total"] == 48.60
        
        # Verify confirmation generated
        assert result["confirmation_message"] is not None
        assert "ORD-001" in result["confirmation_message"]
        assert "48.60" in result["confirmation_message"]
    
    def test_invalid_order_stops_at_validation(self, graph):
        """Test that invalid orders don't proceed to calculation."""
        initial_state = {
            "order_id": "ORD-002",
            "items": [],  # Empty items - invalid!
            "subtotal": None,
            "tax": None,
            "total": None,
            "is_valid": None,
            "error": None,
            "confirmation_message": None
        }
        
        result = graph.invoke(initial_state)
        
        # Validation should fail
        assert result["is_valid"] is False
        assert result["error"] is not None
        assert "at least one item" in result["error"]
        
        # Calculation should NOT have happened
        assert result["subtotal"] is None
        assert result["total"] is None
        
        # Confirmation should NOT have happened
        assert result["confirmation_message"] is None
    
    def test_state_accumulates_through_workflow(self, graph):
        """Test that state is correctly accumulated at each step."""
        initial_state = {
            "order_id": "ORD-003",
            "items": [{"name": "Test Item", "price": 100.00, "quantity": 1}],
            "subtotal": None,
            "tax": None,
            "total": None,
            "is_valid": None,
            "error": None,
            "confirmation_message": None
        }
        
        result = graph.invoke(initial_state)
        
        # Original data should be preserved
        assert result["order_id"] == "ORD-003"
        assert result["items"] == initial_state["items"]
        
        # Each stage should have added its data
        assert result["is_valid"] is not None  # From validate_order
        assert result["subtotal"] is not None  # From calculate_total
        assert result["confirmation_message"] is not None  # From confirm_order
    
    def test_missing_order_id_fails_validation(self, graph):
        """Test validation catches missing order ID."""
        initial_state = {
            "order_id": "",  # Empty order ID
            "items": [{"name": "Item", "price": 10.00, "quantity": 1}],
            "subtotal": None,
            "tax": None,
            "total": None,
            "is_valid": None,
            "error": None,
            "confirmation_message": None
        }
        
        result = graph.invoke(initial_state)
        
        assert result["is_valid"] is False
        assert "Order ID" in result["error"]
    
    def test_invalid_item_quantity_fails_validation(self, graph):
        """Test validation catches invalid quantities."""
        initial_state = {
            "order_id": "ORD-004",
            "items": [{"name": "Item", "price": 10.00, "quantity": -1}],
            "subtotal": None,
            "tax": None,
            "total": None,
            "is_valid": None,
            "error": None,
            "confirmation_message": None
        }
        
        result = graph.invoke(initial_state)
        
        assert result["is_valid"] is False
        assert "Invalid quantity" in result["error"]
