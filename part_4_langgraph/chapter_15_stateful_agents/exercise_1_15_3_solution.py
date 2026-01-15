# From: Zero to AI Agent, Chapter 15, Section 15.3
# File: exercise_1_15_3_solution.py

"""
Custom reducer that accumulates but removes duplicates.
"""

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END

def dedupe_messages(existing: list, new: list) -> list:
    """Accumulate messages, removing duplicates by content."""
    result = existing.copy()
    seen = {msg["content"] for msg in existing}
    
    for msg in new:
        if msg["content"] not in seen:
            result.append(msg)
            seen.add(msg["content"])
    
    return result

class ChatState(TypedDict):
    messages: Annotated[list[dict], dedupe_messages]

def greeting(state):
    return {"messages": [
        {"role": "system", "content": "Welcome!"},
        {"role": "assistant", "content": "How can I help?"}
    ]}

def help_prompt(state):
    return {"messages": [
        {"role": "assistant", "content": "How can I help?"},  # Duplicate!
        {"role": "assistant", "content": "I'm here to assist."}
    ]}

# Build graph
graph = StateGraph(ChatState)
graph.add_node("greet", greeting)
graph.add_node("help", help_prompt)
graph.add_edge(START, "greet")
graph.add_edge("greet", "help")
graph.add_edge("help", END)

app = graph.compile()
result = app.invoke({"messages": []})

print("=== Dedupe Reducer ===")
print(f"Total messages: {len(result['messages'])}")
for msg in result['messages']:
    print(f"  - {msg['content']}")
print("\n'How can I help?' appears only once!")
