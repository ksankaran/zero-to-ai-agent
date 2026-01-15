# From: Zero to AI Agent, Chapter 15, Section 15.4
# File: persistence_demo.py

"""
Complete persistence demonstration.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

class ChatState(TypedDict):
    messages: Annotated[list[str], add]
    turn: int

def chat_turn(state: ChatState) -> dict:
    turn = state["turn"] + 1
    return {
        "messages": [f"Turn {turn}: Hello!"],
        "turn": turn
    }

# Build graph
graph = StateGraph(ChatState)
graph.add_node("chat", chat_turn)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# Run with persistence
DB_PATH = "chat_demo.db"

print("=== Session 1: Starting fresh ===")
with SqliteSaver.from_conn_string(DB_PATH) as saver:
    app = graph.compile(checkpointer=saver)
    config = {"configurable": {"thread_id": "demo"}}
    
    # Two turns
    state = {"messages": [], "turn": 0}
    state = app.invoke(state, config)
    state = app.invoke(state, config)
    
    print(f"Messages: {state['messages']}")
    print(f"Turn: {state['turn']}")

print("\n=== Session 2: Resuming after 'restart' ===")
with SqliteSaver.from_conn_string(DB_PATH) as saver:
    app = graph.compile(checkpointer=saver)
    config = {"configurable": {"thread_id": "demo"}}
    
    # Load existing state
    existing = app.get_state(config)
    print(f"Loaded {existing.values['turn']} turns from disk!")
    
    # Continue
    state = app.invoke(existing.values, config)
    print(f"Messages: {state['messages']}")
    print(f"Turn: {state['turn']}")
