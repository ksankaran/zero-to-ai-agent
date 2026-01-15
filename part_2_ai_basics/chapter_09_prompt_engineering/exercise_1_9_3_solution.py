# From: Zero to AI Agent, Chapter 9, Section 9.3
# File: exercise_1_9_3_solution.py

"""
Teach format conversions through examples only - no rule explanations
"""

# Task 1: Date Format Conversion
date_conversion_prompt = """
Convert dates to ISO format:

January 15, 2024 → 2024-01-15
December 3, 2023 → 2023-12-03

March 28, 2024 →"""

# Task 2: Phone Number Formatting
phone_formatting_prompt = """
Format phone numbers:

555-123-4567 → (555) 123-4567
15551234567 → (555) 123-4567

555.123.4567 →"""

# Task 3: Citation Style Conversion
citation_conversion_prompt = """
Convert citations from MLA to APA:

MLA: Smith, John. "The Future of AI." Technology Today, vol. 45, no. 3, 2024, pp. 23-45.
APA: Smith, J. (2024). The future of AI. Technology Today, 45(3), 23-45.

MLA: Johnson, Sarah and Mike Davis. Learning Python. TechPress, 2023.
APA: Johnson, S., & Davis, M. (2023). Learning python. TechPress.

MLA: Lee, Amy. "Understanding Algorithms." Computer Science Quarterly, vol. 12, no. 1, 2024, pp. 67-89.
APA:"""

def test_formats():
    """Test each format with unusual inputs"""
    
    test_cases = {
        "Date": {
            "prompt": date_conversion_prompt,
            "test": "September 7, 2024",
            "expected": "2024-09-07"
        },
        "Phone": {
            "prompt": phone_formatting_prompt,
            "test": "555 123 4567",
            "expected": "(555) 123-4567"
        },
        "Citation": {
            "prompt": citation_conversion_prompt,
            "test": 'Brown, Chris. "Machine Learning Basics." AI Monthly, vol. 8, no. 2, 2024, pp. 12-28.',
            "expected": "Brown, C. (2024). Machine learning basics. AI Monthly, 8(2), 12-28."
        }
    }
    
    for format_type, test in test_cases.items():
        print(f"\n{'='*50}")
        print(f"Format Type: {format_type}")
        print(f"{'='*50}")
        print("Few-shot examples provided:")
        print(test["prompt"])
        print(f"\nTest input: {test['test']}")
        print(f"Expected pattern: {test['expected']}")
        print("\nThe AI learns the pattern from just 2 examples!")

if __name__ == "__main__":
    test_formats()