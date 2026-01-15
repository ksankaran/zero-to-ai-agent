# From: Zero to AI Agent, Chapter 11, Section 11.6
# File: validation.py

from pydantic import BaseModel, Field, validator
from langchain_core.output_parsers import PydanticOutputParser

class Order(BaseModel):
    quantity: int = Field(description="number of items")
    price_each: float = Field(description="price per item")
    discount_percent: int = Field(description="discount percentage (0-100)")
    
    @validator('quantity')
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v
    
    @validator('discount_percent')
    def discount_valid(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Discount must be 0-100')
        return v
    
    def calculate_total(self):
        subtotal = self.quantity * self.price_each
        discount = subtotal * (self.discount_percent / 100)
        return subtotal - discount

# Parser will enforce these rules!
parser = PydanticOutputParser(pydantic_object=Order)

# If LLM returns invalid data, you'll know immediately
print("Parser ready with validation rules")
