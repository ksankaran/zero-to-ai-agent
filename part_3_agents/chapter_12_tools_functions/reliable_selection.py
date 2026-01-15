# From: Zero to AI Agent, Chapter 12, Section 12.4
# File: reliable_selection.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Define multiple tools with clear purposes
def calculate(expression: str) -> str:
    """Perform mathematical calculations."""
    try:
        return str(eval(expression))
    except:
        return "Calculation error"

def translate(text: str, target_language: str) -> str:
    """Translate text to another language."""
    # Simulated translation
    translations = {
        "spanish": {"hello": "hola", "goodbye": "adiós"},
        "french": {"hello": "bonjour", "goodbye": "au revoir"}
    }
    # Simple word lookup (real implementation would use an API)
    return f"Translation to {target_language}: {text} → ..."

def search(query: str) -> str:
    """Search for current information."""
    return f"Search results for '{query}': Latest news and updates..."

# Create tools
tools = [
    Tool(name="calculator", func=calculate, description="For math calculations"),
    Tool(name="translator", func=translate, description="For language translation"),
    Tool(name="search", func=search, description="For current information")
]

# Bind all tools
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Test different queries
test_queries = [
    "What is 25 * 4?",
    "How do you say hello in Spanish?",
    "What's the latest news about AI?"
]

for query in test_queries:
    print(f"\nQuery: {query}")
    response = llm_with_tools.invoke([HumanMessage(content=query)])
    
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        print(f"Selected tool: {tool_call['name']}")
        print(f"Confidence: High (structured selection)")
    else:
        print("No tool needed")
