# From: Zero to AI Agent, Chapter 7, Section 7.4
# File: exercise_1_7_4_solution.py

"""
Exercise 1 Solution: Prompt Improvement Challenge
Transform weak prompts into effective ones using prompt engineering techniques.
"""

from typing import Dict, List, Tuple


def improve_prompts():
    """
    Improve weak prompts using prompt engineering best practices.
    """
    
    print("=" * 70)
    print("EXERCISE 1: PROMPT IMPROVEMENT CHALLENGE")
    print("=" * 70)
    
    weak_prompts = [
        "Write about space",
        "Fix this: def func(x): return x/0",
        "Translate: Hello",
        "Make a list",
        "Explain AI"
    ]
    
    for i, weak in enumerate(weak_prompts, 1):
        print(f"\n{i}. WEAK PROMPT: \"{weak}\"")
        print("-" * 50)
        
        improved = improve_single_prompt(weak, i)
        
        print("✨ IMPROVED VERSION:")
        print("```")
        print(improved["prompt"])
        print("```")
        
        print("\n📊 IMPROVEMENTS APPLIED:")
        for improvement in improved["improvements"]:
            print(f"  • {improvement}")
        
        print("\n💡 WHY THIS IS BETTER:")
        print(f"  {improved['reasoning']}")
    
    # Show general principles
    show_improvement_principles()


def improve_single_prompt(weak_prompt: str, number: int) -> Dict:
    """Improve a single weak prompt."""
    
    improvements = {
        1: {  # "Write about space"
            "prompt": """Write a 300-word educational article about space exploration for high school students.

Include:
- 2-3 recent achievements in space exploration
- Why space exploration matters for humanity
- One specific mission or technology in detail

Style: Engaging but informative, avoid technical jargon.
Format: Include a compelling opening hook and a forward-looking conclusion.""",
            "improvements": [
                "Added specific audience (high school students)",
                "Defined length (300 words)",
                "Listed specific content requirements",
                "Clarified tone and style",
                "Specified structure expectations"
            ],
            "reasoning": "The original prompt was too vague. The improved version provides context, constraints, and clear expectations, leading to more useful and targeted output."
        },
        
        2: {  # "Fix this: def func(x): return x/0"
            "prompt": """Debug and fix this Python function that's causing a ZeroDivisionError:

```python
def func(x):
    return x/0
```

Requirements:
1. Identify the error and explain why it occurs
2. Provide a corrected version with proper error handling
3. Include at least 2 different approaches to handle division by zero
4. Add docstring and type hints
5. Write a simple test to verify the fix

Context: This function is part of a calculator application where x represents user input.""",
            "improvements": [
                "Specified the exact error to address",
                "Required explanation of the problem",
                "Asked for multiple solutions",
                "Added code quality requirements",
                "Provided application context"
            ],
            "reasoning": "Simply saying 'fix this' doesn't guide the response. The improved version teaches debugging methodology and ensures robust error handling."
        },
        
        3: {  # "Translate: Hello"
            "prompt": """Translate "Hello" into the following languages, including pronunciation guide and cultural context:

Languages:
1. Spanish
2. French  
3. Japanese
4. Arabic
5. Mandarin Chinese

For each translation, provide:
- The written form (with script for non-Latin alphabets)
- Phonetic pronunciation for English speakers
- Formal vs informal variations if applicable
- Cultural note about appropriate usage

Example format:
Language: [Translation] | Pronunciation: [Guide] | Context: [When/how to use]""",
            "improvements": [
                "Specified target languages",
                "Requested pronunciation guides",
                "Asked for cultural context",
                "Provided output format",
                "Included formal/informal distinctions"
            ],
            "reasoning": "A single word translation lacks context. The improved version provides practical, usable information for real communication."
        },
        
        4: {  # "Make a list"
            "prompt": """Create a prioritized checklist for launching a small online business.

Specifications:
- 15-20 actionable items
- Organized into 3 phases: Planning, Setup, and Launch
- Each item should be specific and measurable
- Include time estimates (hours/days/weeks)
- Mark critical path items with [CRITICAL]
- Add brief explanation for why each item matters

Format as a numbered list with clear phase headers.
Target audience: First-time entrepreneur with limited budget.""",
            "improvements": [
                "Defined the type and purpose of list",
                "Specified item count and organization",
                "Required actionable, measurable items",
                "Added time estimates requirement",
                "Identified target audience"
            ],
            "reasoning": "'Make a list' could mean anything. The improved version creates a valuable, actionable resource with clear structure and purpose."
        },
        
        5: {  # "Explain AI"
            "prompt": """Explain artificial intelligence to a curious 12-year-old using everyday analogies.

Cover these key points:
1. What AI is (and isn't)
2. How AI learns from examples
3. One specific example they use daily (like YouTube recommendations)
4. Why AI sometimes makes mistakes
5. How AI might help them in the future

Requirements:
- Use at least 2 relatable analogies
- Avoid technical terms or explain them simply
- Keep it under 400 words
- End with an engaging question to spark further curiosity

Tone: Friendly, encouraging, and wonder-inducing.""",
            "improvements": [
                "Defined specific audience and their level",
                "Listed key points to cover",
                "Required relatable analogies",
                "Set appropriate length",
                "Specified engaging tone"
            ],
            "reasoning": "'Explain AI' is too broad. The improved version creates an age-appropriate, engaging explanation that actually teaches understanding."
        }
    }
    
    return improvements[number]


