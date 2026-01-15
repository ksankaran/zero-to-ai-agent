# From: Zero to AI Agent, Chapter 12, Section 12.6
# File: input_validation.py

from langchain_core.tools import Tool
from datetime import datetime
import re

def search_with_validation(query: str) -> str:
    """
    Search tool with comprehensive input validation.
    """
    # 1. Check if input exists
    if not query:
        return "Error: Search query cannot be empty"
    
    # 2. Check type
    if not isinstance(query, str):
        return "Error: Search query must be text"
    
    # 3. Check length
    if len(query) < 2:
        return "Error: Search query too short (minimum 2 characters)"
    if len(query) > 200:
        return "Error: Search query too long (maximum 200 characters)"
    
    # 4. Clean dangerous characters
    # Remove special characters that might break the search
    cleaned = re.sub(r'[^\w\s\-.]', '', query)
    
    # 5. Check if anything remains
    if not cleaned.strip():
        return "Error: Search query contains only special characters"
    
    # If we get here, input is valid!
    return f"Searching for: '{cleaned}'"

def date_parser_with_validation(date_string: str) -> str:
    """
    Parse dates with validation and multiple format support.
    """
    if not date_string:
        return "Error: Date cannot be empty"
    
    # Try multiple date formats
    formats = [
        "%Y-%m-%d",      # 2024-03-15
        "%m/%d/%Y",      # 03/15/2024
        "%d/%m/%Y",      # 15/03/2024
        "%B %d, %Y",     # March 15, 2024
        "%b %d, %Y",     # Mar 15, 2024
    ]
    
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_string.strip(), fmt)
            # Return in standard format
            return f"Date: {parsed_date.strftime('%Y-%m-%d')}"
        except ValueError:
            continue  # Try next format
    
    # If no format worked
    return f"Error: Could not parse date '{date_string}'. Try formats like: 2024-03-15, 03/15/2024, or March 15, 2024"

# Create validated tools
search_tool = Tool(
    name="ValidatedSearch",
    func=search_with_validation,
    description="Search with input validation"
)

date_tool = Tool(
    name="DateParser",
    func=date_parser_with_validation,
    description="Parse dates in various formats"
)

# Test validation
print("INPUT VALIDATION EXAMPLES")
print("=" * 50)

# Test search validation
search_tests = [
    "Python programming",  # Valid
    "",                    # Empty
    "a",                   # Too short
    "x" * 250,            # Too long
    "'; DROP TABLE;",     # SQL injection attempt
    "!!!***!!!",          # Only special chars
]

print("\nSearch Validation:")
for query in search_tests:
    display = query[:30] + "..." if len(query) > 30 else query
    result = search_tool.func(query)
    status = "✅" if not result.startswith("Error") else "❌"
    print(f"{status} '{display}' → {result}")

# Test date parsing
print("\nDate Parsing:")
date_tests = [
    "2024-03-15",
    "03/15/2024",
    "March 15, 2024",
    "invalid",
    "",
]

for date in date_tests:
    result = date_tool.func(date)
    status = "✅" if not result.startswith("Error") else "❌"
    print(f"{status} '{date}' → {result}")
