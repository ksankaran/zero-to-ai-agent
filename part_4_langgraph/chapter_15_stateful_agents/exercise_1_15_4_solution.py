# From: Zero to AI Agent, Chapter 15, Section 15.4
# File: exercise_1_15_4_solution.py

"""
Multi-user chat system with SQLite persistence.
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from datetime import datetime
import sqlite3

class ChatState(TypedDict):
    messages: Annotated[list[dict], add]
    user_id: str
    last_activity: str

def update_activity(state: ChatState) -> dict:
    return {"last_activity": datetime.now().isoformat()}

# Build minimal graph
graph = StateGraph(ChatState)
graph.add_node("update", update_activity)
graph.add_edge(START, "update")
graph.add_edge("update", END)

DB_PATH = "multiuser_chat.db"

def send_message(user_id: str, content: str, role: str = "user"):
    """Send a message in a user's chat."""
    with SqliteSaver.from_conn_string(DB_PATH) as saver:
        app = graph.compile(checkpointer=saver)
        thread_id = f"chat:{user_id}"
        config = {"configurable": {"thread_id": thread_id}}
        
        # Load or create state
        try:
            current = app.get_state(config).values or {}
        except:
            current = {}
        
        state = {
            "messages": current.get("messages", []) + [{"role": role, "content": content}],
            "user_id": user_id,
            "last_activity": ""
        }
        
        return app.invoke(state, config)

def list_user_conversations(user_id: str):
    """List all conversations for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Find threads for this user
    cursor.execute(
        "SELECT DISTINCT thread_id FROM checkpoints WHERE thread_id LIKE ?",
        (f"chat:{user_id}%",)
    )
    
    conversations = []
    with SqliteSaver.from_conn_string(DB_PATH) as saver:
        app = graph.compile(checkpointer=saver)
        
        for (thread_id,) in cursor.fetchall():
            config = {"configurable": {"thread_id": thread_id}}
            state = app.get_state(config)
            
            if state.values:
                conversations.append({
                    "thread_id": thread_id,
                    "message_count": len(state.values.get("messages", [])),
                    "last_activity": state.values.get("last_activity", "Unknown")
                })
    
    conn.close()
    return conversations

# Demo
print("=== Multi-User Chat ===\n")

# Alice sends messages
send_message("alice", "Hello!")
send_message("alice", "How are you?")
send_message("alice", "Great, thanks!", "assistant")

# Bob sends messages
send_message("bob", "Hi there")

# List Alice's conversations
print("Alice's conversations:")
for conv in list_user_conversations("alice"):
    print(f"  {conv['thread_id']}: {conv['message_count']} messages")

print("\nBob's conversations:")
for conv in list_user_conversations("bob"):
    print(f"  {conv['thread_id']}: {conv['message_count']} messages")
