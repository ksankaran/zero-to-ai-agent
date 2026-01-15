# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: api_tool_pattern.py

from langchain_core.tools import Tool
import os
from typing import Optional

def create_api_tool(endpoint_name: str):
    """
    Factory function to create API tools.
    This is a pattern - adapt for your specific APIs!
    """
    def api_caller(parameters: str) -> str:
        # Check for API key
        api_key = os.getenv(f"{endpoint_name.upper()}_API_KEY")
        if not api_key:
            return f"Error: {endpoint_name} API key not configured"
        
        try:
            # In real implementation:
            # import requests
            # response = requests.get(
            #     f"https://api.{endpoint_name}.com/v1/query",
            #     params={"q": parameters},
            #     headers={"Authorization": f"Bearer {api_key}"},
            #     timeout=10
            # )
            # return response.json()
            
            # Simulated response
            return f"API response for {parameters} from {endpoint_name}"
            
        except TimeoutError:
            return f"Error: {endpoint_name} API timeout"
        except Exception as e:
            return f"Error: {endpoint_name} API failed"
    
    return Tool(
        name=f"{endpoint_name.title()}API",
        func=api_caller,
        description=f"Query the {endpoint_name} API. Input: query parameters"
    )

# Create tools for different APIs
weather_api = create_api_tool("weather")
news_api = create_api_tool("news")
stock_api = create_api_tool("stocks")

# Each tool follows the same pattern but connects to different services
