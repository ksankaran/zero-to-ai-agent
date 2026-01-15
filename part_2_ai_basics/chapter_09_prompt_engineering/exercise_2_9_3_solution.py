# From: Zero to AI Agent, Chapter 9, Section 9.3
# File: exercise_2_9_3_solution.py

"""
Convert generic text into three different communication styles
"""

def create_style_prompt(style_name: str, examples: list) -> str:
    """Build a few-shot prompt for a specific style"""
    
    prompt = f"Convert to {style_name} style:\n\n"
    
    for original, converted in examples:
        prompt += f"Original: {original}\n"
        prompt += f"{style_name}: {converted}\n\n"
    
    return prompt

# Corporate Speak Examples
corporate_examples = [
    (
        "We need to fix this problem quickly.",
        "We should leverage our core competencies to action a solution-oriented approach to this challenge."
    ),
    (
        "The project is running late.",
        "The project timeline requires strategic realignment to optimize deliverable schedules."
    ),
    (
        "Customers don't like the new feature.",
        "User feedback indicates opportunities for enhancement in our latest feature deployment."
    )
]

# Gen Z Social Media Examples  
gen_z_examples = [
    (
        "We need to fix this problem quickly.",
        "this is broken fr fr, gotta fix asap no cap"
    ),
    (
        "The project is running late.",
        "project's not giving what it's supposed to give rn ngl"
    ),
    (
        "Customers don't like the new feature.",
        "users are saying the new feature is mid, kinda cringe tbh"
    )
]

# Academic Writing Examples
academic_examples = [
    (
        "We need to fix this problem quickly.",
        "It has been determined that immediate remediation of the identified issue is required."
    ),
    (
        "The project is running late.",
        "Current analysis suggests that project completion parameters exceed initially projected timelines."
    ),
    (
        "Customers don't like the new feature.",
        "User satisfaction metrics indicate suboptimal reception of recently implemented functionality."
    )
]

def demonstrate_styles():
    """Show how the same content transforms across styles"""
    
    test_sentence = "Our sales increased this month."
    
    styles = [
        ("Corporate Speak", corporate_examples),
        ("Gen Z Social Media", gen_z_examples),
        ("Academic Writing", academic_examples)
    ]
    
    print("STYLE TRANSFORMATION DEMONSTRATION")
    print("="*50)
    print(f"Original sentence: '{test_sentence}'")
    print("="*50)
    
    for style_name, examples in styles:
        prompt = create_style_prompt(style_name, examples)
        print(f"\n{style_name} Style:")
        print("-"*30)
        
        if style_name == "Corporate Speak":
            print("→ 'Our revenue streams have demonstrated positive momentum in the current fiscal period.'")
        elif style_name == "Gen Z Social Media":
            print("→ 'sales went crazy this month, we're literally winning'")
        else:  # Academic
            print("→ 'Analysis of financial data reveals upward trends in revenue generation during the observed period.'")
        
        print(f"\nLearned from {len(examples)} examples:")
        for i, (orig, conv) in enumerate(examples[:2], 1):  # Show first 2
            print(f"  Example {i}: '{orig[:30]}...'")

if __name__ == "__main__":
    demonstrate_styles()