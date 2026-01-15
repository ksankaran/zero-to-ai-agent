# From: AI Agents Book, Chapter 18, Section 18.3
# File: simple_evaluators.py
# Description: Basic evaluation functions for exact match and keyword checking


def evaluate_exact_match(response: str, expected: str) -> dict:
    """Check if response exactly matches expected output."""
    match = response.strip().lower() == expected.strip().lower()
    return {
        "metric": "exact_match",
        "score": 1.0 if match else 0.0,
        "passed": match
    }


def evaluate_contains_keywords(response: str, required_keywords: list[str]) -> dict:
    """Check if response contains all required keywords."""
    response_lower = response.lower()
    found = [kw for kw in required_keywords if kw.lower() in response_lower]
    missing = [kw for kw in required_keywords if kw.lower() not in response_lower]
    
    score = len(found) / len(required_keywords) if required_keywords else 1.0
    
    return {
        "metric": "keyword_coverage",
        "score": score,
        "found": found,
        "missing": missing,
        "passed": len(missing) == 0
    }


# Example usage
if __name__ == "__main__":
    # Test exact match
    result = evaluate_exact_match("Paris", "paris")
    print(f"Exact match: {result}")
    
    # Test keyword coverage
    response = "The capital of France is Paris, a beautiful city."
    result = evaluate_contains_keywords(response, ["Paris", "capital", "France"])
    print(f"Keyword coverage: {result}")
