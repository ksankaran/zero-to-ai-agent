# From: Zero to AI Agent, Chapter 12, Section 12.5
# File: tool_routing_patterns.py

from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Pattern 1: Hierarchical Tools (General → Specific)
def quick_answer(question: str) -> str:
    return f"Quick answer: {question[:50]}..."

def detailed_answer(question: str) -> str:
    return f"Detailed analysis: {question} [500 words]..."

def expert_answer(question: str) -> str:
    return f"Expert consultation: {question} [with citations]..."

hierarchy_tools = [
    Tool(
        name="quick_answer",
        func=quick_answer,
        description="For simple questions needing fast, brief answers (1-2 sentences)"
    ),
    Tool(
        name="detailed_answer",
        func=detailed_answer,
        description="For complex questions needing thorough explanation (paragraph+)"
    ),
    Tool(
        name="expert_answer",
        func=expert_answer,
        description="For technical questions needing citations and expertise"
    )
]

# Pattern 2: Domain-Specific Tools
def search_products(query: str) -> str:
    return f"Product results: {query}"

def search_documentation(query: str) -> str:
    return f"Documentation: {query}"

def search_forums(query: str) -> str:
    return f"Forum discussions: {query}"

domain_tools = [
    Tool(
        name="product_search",
        func=search_products,
        description="Search for products, prices, and shopping information"
    ),
    Tool(
        name="docs_search",
        func=search_documentation,
        description="Search technical documentation, APIs, and guides"
    ),
    Tool(
        name="forum_search",
        func=search_forums,
        description="Search community forums, discussions, and Q&A"
    )
]

# Test routing
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

print("ROUTING PATTERN EXAMPLES")
print("=" * 50)

# Test hierarchical routing
print("\n1. HIERARCHICAL ROUTING:")
test_hierarchical = [
    "What's 2+2?",  # Should use quick_answer
    "Explain how neural networks work",  # Should use detailed_answer
    "Provide peer-reviewed analysis of CRISPR technology"  # Should use expert_answer
]

llm_hierarchical = llm.bind_tools(hierarchy_tools)
for query in test_hierarchical:
    response = llm_hierarchical.invoke([HumanMessage(content=query)])
    if response.tool_calls:
        print(f"'{query[:30]}...' → {response.tool_calls[0]['name']}")

# Test domain routing
print("\n2. DOMAIN-SPECIFIC ROUTING:")
test_domains = [
    "Find the best laptop under $1000",  # Should use product_search
    "How to use pandas DataFrame",  # Should use docs_search
    "Why is my Python code slow?"  # Should use forum_search
]

llm_domain = llm.bind_tools(domain_tools)
for query in test_domains:
    response = llm_domain.invoke([HumanMessage(content=query)])
    if response.tool_calls:
        print(f"'{query[:30]}...' → {response.tool_calls[0]['name']}")
