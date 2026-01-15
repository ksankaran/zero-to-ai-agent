# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: bulletproof_tool.py

from langchain_core.tools import Tool
import re
from typing import Optional
import time

def bulletproof_search(query: str) -> str:
    """
    A production-ready search tool with all safety features.
    """
    # 1. Input validation
    if not query or not isinstance(query, str):
        return "Error: Please provide a search query"
    
    # 2. Length limits
    if len(query) > 200:
        return "Error: Query too long (max 200 characters)"
    
    # 3. Clean dangerous characters
    query = re.sub(r'[^\w\s\-.]', '', query)
    query = query.strip()
    
    if not query:
        return "Error: Invalid search query"
    
    # 4. Rate limiting (in production, use proper rate limiting)
    time.sleep(0.1)  # Prevent hammering
    
    try:
        # 5. Timeout for external calls
        # In real tool: requests.get(url, timeout=5)
        
        # 6. Simulated search results
        results = f"Search results for '{query}': Found 3 relevant articles..."
        
        # 7. Output sanitization
        return results[:500]  # Limit response size
        
    except Exception as e:
        # 8. Generic error handling
        return "Error: Search temporarily unavailable"

# Create production-ready tool
search_tool = Tool(
    name="WebSearch",
    func=bulletproof_search,
    description="Search the web for information. Input: search query (max 200 chars)"
)

# Test edge cases
print(search_tool.func(""))                    # Error handling
print(search_tool.func("Normal search"))       # Success
print(search_tool.func("x" * 300))            # Length limit
print(search_tool.func("'; DROP TABLE;"))      # SQL injection attempt - cleaned
