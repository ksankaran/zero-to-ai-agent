# From: Zero to AI Agent, Chapter 12, Section 12.3
# File: exercise_1_12_3_solution.py

from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Initialize tools
search_tool = DuckDuckGoSearchRun()
wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
)

print("TOOL EXPLORER - COMPARISON STUDY")
print("=" * 60)

# Test DuckDuckGo with different queries
print("\n1. DUCKDUCKGO TESTS")
print("-" * 40)
queries = {
    "news": "AI breakthroughs 2024",
    "facts": "population of Tokyo",
    "tutorial": "Python pandas beginner"
}

for qtype, query in queries.items():
    result = search_tool.run(query)
    print(f"\n{qtype.upper()}: {query}")
    print(f"Result: {result[:150]}...")
    print(f"Best for: {'Current info' if qtype == 'news' else 'Quick facts' if qtype == 'facts' else 'Learning resources'}")

# Test Wikipedia with different topics  
print("\n\n2. WIKIPEDIA TESTS")
print("-" * 40)
topics = {
    "person": "Albert Einstein",
    "place": "Tokyo",
    "concept": "Machine Learning"
}

for ttype, topic in topics.items():
    result = wikipedia_tool.run(topic)
    print(f"\n{ttype.upper()}: {topic}")
    print(f"Result: {result[:150]}...")
    print(f"Best for: {'Biographies' if ttype == 'person' else 'Geography' if ttype == 'place' else 'Definitions'}")

print("\n\nCOMPARISON SUMMARY:")
print("DuckDuckGo: Current events, tutorials, recent info")
print("Wikipedia: Established facts, biographies, concepts")
