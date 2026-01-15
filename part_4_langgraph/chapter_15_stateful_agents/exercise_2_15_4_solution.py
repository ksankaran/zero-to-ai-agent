# From: Zero to AI Agent, Chapter 15, Section 15.4
# File: exercise_2_15_4_solution.py

"""
Checkpoint cleanup and maintenance utility.
"""

import sqlite3
import os
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class DemoState(TypedDict):
    counter: int

def increment(state: DemoState) -> dict:
    return {"counter": state["counter"] + 1}

# Build graph for creating test data
graph = StateGraph(DemoState)
graph.add_node("inc", increment)
graph.add_edge(START, "inc")
graph.add_edge("inc", END)

DB_PATH = "cleanup_demo.db"

def get_stats(db_path: str) -> dict:
    """Get checkpoint statistics."""
    if not os.path.exists(db_path):
        return {"total": 0, "threads": 0, "size_bytes": 0}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM checkpoints")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT thread_id) FROM checkpoints")
    threads = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total": total,
        "threads": threads,
        "size_bytes": os.path.getsize(db_path)
    }

def cleanup(db_path: str, keep_per_thread: int = 3) -> int:
    """Remove old checkpoints, keeping N most recent per thread."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
    threads = [row[0] for row in cursor.fetchall()]
    
    deleted = 0
    for thread_id in threads:
        cursor.execute("""
            SELECT checkpoint_id FROM checkpoints 
            WHERE thread_id = ? ORDER BY checkpoint_id DESC
        """, (thread_id,))
        
        checkpoints = [row[0] for row in cursor.fetchall()]
        
        for cp_id in checkpoints[keep_per_thread:]:
            cursor.execute("DELETE FROM checkpoints WHERE checkpoint_id = ?", (cp_id,))
            deleted += 1
    
    conn.commit()
    conn.execute("VACUUM")  # Reclaim space
    conn.close()
    
    return deleted

# Create test data
print("=== Checkpoint Cleanup Utility ===\n")
print("Creating test data...")

with SqliteSaver.from_conn_string(DB_PATH) as saver:
    app = graph.compile(checkpointer=saver)
    
    for thread_num in range(3):
        config = {"configurable": {"thread_id": f"thread-{thread_num}"}}
        state = {"counter": 0}
        for _ in range(10):
            state = app.invoke(state, config)

# Show before stats
print("\n--- Before Cleanup ---")
before = get_stats(DB_PATH)
print(f"Checkpoints: {before['total']}")
print(f"Threads: {before['threads']}")
print(f"Size: {before['size_bytes']:,} bytes")

# Run cleanup
deleted = cleanup(DB_PATH, keep_per_thread=2)
print(f"\n--- Cleanup ---")
print(f"Deleted: {deleted} checkpoints")

# Show after stats
print("\n--- After Cleanup ---")
after = get_stats(DB_PATH)
print(f"Checkpoints: {after['total']}")
print(f"Size: {after['size_bytes']:,} bytes")
print(f"Space saved: {before['size_bytes'] - after['size_bytes']:,} bytes")
