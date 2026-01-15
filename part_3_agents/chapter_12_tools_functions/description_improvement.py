# From: Zero to AI Agent, Chapter 12, Section 12.5
# File: description_improvement.py

from langchain_core.tools import Tool

# Bad descriptions - vague and ambiguous
bad_calculator = Tool(
    name="calc",
    func=lambda x: eval(x),
    description="calculator"  # Too vague!
)

bad_search = Tool(
    name="srch",
    func=lambda x: f"Results for {x}",
    description="searches stuff"  # What stuff? When?
)

# Good descriptions - clear and specific
good_calculator = Tool(
    name="calculator",
    func=lambda x: eval(x),
    description=(
        "Use this for mathematical calculations and arithmetic. "
        "Input: mathematical expression like '2+2' or '15*3.14'. "
        "Output: numerical result as a string."
    )
)

good_search = Tool(
    name="web_search",
    func=lambda x: f"Results for {x}",
    description=(
        "Use this to search the web for current information, news, or facts. "
        "Best for: recent events, current data, or topics after 2021. "
        "Input: search query string. "
        "Output: relevant web snippets and summaries."
    )
)

print("DESCRIPTION COMPARISON")
print("=" * 50)

print("\n❌ BAD DESCRIPTIONS:")
print(f"Calculator: '{bad_calculator.description}'")
print(f"Search: '{bad_search.description}'")

print("\n✅ GOOD DESCRIPTIONS:")
print(f"Calculator: '{good_calculator.description}'")
print(f"Search: '{good_search.description}'")

print("\n💡 The difference:")
print("- Good descriptions explain WHEN to use the tool")
print("- They specify input/output formats")
print("- They include examples or use cases")
print("- They differentiate from similar tools")
