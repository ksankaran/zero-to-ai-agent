# From: Zero to AI Agent, Chapter 12, Section 12.3
# File: exploring_duckduckgo.py

from langchain_community.tools import DuckDuckGoSearchRun

# Initialize the search tool - that's it!
search_tool = DuckDuckGoSearchRun()

# Test it directly - just like calling a function!
print("Testing DuckDuckGo Search Tool")
print("=" * 50)

# Search for something current
result = search_tool.run("Python programming language latest version 2024")
print("Search for Python version:")
print(result[:300] + "...")  # First 300 chars
print()

# Search for news
news_result = search_tool.run("artificial intelligence breakthrough today")
print("Search for AI news:")
print(news_result[:300] + "...")
print()

# Search for factual information
fact_result = search_tool.run("height of Mount Everest in meters")
print("Search for facts:")
print(fact_result[:300] + "...")
