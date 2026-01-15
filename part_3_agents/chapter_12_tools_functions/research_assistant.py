# From: Zero to AI Agent, Chapter 12, Section 12.7
# File: research_assistant.py

from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Setup built-in tools
search_tool = DuckDuckGoSearchRun()
wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        top_k_results=1,
        doc_content_chars_max=500
    )
)

# Create custom tools for the assistant
def save_notes(content: str) -> str:
    """Save research notes to a file."""
    try:
        # In production, implement proper file handling
        with open("research_notes.txt", "a") as f:
            f.write(f"\n{content}\n")
        return "Notes saved successfully"
    except Exception as e:
        return f"Error saving notes: {e}"

def summarize(text: str) -> str:
    """Create a brief summary of text."""
    # Simple summary (in production, might use another LLM call)
    words = text.split()
    if len(words) > 50:
        summary = ' '.join(words[:50]) + "..."
    else:
        summary = text
    return f"Summary: {summary}"

# Combine all tools
tools = [
    search_tool,
    wikipedia_tool,
    Tool(name="SaveNotes", func=save_notes, 
         description="Save important information to notes. Input: text to save"),
    Tool(name="Summarize", func=summarize,
         description="Create a brief summary. Input: text to summarize"),
]

# Create research assistant
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
client = Client(api_key=langsmith_api_key)
prompt = client.pull_prompt("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=6
)

print("🔬 RESEARCH ASSISTANT READY!")
print("=" * 50)

# Complex research task
research_query = """
Research LangChain framework:
1. Find current information about it
2. Check Wikipedia for background
3. Save the key points to notes
4. Give me a summary
"""

print(f"📚 Research Request: {research_query}")
print("-" * 50)

result = agent_executor.invoke({"input": research_query})

print(f"\n📊 Research Complete!")
print(f"Final Report: {result['output']}")
