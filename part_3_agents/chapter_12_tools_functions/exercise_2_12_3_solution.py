# From: Zero to AI Agent, Chapter 12, Section 12.3
# File: exercise_2_12_3_solution.py

from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WriteFileTool
import tempfile
from datetime import datetime

# Initialize tools
search_tool = DuckDuckGoSearchRun()
wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
)
workspace = tempfile.mkdtemp(prefix="research_")
write_tool = WriteFileTool(root_dir=workspace)

def research_topic(topic):
    """Research workflow for a topic."""
    print(f"Researching: {topic}")
    print("-" * 40)
    
    # 1. Wikipedia for background
    print("1. Getting background from Wikipedia...")
    wiki_result = wikipedia_tool.run(topic)
    background = wiki_result[:500] if wiki_result else "No Wikipedia entry"
    
    # 2. Search for recent developments
    print("2. Searching for recent news...")
    search_result = search_tool.run(f"{topic} latest news 2024")
    recent = search_result[:500] if search_result else "No recent news"
    
    # 3. Create structured report
    report = f"""# Research Report: {topic}
Date: {datetime.now().strftime('%Y-%m-%d')}

## Background Information
{background}

## Recent Developments
{recent}

## Summary
This report combines encyclopedic knowledge with current developments.
"""
    
    # 4. Save report
    filename = f"{topic.replace(' ', '_').lower()}_report.md"
    write_tool.run({"file_path": filename, "text": report})
    print(f"3. Report saved: {workspace}/{filename}\n")
    
    return report

# Research multiple topics
topics = ["Quantum Computing", "Blockchain Technology"]
for topic in topics:
    research_topic(topic)

print(f"All reports saved in: {workspace}")
