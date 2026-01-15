# From: AI Agents Book - Chapter 13, Section 13.7
# File: pii_filter.py

import re


class PIIFilter:
    """Filter personally identifiable information from messages."""
    
    def __init__(self):
        # Patterns for common PII
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        }
    
    def filter_message(self, text: str) -> str:
        """Replace PII with placeholders."""
        filtered = text
        
        # Replace email addresses
        filtered = re.sub(self.patterns['email'], '[EMAIL]', filtered)
        
        # Replace phone numbers
        filtered = re.sub(self.patterns['phone'], '[PHONE]', filtered)
        
        # Replace SSNs
        filtered = re.sub(self.patterns['ssn'], '[SSN]', filtered)
        
        # Replace credit cards
        filtered = re.sub(self.patterns['credit_card'], '[CARD]', filtered)
        
        return filtered
    
    def contains_pii(self, text: str) -> bool:
        """Check if text contains any PII."""
        for pattern in self.patterns.values():
            if re.search(pattern, text):
                return True
        return False


def safe_add_message(memory, user_input, pii_filter):
    """Add message to memory after filtering PII."""
    if pii_filter.contains_pii(user_input):
        print("Warning: PII detected and filtered")
        user_input = pii_filter.filter_message(user_input)
    
    # Now safe to store
    memory.add_message(user_input)


# Usage
if __name__ == "__main__":
    filter = PIIFilter()
    
    test_message = "My email is john@example.com and phone is 555-123-4567"
    filtered = filter.filter_message(test_message)
    print(f"Original: {test_message}")
    print(f"Filtered: {filtered}")
    # Output: "My email is [EMAIL] and phone is [PHONE]"
    
    # Test detection
    print(f"Contains PII: {filter.contains_pii(test_message)}")
    print(f"Contains PII after filter: {filter.contains_pii(filtered)}")
