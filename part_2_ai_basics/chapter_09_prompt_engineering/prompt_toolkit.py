# From: Zero to AI Agent, Chapter 9, Section 9.1
# File: prompt_toolkit.py

"""
A simple template system for managing and reusing common prompts
"""

import json

# Store your best prompts for reuse
prompt_templates = {
    "code_review": """You are reviewing code for a {context} project.
Focus on: {focus_areas}
The developer has {experience} experience.
Code: {code}
Provide specific, actionable feedback.""",
    
    "bug_fix": """This {language} function should {expected_behavior}.
Instead, it {actual_behavior}.
Code: {code}
Find the bug and explain the fix.""",
    
    "explanation": """Explain {concept} to someone with {knowledge_level} knowledge.
Use {explanation_style} style.
Keep it under {word_limit} words."""
}

# Function to fill in a template
def use_template(template_name, **kwargs):
    template = prompt_templates[template_name]
    return template.format(**kwargs)

# Example usage
if __name__ == "__main__":
    prompt = use_template(
        "code_review",
        context="learning",
        focus_areas="best practices and potential errors",
        experience="6 months Python",
        code="def calc(x, y): return x/y"
    )
    
    print(prompt)