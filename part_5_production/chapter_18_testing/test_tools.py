# From: AI Agents Book, Chapter 18, Section 18.1
# File: test_tools.py
# Description: Unit tests for agent tools - demonstrates mocking external services

import pytest
from unittest.mock import AsyncMock, Mock, patch
from tools import calculate_shipping, get_customer_info


# Tests for calculate_shipping (deterministic - no mocking needed)

def test_basic_shipping_calculation():
    result = calculate_shipping(weight_kg=2.0, distance_km=100)
    
    assert result["cost"] == 7.00  # 5 + (2 * 0.5) + (100 * 0.01)
    assert result["currency"] == "USD"
    assert result["express"] is False
    assert result["estimated_days"] == 5


def test_express_shipping_multiplier():
    standard = calculate_shipping(weight_kg=2.0, distance_km=100, express=False)
    express = calculate_shipping(weight_kg=2.0, distance_km=100, express=True)
    
    assert express["cost"] == standard["cost"] * 1.5
    assert express["estimated_days"] == 1


def test_zero_weight_and_distance():
    result = calculate_shipping(weight_kg=0, distance_km=0)
    
    assert result["cost"] == 5.00  # Just the base rate


# Tests for get_customer_info (requires mocking the HTTP client)

@pytest.mark.asyncio
async def test_get_customer_info_success():
    mock_response = {
        "id": "cust_123",
        "name": "Alice Smith",
        "email": "alice@example.com",
        "tier": "premium"
    }
    
    with patch("tools.httpx.AsyncClient") as MockClient:
        # Set up the mock to return our fake response
        # Use regular Mock for response since json() is sync in httpx
        mock_response_obj = Mock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status = Mock()

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response_obj
        MockClient.return_value.__aenter__.return_value = mock_client_instance
        
        result = await get_customer_info("cust_123")
        
        assert result["name"] == "Alice Smith"
        assert result["tier"] == "premium"
        
        # Verify the API was called correctly
        mock_client_instance.get.assert_called_once()
        call_args = mock_client_instance.get.call_args
        assert "cust_123" in call_args[0][0]
