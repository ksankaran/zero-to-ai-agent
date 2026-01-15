# From: Zero to AI Agent, Chapter 12, Section 12.3
# File: exploring_wikipedia.py

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Configure Wikipedia tool
wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        top_k_results=1,  # Number of results to return
        doc_content_chars_max=1000  # Max characters per result
    )
)

print("Testing Wikipedia Tool")
print("=" * 50)

# Look up a programming language
result = wikipedia_tool.run("Python (programming language)")
print("Python programming language:")
print(result[:400] + "...")
print()

# Look up a concept
ml_result = wikipedia_tool.run("Machine Learning")
print("Machine Learning:")
# Get just the first two sentences
sentences = ml_result.split('. ')[:2]
print('. '.join(sentences) + '.')
print()

# Look up a person
turing_result = wikipedia_tool.run("Alan Turing")
print("Alan Turing:")
sentences = turing_result.split('. ')[:2]
print('. '.join(sentences) + '.')
