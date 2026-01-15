# From: Zero to AI Agent, Chapter 16, Section 16.2
# File: sequential_pipeline.py

"""
Sequential pattern: Research → Draft → Edit pipeline.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)


class ArticleState(TypedDict):
    topic: str
    research: str
    draft: str
    final: str


def researcher_agent(state: ArticleState) -> dict:
    """Stage 1: Research the topic."""
    prompt = f"""Research this topic and provide 3 key facts:
    Topic: {state['topic']}
    
    Format: Three bullet points with factual information."""
    
    response = llm.invoke(prompt)
    print("📚 Researcher complete")
    return {"research": response.content}


def writer_agent(state: ArticleState) -> dict:
    """Stage 2: Write draft based on research."""
    prompt = f"""Write a short paragraph about {state['topic']}.
    
    Use these research points:
    {state['research']}
    
    Keep it to 3-4 sentences."""
    
    response = llm.invoke(prompt)
    print("✍️ Writer complete")
    return {"draft": response.content}


def editor_agent(state: ArticleState) -> dict:
    """Stage 3: Polish the draft."""
    prompt = f"""Edit this draft for clarity and impact:
    
    {state['draft']}
    
    Make it more engaging. Keep the same length."""
    
    response = llm.invoke(prompt)
    print("📝 Editor complete")
    return {"final": response.content}


# Build sequential pipeline
workflow = StateGraph(ArticleState)

workflow.add_node("researcher", researcher_agent)
workflow.add_node("writer", writer_agent)
workflow.add_node("editor", editor_agent)

# Sequential flow: one after another
workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "editor")
workflow.add_edge("editor", END)

app = workflow.compile()

# Run it
result = app.invoke({
    "topic": "The benefits of morning exercise",
    "research": "",
    "draft": "",
    "final": ""
})

print("\n" + "=" * 50)
print("FINAL ARTICLE:")
print("=" * 50)
print(result["final"])
