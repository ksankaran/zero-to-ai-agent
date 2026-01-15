# From: Zero to AI Agent, Chapter 12, Section 12.5
# File: tool_selection_basics.py

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Create tools with varying specificity
def general_search(query: str) -> str:
    return f"General web results for: {query}"

def news_search(query: str) -> str:
    return f"Latest news about: {query}"

def academic_search(query: str) -> str:
    return f"Academic papers about: {query}"

def weather_check(location: str) -> str:
    return f"Weather in {location}: Sunny, 72°F"

# Create tools with clear, specific descriptions
tools = [
    Tool(
        name="general_search",
        func=general_search,
        description="Search the web for any kind of information"
    ),
    Tool(
        name="news_search",
        func=news_search,
        description="Search specifically for recent news and current events"
    ),
    Tool(
        name="academic_search",
        func=academic_search,
        description="Search for academic papers, research, and scholarly articles"
    ),
    Tool(
        name="weather",
        func=weather_check,
        description="Get current weather for a specific location"
    )
]

# Create LLM with tools
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Test different queries to see tool selection
test_queries = [
    "What's the weather in Paris?",
    "Find recent news about AI",
    "Search for information about Python",
    "Find academic research on machine learning"
]

print("TOOL SELECTION DEMONSTRATION")
print("=" * 50)

for query in test_queries:
    response = llm_with_tools.invoke([HumanMessage(content=query)])
    
    print(f"\nQuery: '{query}'")
    if response.tool_calls:
        selected_tool = response.tool_calls[0]['name']
        print(f"Selected: {selected_tool}")
        print(f"Reasoning: Matched keywords and intent to tool description")
    else:
        print("No tool selected")
