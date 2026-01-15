# From: Zero to AI Agent, Chapter 9, Section 9.5
# File: exercise_2_9_5_solution.py

"""
Build comprehensive test suite for API documentation prompt
"""

base_prompt = """You are a technical documentation writer. 
Convert this API response into user-friendly documentation."""

# Normal Test Cases
normal_tests = [
    {
        "name": "Simple Success Response",
        "input": '{"status": 200, "data": {"user_id": 123, "name": "John"}}',
        "expected": "Clear explanation of successful user retrieval"
    },
    {
        "name": "Error Response", 
        "input": '{"status": 404, "error": "User not found"}',
        "expected": "User-friendly error explanation with next steps"
    },
    {
        "name": "Complex Nested Data",
        "input": '{"status": 200, "data": {"user": {"profile": {"settings": {"theme": "dark"}}}}}',
        "expected": "Simplified explanation of nested structure"
    },
    {
        "name": "Array Response",
        "input": '{"status": 200, "data": [{"id": 1}, {"id": 2}, {"id": 3}]}',
        "expected": "Clear explanation of list data"
    },
    {
        "name": "Empty Response",
        "input": '{"status": 204, "data": null}',
        "expected": "Explanation of successful action with no return data"
    }
]

# Edge Cases
edge_cases = [
    {
        "name": "Malformed JSON",
        "input": '{"status": 200, "data": "incomplete...',
        "expected": "Graceful handling of invalid input"
    },
    {
        "name": "Extremely Long Response",
        "input": '{"data": ' + '{"field": "value", ' * 100 + '}}',
        "expected": "Summarized documentation, not overwhelming"
    },
    {
        "name": "Binary/Encoded Data",
        "input": '{"status": 200, "data": "base64:SGVsbG8gV29ybGQ="}',
        "expected": "Explanation that data is encoded"
    }
]

# Adversarial Cases
adversarial_cases = [
    {
        "name": "Injection Attempt",
        "input": '{"status": 200, "data": "\'; DROP TABLE users; --"}',
        "expected": "Safe handling, no execution of malicious content"
    },
    {
        "name": "Contradictory Data",
        "input": '{"status": 200, "error": "Success", "data": null}',
        "expected": "Handles contradiction intelligently"
    }
]

# Scoring Rubric
scoring_rubric = {
    "accuracy": {
        "weight": 0.3,
        "criteria": "Correctly interprets API response meaning"
    },
    "clarity": {
        "weight": 0.25,
        "criteria": "Easy for non-technical users to understand"
    },
    "completeness": {
        "weight": 0.2,
        "criteria": "Addresses all important information"
    },
    "formatting": {
        "weight": 0.15,
        "criteria": "Well-structured and readable output"
    },
    "error_handling": {
        "weight": 0.1,
        "criteria": "Gracefully handles edge cases"
    }
}

# Success Criteria
success_criteria = """
MUST HAVE (Minimum for production):
✓ Accurate interpretation: 95%+ correct
✓ No technical jargon in output
✓ Handles all normal cases properly
✓ Graceful error handling
✓ Consistent formatting

NICE TO HAVE (Excellence targets):
✓ Helpful next steps for errors
✓ Examples where appropriate
✓ Links to more resources
✓ Detects and explains patterns
"""

def calculate_score(test_result, rubric):
    """Calculate weighted score based on rubric"""
    total = 0
    for category, details in rubric.items():
        # In real implementation, get actual scores
        score = 8  # Placeholder
        total += score * details['weight']
    return total

if __name__ == "__main__":
    print("API DOCUMENTATION TEST SUITE")
    print("="*50)
    print(f"Normal Cases: {len(normal_tests)}")
    print(f"Edge Cases: {len(edge_cases)}")
    print(f"Adversarial Cases: {len(adversarial_cases)}")
    print(f"Total Test Cases: {len(normal_tests) + len(edge_cases) + len(adversarial_cases)}")
    print("\nScoring Categories:")
    for category, details in scoring_rubric.items():
        print(f"  {category}: {details['weight']*100:.0f}% - {details['criteria']}")
    print("\n" + success_criteria)