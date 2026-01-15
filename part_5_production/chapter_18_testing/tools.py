# From: AI Agents Book, Chapter 18, Section 18.1
# File: tools.py
# Description: Agent tool functions - shipping calculator and customer lookup

import httpx


def calculate_shipping(weight_kg: float, distance_km: float, express: bool = False) -> dict:
    """Calculate shipping cost based on weight and distance."""
    base_rate = 5.00
    weight_charge = weight_kg * 0.50
    distance_charge = distance_km * 0.01
    
    subtotal = base_rate + weight_charge + distance_charge
    
    if express:
        subtotal *= 1.5
    
    return {
        "cost": round(subtotal, 2),
        "currency": "USD",
        "express": express,
        "estimated_days": 1 if express else 5
    }


async def get_customer_info(customer_id: str) -> dict:
    """Fetch customer information from the CRM API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.example.com/customers/{customer_id}",
            headers={"Authorization": "Bearer secret-token"}
        )
        response.raise_for_status()
        return response.json()
