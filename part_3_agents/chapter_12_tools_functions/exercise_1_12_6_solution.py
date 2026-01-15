# From: Zero to AI Agent, Chapter 12, Section 12.6
# File: exercise_1_12_6_solution.py

import time
import re
from typing import Optional

def robust_url_fetcher(url: str) -> str:
    """Fetch webpage content with validation, timeout, and retry."""
    
    # 1. URL Validation
    if not url:
        return "Error: URL cannot be empty"
    
    # Check for valid protocol
    if not url.startswith(('http://', 'https://')):
        return "Error: URL must start with http:// or https://"
    
    # Basic URL pattern check
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:[A-Za-z0-9.-]+)'  # domain
        r'(?::\d+)?'  # optional port
        r'(?:/[^?]*)?'  # path
    )
    
    if not url_pattern.match(url):
        return "Error: Invalid URL format"
    
    # 2. Fetch with timeout and retries
    MAX_RETRIES = 2
    TIMEOUT = 5
    
    for attempt in range(MAX_RETRIES + 1):
        try:
            # Simulate URL fetching with timeout
            # In production, use: requests.get(url, timeout=TIMEOUT)
            
            # Simulate different scenarios
            import random
            if random.random() < 0.3:  # 30% failure rate
                raise TimeoutError("Request timed out")
            
            # Simulate successful fetch
            return f"Successfully fetched content from {url}: [webpage content here]"
            
        except TimeoutError:
            if attempt < MAX_RETRIES:
                print(f"  Attempt {attempt + 1} timed out, retrying...")
                time.sleep(1)  # Wait before retry
            else:
                return f"Error: Could not fetch {url} - connection timed out after {MAX_RETRIES + 1} attempts"
        
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f"  Attempt {attempt + 1} failed, retrying...")
                time.sleep(1)
            else:
                return f"Error: Could not fetch {url} - {str(e)}"
    
    return f"Error: Unable to fetch {url}"

# Test the robust fetcher
print("ROBUST URL FETCHER TEST")
print("=" * 50)

test_urls = [
    "https://example.com",          # Valid
    "http://test.org/page",         # Valid
    "example.com",                  # Missing protocol
    "",                              # Empty
    "not-a-url",                     # Invalid format
    "ftp://file.com",               # Wrong protocol
]

for url in test_urls:
    print(f"\nFetching: '{url}'")
    result = robust_url_fetcher(url)
    print(f"Result: {result}")