def show_improvement_principles():
    """Show general principles for improving prompts."""
    
    print("\n" + "=" * 70)
    print("PROMPT IMPROVEMENT PRINCIPLES")
    print("=" * 70)
    
    principles = [
        {
            "principle": "Be Specific",
            "bad": "Write something",
            "good": "Write a 500-word blog post about...",
            "why": "Specificity reduces ambiguity"
        },
        {
            "principle": "Define the Audience",
            "bad": "Explain quantum physics",
            "good": "Explain quantum physics to a high school student",
            "why": "Audience determines language and depth"
        },
        {
            "principle": "Set Clear Constraints",
            "bad": "Make it good",
            "good": "Make it engaging, under 200 words, with examples",
            "why": "Constraints guide creativity"
        },
        {
            "principle": "Provide Context",
            "bad": "Fix this code",
            "good": "Fix this code that processes user payments",
            "why": "Context informs appropriate solutions"
        },
        {
            "principle": "Specify Format",
            "bad": "List some ideas",
            "good": "List 5 ideas as bullet points with brief explanations",
            "why": "Format specifications ensure usable output"
        },
        {
            "principle": "Include Examples",
            "bad": "Format this data",
            "good": "Format this data like this example: Name | Age | City",
            "why": "Examples clarify expectations"
        }
    ]
    
    for p in principles:
        print(f"\n📋 {p['principle']}")
        print(f"   ❌ Bad: \"{p['bad']}\"")
        print(f"   ✅ Good: \"{p['good']}\"")
        print(f"   💡 Why: {p['why']}")


def create_prompt_template():
    """Create a reusable template for well-structured prompts."""
    
    print("\n" + "=" * 70)
    print("UNIVERSAL PROMPT TEMPLATE")
    print("=" * 70)
    
    template = """
[ROLE/CONTEXT]
You are a [specific role] helping with [specific task].

[TASK]
[Clear, specific description of what you want]

[REQUIREMENTS]
- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]

[CONSTRAINTS]
- Length: [word/token count]
- Style: [tone/formality level]
- Format: [output structure]

[EXAMPLES] (if needed)
Input: [example input]
Output: [example output]

[ADDITIONAL CONTEXT] (if relevant)
[Any background information that helps]
    """
    
    print("Use this template to structure your prompts:")
    print(template)
    
    print("\n✅ Example using the template:")
    
    example = """
[ROLE/CONTEXT]
You are a technical documentation writer helping with API documentation.

[TASK]
Write clear documentation for a REST API endpoint that creates new user accounts.

[REQUIREMENTS]
- Include endpoint URL, HTTP method, and authentication
- Document all request parameters with types and validation rules
- Show example request and response bodies
- List possible error codes and their meanings

[CONSTRAINTS]
- Length: 300-400 words
- Style: Technical but accessible to junior developers
- Format: Markdown with code blocks

[EXAMPLES]
Similar to Stripe's API documentation style

[ADDITIONAL CONTEXT]
This is for a SaaS application's public API used by third-party developers.
    """
    
    print(example)


def main():
    """Run prompt improvement exercise."""
    
    # Improve prompts
    improve_prompts()
    
    # Show template
    create_prompt_template()
    
    print("\n" + "=" * 70)
    print("EXERCISE 1 COMPLETE")
    print("=" * 70)
    print("\n✅ You've learned to transform vague prompts into effective ones!")
    print("   Remember: Specific, Contextual, Constrained, and Formatted!")


if __name__ == "__main__":
    main()
