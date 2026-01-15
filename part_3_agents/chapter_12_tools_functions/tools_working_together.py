# From: Zero to AI Agent, Chapter 12, Section 12.3
# File: tools_working_together.py

from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WriteFileTool
import tempfile

# Initialize our tools
search_tool = DuckDuckGoSearchRun()
wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
)
working_dir = tempfile.mkdtemp(prefix="research_")
write_tool = WriteFileTool(root_dir=working_dir)

print("Demonstrating How Tools Complement Each Other")
print("=" * 50)

# Research task: Learn about a topic from multiple angles
topic = "Large Language Models"

# Step 1: Get established facts from Wikipedia
print(f"\n1. Wikipedia (Established Facts) about {topic}:")
wiki_result = wikipedia_tool.run(topic)
wiki_summary = wiki_result[:200] + "..."
print(wiki_summary)

# Step 2: Get current developments from search
print(f"\n2. Web Search (Recent News) about {topic}:")
search_query = f"{topic} breakthrough 2024 news"
search_result = search_tool.run(search_query)
search_summary = search_result[:200] + "..."
print(search_summary)

# Step 3: Save the combined research
print(f"\n3. Saving Research to File:")
research_report = f"""Research Report: {topic}
Generated on: {tempfile.gettempdir()}

ESTABLISHED FACTS (Wikipedia):
{wiki_result[:400]}

RECENT DEVELOPMENTS (Web Search):
{search_result[:400]}

Summary: This report combines foundational knowledge with current developments.
"""

write_tool.run({
    "file_path": "research_report.txt",
    "text": research_report
})
print(f"   Report saved to: {working_dir}/research_report.txt")

print("\n" + "=" * 50)
print("Notice how each tool serves a different purpose:")
print("- Wikipedia: Authoritative, stable information")
print("- Web Search: Current events and recent developments")
print("- File Tools: Persistence and report generation")
print("\nWhen agents use these together, they become research assistants!")
