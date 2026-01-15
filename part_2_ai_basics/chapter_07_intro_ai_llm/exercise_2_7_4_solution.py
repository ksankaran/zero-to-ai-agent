# From: Zero to AI Agent, Chapter 7, Section 7.4
# File: exercise_2_7_4_solution.py

"""
Exercise 2 Solution: Few-Shot Template Creation
Create effective few-shot prompts for various tasks.
"""

from typing import List, Dict


def create_few_shot_templates():
    """
    Create few-shot prompt templates for different tasks.
    """
    
    print("=" * 70)
    print("EXERCISE 2: FEW-SHOT TEMPLATE CREATION")
    print("=" * 70)
    
    # Task 1: Date Extraction
    date_extraction_template()
    
    # Task 2: Customer Support Classification
    support_classification_template()
    
    # Task 3: Informal to Formal Conversion
    formality_conversion_template()
    
    # Best practices
    show_few_shot_best_practices()


def date_extraction_template():
    """Create few-shot template for extracting dates from text."""
    
    print("\n📅 TASK 1: EXTRACTING DATES FROM TEXT")
    print("-" * 50)
    
    template = """Extract all dates from the given text and format them as YYYY-MM-DD.

Examples:

Text: "The meeting is scheduled for January 15th, 2024."
Dates: 2024-01-15

Text: "We launched on 03/20/2023 and had our first update by April 2023."
Dates: 2023-03-20, 2023-04-01 (assuming first of month when day not specified)

Text: "The contract expires next Tuesday, which is the 5th of December."
Dates: 2024-12-05 (assuming current year when not specified)

Text: "Founded in 1995, the company went public on July 4, 2010."
Dates: 1995-01-01 (year only), 2010-07-04

Text: "The deadline was yesterday, and the review is tomorrow."
Dates: [Relative dates - need current date context]

Now extract dates from this text:
Text: {input_text}
Dates:"""
    
    print("TEMPLATE:")
    print(template)
    
    # Show how to use it
    print("\n💻 USAGE EXAMPLE:")
    usage = """
def extract_dates(text):
    prompt = template.format(input_text=text)
    # Send to LLM
    response = llm_call(prompt, temperature=0.1)
    # Parse response
    dates = parse_date_response(response)
    return dates

# Test
text = "The project started on May 1st and ends December 31, 2024"
dates = extract_dates(text)
# Returns: ["2024-05-01", "2024-12-31"]
    """
    print(usage)
    
    print("\n📊 KEY FEATURES:")
    print("• Multiple examples showing different date formats")
    print("• Handles partial dates (year only, month-year)")
    print("• Shows how to handle relative dates")
    print("• Clear output format specification")
    print("• Edge cases included")


def support_classification_template():
    """Create few-shot template for classifying customer support tickets."""
    
    print("\n🎫 TASK 2: CLASSIFYING CUSTOMER SUPPORT TICKETS")
    print("-" * 50)
    
    template = """Classify the customer support ticket into one of these categories:
- TECHNICAL: Software bugs, errors, technical issues
- BILLING: Payment, subscription, refund issues
- FEATURE: Feature requests, suggestions
- ACCOUNT: Login, password, account management
- OTHER: Doesn't fit other categories

Also assign priority: HIGH, MEDIUM, or LOW

Examples:

Ticket: "I can't log into my account. I've tried resetting my password three times."
Category: ACCOUNT
Priority: HIGH

Ticket: "When will you add dark mode? It would really help with eye strain."
Category: FEATURE
Priority: LOW

Ticket: "I was charged twice for my monthly subscription. Please refund the duplicate charge."
Category: BILLING
Priority: HIGH

Ticket: "The app crashes whenever I try to upload a file larger than 10MB."
Category: TECHNICAL
Priority: HIGH

Ticket: "How do I change my notification settings? I can't find the option."
Category: ACCOUNT
Priority: LOW

Ticket: "Your service is great! Just wanted to say thanks."
Category: OTHER
Priority: LOW

Now classify this ticket:
Ticket: {ticket_text}
Category:
Priority:"""
    
    print("TEMPLATE:")
    print(template)
    
    print("\n🎯 CLASSIFICATION SCHEMA:")
    schema = {
        "TECHNICAL": ["bug", "error", "crash", "slow", "broken", "not working"],
        "BILLING": ["charge", "payment", "refund", "invoice", "subscription", "price"],
        "FEATURE": ["add", "request", "would be nice", "suggestion", "improve"],
        "ACCOUNT": ["login", "password", "email", "profile", "settings", "can't access"],
        "OTHER": ["thanks", "praise", "general question", "feedback"]
    }
    
    for category, keywords in schema.items():
        print(f"\n{category}:")
        print(f"  Keywords: {', '.join(keywords[:4])}...")
    
    print("\n⚡ PRIORITY RULES:")
    print("• HIGH: Can't use service, money issues, data loss")
    print("• MEDIUM: Functionality impaired but workarounds exist")
    print("• LOW: Questions, suggestions, minor inconveniences")


