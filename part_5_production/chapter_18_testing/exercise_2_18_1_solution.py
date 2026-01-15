# From: AI Agents Book, Chapter 18, Section 18.1
# File: exercise_2_18_1_solution.py
# Description: Exercise 2 Solution - Shopping cart state helpers with tests

import pytest
from typing import TypedDict


# State definitions
class CartItem(TypedDict):
    name: str
    quantity: int
    price: float


class CartState(TypedDict):
    items: list[CartItem]
    total: float
    coupon_code: str | None


# Helper functions
def add_item(state: CartState, name: str, quantity: int, price: float) -> dict:
    """Add an item to the cart. Returns state update."""
    # Check if item already exists
    for item in state["items"]:
        if item["name"] == name:
            # Update quantity of existing item
            new_items = []
            for i in state["items"]:
                if i["name"] == name:
                    new_items.append({
                        "name": name,
                        "quantity": i["quantity"] + quantity,
                        "price": price
                    })
                else:
                    new_items.append(i)
            return {"items": new_items}
    
    # Add new item
    new_items = state["items"] + [{"name": name, "quantity": quantity, "price": price}]
    return {"items": new_items}


def remove_item(state: CartState, name: str) -> dict:
    """Remove an item from the cart. Returns state update."""
    new_items = [item for item in state["items"] if item["name"] != name]
    
    if len(new_items) == len(state["items"]):
        # Item wasn't found - return unchanged
        return {"items": state["items"]}
    
    return {"items": new_items}


def apply_coupon(state: CartState, code: str, valid_coupons: dict[str, float]) -> dict:
    """Apply a coupon code. Returns state update with discount info."""
    if code not in valid_coupons:
        return {"coupon_code": None, "coupon_error": "Invalid coupon code"}
    
    return {"coupon_code": code, "coupon_error": None}


def calculate_total(state: CartState, valid_coupons: dict[str, float] = None) -> dict:
    """Calculate cart total. Returns state update."""
    valid_coupons = valid_coupons or {}
    
    subtotal = sum(item["price"] * item["quantity"] for item in state["items"])
    
    discount = 0.0
    if state.get("coupon_code") and state["coupon_code"] in valid_coupons:
        discount = subtotal * valid_coupons[state["coupon_code"]]
    
    total = subtotal - discount
    return {"total": round(total, 2)}


# Tests
class TestAddItem:
    def test_add_new_item(self):
        state = {"items": [], "total": 0, "coupon_code": None}
        
        result = add_item(state, "Widget", 2, 9.99)
        
        assert len(result["items"]) == 1
        assert result["items"][0]["name"] == "Widget"
        assert result["items"][0]["quantity"] == 2
        assert result["items"][0]["price"] == 9.99
    
    def test_add_item_increases_quantity_if_exists(self):
        state = {
            "items": [{"name": "Widget", "quantity": 2, "price": 9.99}],
            "total": 0,
            "coupon_code": None
        }
        
        result = add_item(state, "Widget", 3, 9.99)
        
        assert len(result["items"]) == 1
        assert result["items"][0]["quantity"] == 5
    
    def test_add_different_items(self):
        state = {
            "items": [{"name": "Widget", "quantity": 2, "price": 9.99}],
            "total": 0,
            "coupon_code": None
        }
        
        result = add_item(state, "Gadget", 1, 19.99)
        
        assert len(result["items"]) == 2


class TestRemoveItem:
    def test_remove_existing_item(self):
        state = {
            "items": [
                {"name": "Widget", "quantity": 2, "price": 9.99},
                {"name": "Gadget", "quantity": 1, "price": 19.99}
            ],
            "total": 0,
            "coupon_code": None
        }
        
        result = remove_item(state, "Widget")
        
        assert len(result["items"]) == 1
        assert result["items"][0]["name"] == "Gadget"
    
    def test_remove_nonexistent_item_returns_unchanged(self):
        state = {
            "items": [{"name": "Widget", "quantity": 2, "price": 9.99}],
            "total": 0,
            "coupon_code": None
        }
        
        result = remove_item(state, "Nonexistent")
        
        assert len(result["items"]) == 1
        assert result["items"][0]["name"] == "Widget"
    
    def test_remove_from_empty_cart(self):
        state = {"items": [], "total": 0, "coupon_code": None}
        
        result = remove_item(state, "Widget")
        
        assert result["items"] == []


class TestApplyCoupon:
    def test_apply_valid_coupon(self):
        state = {"items": [], "total": 0, "coupon_code": None}
        valid_coupons = {"SAVE10": 0.10, "SAVE20": 0.20}
        
        result = apply_coupon(state, "SAVE10", valid_coupons)
        
        assert result["coupon_code"] == "SAVE10"
        assert result.get("coupon_error") is None
    
    def test_apply_invalid_coupon(self):
        state = {"items": [], "total": 0, "coupon_code": None}
        valid_coupons = {"SAVE10": 0.10}
        
        result = apply_coupon(state, "INVALID", valid_coupons)
        
        assert result["coupon_code"] is None
        assert "Invalid" in result["coupon_error"]


class TestCalculateTotal:
    def test_calculate_total_no_discount(self):
        state = {
            "items": [
                {"name": "Widget", "quantity": 2, "price": 10.00},
                {"name": "Gadget", "quantity": 1, "price": 20.00}
            ],
            "total": 0,
            "coupon_code": None
        }
        
        result = calculate_total(state)
        
        assert result["total"] == 40.00
    
    def test_calculate_total_with_discount(self):
        state = {
            "items": [{"name": "Widget", "quantity": 1, "price": 100.00}],
            "total": 0,
            "coupon_code": "SAVE10"
        }
        valid_coupons = {"SAVE10": 0.10}
        
        result = calculate_total(state, valid_coupons)
        
        assert result["total"] == 90.00
    
    def test_calculate_total_empty_cart(self):
        state = {"items": [], "total": 0, "coupon_code": None}
        
        result = calculate_total(state)
        
        assert result["total"] == 0.00
