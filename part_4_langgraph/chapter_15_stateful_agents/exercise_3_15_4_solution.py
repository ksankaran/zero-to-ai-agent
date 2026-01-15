# From: Zero to AI Agent, Chapter 15, Section 15.4
# File: exercise_3_15_4_solution.py

"""
Conversation export/import and forking utility.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from datetime import datetime
import json

class ConvoState(TypedDict):
    messages: Annotated[list[dict], add]
    metadata: dict

def process(state: ConvoState) -> dict:
    return {"metadata": {**state.get("metadata", {}), "updated": datetime.now().isoformat()}}

graph = StateGraph(ConvoState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

DB_PATH = "export_demo.db"

def export_conversation(thread_id: str, output_file: str):
    """Export conversation to JSON file."""
    with SqliteSaver.from_conn_string(DB_PATH) as saver:
        app = graph.compile(checkpointer=saver)
        config = {"configurable": {"thread_id": thread_id}}
        
        state = app.get_state(config)
        if not state.values:
            raise ValueError(f"Thread not found: {thread_id}")
        
        export_data = {
            "thread_id": thread_id,
            "exported_at": datetime.now().isoformat(),
            "state": state.values
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return export_data

def import_conversation(input_file: str, new_thread_id: str):
    """Import conversation from JSON file."""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    state = data["state"]
    state["metadata"] = {
        **state.get("metadata", {}),
        "imported_from": data["thread_id"],
        "imported_at": datetime.now().isoformat()
    }
    
    with SqliteSaver.from_conn_string(DB_PATH) as saver:
        app = graph.compile(checkpointer=saver)
        config = {"configurable": {"thread_id": new_thread_id}}
        return app.invoke(state, config)

def fork_conversation(source_thread: str, new_thread: str):
    """Create a copy of a conversation in a new thread."""
    with SqliteSaver.from_conn_string(DB_PATH) as saver:
        app = graph.compile(checkpointer=saver)
        
        # Load source
        source_config = {"configurable": {"thread_id": source_thread}}
        source_state = app.get_state(source_config).values
        
        # Add fork metadata
        source_state["metadata"] = {
            **source_state.get("metadata", {}),
            "forked_from": source_thread,
            "forked_at": datetime.now().isoformat()
        }
        
        # Save to new thread
        new_config = {"configurable": {"thread_id": new_thread}}
        return app.invoke(source_state, new_config)

# Demo
print("=== Export/Import Tool ===\n")

# Create a conversation
with SqliteSaver.from_conn_string(DB_PATH) as saver:
    app = graph.compile(checkpointer=saver)
    config = {"configurable": {"thread_id": "original"}}
    
    state = {
        "messages": [{"role": "user", "content": "Hello!"}],
        "metadata": {"topic": "greeting"}
    }
    app.invoke(state, config)
    print("Created original conversation")

# Export
export_conversation("original", "backup.json")
print("Exported to backup.json")

# Import to new thread
import_conversation("backup.json", "imported")
print("Imported to 'imported' thread")

# Fork
fork_conversation("original", "forked")
print("Forked to 'forked' thread")

# Verify all exist
print("\n--- All Threads ---")
with SqliteSaver.from_conn_string(DB_PATH) as saver:
    app = graph.compile(checkpointer=saver)
    
    for thread in ["original", "imported", "forked"]:
        config = {"configurable": {"thread_id": thread}}
        state = app.get_state(config)
        print(f"  {thread}: {len(state.values.get('messages', []))} messages")