def formality_conversion_template():
    """Create few-shot template for converting informal to formal text."""
    
    print("\n👔 TASK 3: INFORMAL TO FORMAL BUSINESS LANGUAGE")
    print("-" * 50)
    
    template = """Convert informal text to professional business language while preserving the meaning.

Examples:

Informal: "Hey, just wanted to check if you got my email about the project?"
Formal: "I am writing to inquire whether you have received my email regarding the project."

Informal: "Can we push the meeting? Something came up."
Formal: "Would it be possible to reschedule our meeting? An urgent matter has arisen that requires my immediate attention."

Informal: "The numbers look kinda weird. Mind taking another look?"
Formal: "Upon review, the figures appear to contain some inconsistencies. Could you please verify the data?"

Informal: "Thanks for getting back to me so fast!"
Formal: "Thank you for your prompt response."

Informal: "Sorry for the late reply - things have been crazy here."
Formal: "I apologize for the delayed response. We have been experiencing an unusually high volume of activity."

Informal: "Let me know if you need anything else!"
Formal: "Please do not hesitate to contact me if you require any additional assistance."

Now convert this text:
Informal: {informal_text}
Formal:"""
    
    print("TEMPLATE:")
    print(template)
    
    print("\n📝 TRANSFORMATION PATTERNS:")
    
    patterns = [
        ("Contractions", "don't → do not, can't → cannot"),
        ("Casual greetings", "Hey → Good morning/afternoon"),
        ("Colloquialisms", "kinda → somewhat, stuff → matters"),
        ("Informal phrases", "ASAP → at your earliest convenience"),
        ("Casual closings", "Thanks! → Thank you for your consideration"),
        ("Slang/shortcuts", "info → information, docs → documents")
    ]
    
    for pattern, example in patterns:
        print(f"\n• {pattern}:")
        print(f"  {example}")
    
    print("\n✨ ADVANCED TEMPLATE VARIATION:")
    advanced = """
# For different formality levels:

Level 1 (Casual Professional):
- Friendly but professional
- Some contractions OK
- Personal pronouns acceptable

Level 2 (Standard Business):
- No contractions
- Third person preferred
- Standard business phrases

Level 3 (Highly Formal):
- Very formal language
- Passive voice when appropriate
- Traditional business conventions
    """
    print(advanced)


def show_few_shot_best_practices():
    """Show best practices for creating few-shot templates."""
    
    print("\n" + "=" * 70)
    print("FEW-SHOT TEMPLATE BEST PRACTICES")
    print("=" * 70)
    
    practices = [
        {
            "principle": "Diverse Examples",
            "description": "Include 3-6 examples covering different cases",
            "why": "Shows pattern variations and edge cases"
        },
        {
            "principle": "Consistent Format",
            "description": "Use exact same format for all examples",
            "why": "Makes pattern recognition easier for LLM"
        },
        {
            "principle": "Progressive Complexity",
            "description": "Start simple, add complexity gradually",
            "why": "Builds understanding step by step"
        },
        {
            "principle": "Include Edge Cases",
            "description": "Show handling of exceptions and special cases",
            "why": "Prevents failures on unusual inputs"
        },
        {
            "principle": "Clear Delimiters",
            "description": "Use clear markers between sections",
            "why": "Helps LLM parse structure correctly"
        },
        {
            "principle": "Output Specification",
            "description": "Show exact desired output format",
            "why": "Ensures consistent, parseable responses"
        }
    ]
    
    for p in practices:
        print(f"\n📋 {p['principle']}")
        print(f"   {p['description']}")
        print(f"   Why: {p['why']}")
    
    print("\n🎯 TEMPLATE STRUCTURE:")
    structure = """
[TASK DESCRIPTION]
Clear explanation of what to do

[EXAMPLES]
Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

Input: [example 3 input]
Output: [example 3 output]

[ACTUAL TASK]
Input: {user_input}
Output:
    """
    print(structure)


def create_universal_few_shot_template():
    """Create a universal few-shot template generator."""
    
    print("\n" + "=" * 70)
    print("UNIVERSAL FEW-SHOT TEMPLATE GENERATOR")
    print("=" * 70)
    
    code = '''
class FewShotTemplate:
    """Universal few-shot template generator."""
    
    def __init__(self, task_description: str):
        self.task_description = task_description
        self.examples = []
    
    def add_example(self, input_text: str, output_text: str, note: str = ""):
        """Add an example to the template."""
        self.examples.append({
            "input": input_text,
            "output": output_text,
            "note": note
        })
    
    def generate_prompt(self, user_input: str) -> str:
        """Generate the complete few-shot prompt."""
        prompt = f"{self.task_description}\\n\\n"
        
        if self.examples:
            prompt += "Examples:\\n\\n"
            for i, ex in enumerate(self.examples, 1):
                prompt += f"Example {i}:\\n"
                prompt += f"Input: {ex['input']}\\n"
                prompt += f"Output: {ex['output']}\\n"
                if ex['note']:
                    prompt += f"Note: {ex['note']}\\n"
                prompt += "\\n"
        
        prompt += f"Now process this:\\n"
        prompt += f"Input: {user_input}\\n"
        prompt += f"Output:"
        
        return prompt

# Usage example
template = FewShotTemplate("Extract key points from text as bullet points")
template.add_example(
    "The weather is nice today. It's sunny and warm.",
    "• Weather is nice\\n• Sunny conditions\\n• Warm temperature"
)
template.add_example(
    "The project deadline is Friday. We need to finish the report.",
    "• Project deadline: Friday\\n• Report needs completion"
)

prompt = template.generate_prompt("New user input here")
    '''
    
    print("IMPLEMENTATION:")
    print(code)


def main():
    """Run few-shot template creation exercise."""
    
    # Create templates
    create_few_shot_templates()
    
    # Universal generator
    create_universal_few_shot_template()
    
    print("\n" + "=" * 70)
    print("EXERCISE 2 COMPLETE")
    print("=" * 70)
    print("\n✅ You've learned to create effective few-shot templates!")
    print("   Remember: Clear examples + consistent format = better results!")


if __name__ == "__main__":
    main()
