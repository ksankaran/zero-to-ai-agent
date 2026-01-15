# From: Building AI Agents, Chapter 14, Section 14.7
# File: step_executor.py

"""Execute a graph step by step for debugging.

Allows you to pause between nodes, inspect state,
and understand the execution flow interactively.
"""


def step_through(app, initial_state: dict):
    """Execute graph step by step, pausing between nodes.
    
    This lets you inspect state after each node.
    
    Args:
        app: A compiled LangGraph application
        initial_state: The initial state dictionary
        
    Returns:
        The final state after execution, or None if stopped early
    """
    print("\n🐛 Step-Through Debugger")
    print("=" * 50)
    print("Commands: [enter]=next, 's'=show state, 'q'=quit")
    print("=" * 50)
    
    # Get stream of execution steps
    step_count = 0
    
    for event in app.stream(initial_state):
        step_count += 1
        
        # event is a dict with the node name as key
        for node_name, node_output in event.items():
            print(f"\n--- Step {step_count}: {node_name} completed ---")
            
            # Show what this node returned
            if node_output:
                print("Output:")
                for key, value in node_output.items():
                    str_val = str(value)[:80]
                    print(f"  {key}: {str_val}")
        
        # Interactive prompt
        cmd = input("\n> ").strip().lower()
        
        if cmd == 'q':
            print("Stopped by user")
            return None
        elif cmd == 's':
            print("\nFull state would be shown here")
            # Note: Getting full state mid-stream requires checkpointing
            # which we'll cover in Chapter 15
    
    print(f"\n✅ Execution complete ({step_count} steps)")
    return event


# Example usage
if __name__ == "__main__":
    print("This module provides the step_through() function.")
    print("Usage:")
    print("  from step_executor import step_through")
    print("  app = create_my_graph()")
    print("  final_state = step_through(app, initial_state)")
