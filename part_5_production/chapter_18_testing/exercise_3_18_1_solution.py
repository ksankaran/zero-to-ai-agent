# From: AI Agents Book, Chapter 18, Section 18.1
# File: exercise_3_18_1_solution.py
# Description: Exercise 3 Solution - Weather API tool with async mocking tests

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx


# The weather tool function
async def get_weather(city: str) -> dict:
    """Fetch current weather for a city from the weather API."""
    if not city or not city.strip():
        return {"error": "City name is required", "temperature": None}
    
    city = city.strip()
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"https://api.weather.example.com/current",
                params={"city": city}
            )
            
            if response.status_code == 404:
                return {"error": f"City '{city}' not found", "temperature": None}
            
            response.raise_for_status()
            data = response.json()
            
            return {
                "city": data["location"]["name"],
                "temperature": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "error": None
            }
    
    except httpx.TimeoutException:
        return {"error": "Request timed out", "temperature": None}
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.status_code}", "temperature": None}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "temperature": None}


# Tests
class TestGetWeather:
    
    @pytest.mark.asyncio
    async def test_successful_response(self):
        """Test correct parsing of successful API response."""
        mock_api_response = {
            "location": {"name": "London"},
            "current": {
                "temp_c": 15.5,
                "condition": {"text": "Partly cloudy"}
            }
        }
        
        with patch("httpx.AsyncClient") as MockClient:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status = MagicMock()
            mock_client.get.return_value = mock_response
            MockClient.return_value.__aenter__.return_value = mock_client
            
            result = await get_weather("London")
            
            assert result["city"] == "London"
            assert result["temperature"] == 15.5
            assert result["condition"] == "Partly cloudy"
            assert result["error"] is None
    
    @pytest.mark.asyncio
    async def test_city_not_found_404(self):
        """Test handling of 404 response."""
        with patch("httpx.AsyncClient") as MockClient:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_client.get.return_value = mock_response
            MockClient.return_value.__aenter__.return_value = mock_client
            
            result = await get_weather("Nonexistentville")
            
            assert result["temperature"] is None
            assert "not found" in result["error"]
            assert "Nonexistentville" in result["error"]
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test handling of network timeout."""
        with patch("httpx.AsyncClient") as MockClient:
            mock_client = AsyncMock()
            mock_client.get.side_effect = httpx.TimeoutException("Connection timed out")
            MockClient.return_value.__aenter__.return_value = mock_client
            
            result = await get_weather("Tokyo")
            
            assert result["temperature"] is None
            assert "timed out" in result["error"].lower()
    
    @pytest.mark.asyncio
    async def test_correct_city_passed_to_api(self):
        """Test that the city name is correctly passed to the API."""
        mock_api_response = {
            "location": {"name": "Paris"},
            "current": {"temp_c": 20.0, "condition": {"text": "Sunny"}}
        }
        
        with patch("httpx.AsyncClient") as MockClient:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status = MagicMock()
            mock_client.get.return_value = mock_response
            MockClient.return_value.__aenter__.return_value = mock_client
            
            await get_weather("Paris")
            
            # Verify the API was called with correct parameters
            mock_client.get.assert_called_once()
            call_kwargs = mock_client.get.call_args
            assert call_kwargs.kwargs["params"]["city"] == "Paris"
    
    @pytest.mark.asyncio
    async def test_empty_city_name(self):
        """Test handling of empty city name."""
        result = await get_weather("")
        
        assert result["temperature"] is None
        assert "required" in result["error"].lower()
    
    @pytest.mark.asyncio
    async def test_whitespace_city_name_trimmed(self):
        """Test that whitespace is trimmed from city name."""
        mock_api_response = {
            "location": {"name": "Berlin"},
            "current": {"temp_c": 18.0, "condition": {"text": "Clear"}}
        }
        
        with patch("httpx.AsyncClient") as MockClient:
            mock_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status = MagicMock()
            mock_client.get.return_value = mock_response
            MockClient.return_value.__aenter__.return_value = mock_client
            
            await get_weather("  Berlin  ")
            
            call_kwargs = mock_client.get.call_args
            assert call_kwargs.kwargs["params"]["city"] == "Berlin"
