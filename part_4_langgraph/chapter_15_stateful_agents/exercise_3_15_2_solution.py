# From: Zero to AI Agent, Chapter 15, Section 15.2
# File: exercise_3_15_2_solution.py

"""
Order processing state with comprehensive validation.
"""

from typing import TypedDict
from pydantic import BaseModel, Field, model_validator
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    name: str = Field(min_length=1)
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)
    
    @property
    def subtotal(self) -> float:
        return self.quantity * self.price

class Order(BaseModel):
    order_id: str
    items: list[OrderItem] = Field(min_length=1)
    total: float = Field(gt=0)
    status: OrderStatus = OrderStatus.PENDING
    
    @model_validator(mode='after')
    def validate_total(self):
        calculated = sum(item.subtotal for item in self.items)
        if abs(self.total - calculated) > 0.01:
            raise ValueError(f'Total {self.total} != calculated {calculated}')
        return self

# TypedDict for LangGraph
class OrderState(TypedDict):
    order: dict
    status_history: list[str]

# Test
print("=== Order Validation ===\n")

# Valid order
valid = Order(
    order_id="ORD-001",
    items=[
        {"name": "Widget", "quantity": 2, "price": 10.00},
        {"name": "Gadget", "quantity": 1, "price": 25.00}
    ],
    total=45.00  # 2*10 + 1*25 = 45 ✓
)
print(f"✓ Valid order: {valid.order_id}, ${valid.total}")

# Invalid: wrong total
try:
    Order(
        order_id="ORD-002",
        items=[{"name": "Item", "quantity": 2, "price": 10.00}],
        total=100.00  # Should be 20!
    )
except Exception as e:
    print(f"✓ Caught bad total: {e}")

# Invalid: zero quantity
try:
    Order(
        order_id="ORD-003",
        items=[{"name": "Item", "quantity": 0, "price": 10.00}],
        total=0
    )
except Exception as e:
    print(f"✓ Caught zero quantity")
