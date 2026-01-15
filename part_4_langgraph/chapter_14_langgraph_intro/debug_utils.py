# From: Building AI Agents, Chapter 14, Section 14.7
# File: debug_utils.py

"""Debugging utilities for LangGraph applications.

Provides decorators to add debug output to nodes and routing functions
without cluttering the main logic.
"""


def debug_node(name: str):
    """Decorator that adds debug output to any node function.
    
    Usage:
        @debug_node("my_node")
        def my_node(state: MyState) -> dict:
            ...
    """
    def decorator(func):
        def wrapper(state):
            # Print entry
            print(f"\n{'='*50}")
            print(f"🔵 ENTERING: {name}")
            print(f"{'='*50}")
            
            # Print incoming state
            print(f"📥 State received:")
            for key, value in state.items():
                str_val = str(value)[:60] + "..." if len(str(value)) > 60 else str(value)
                print(f"   {key}: {str_val}")
            
            # Call the actual function
            result = func(state)
            
            # Print outgoing updates
            print(f"\n📤 Returning updates:")
            if result:
                for key, value in result.items():
                    str_val = str(value)[:60] + "..." if len(str(value)) > 60 else str(value)
                    print(f"   {key}: {str_val}")
            else:
                print("   (no updates)")
            
            print(f"{'='*50}\n")
            
            return result
        return wrapper
    return decorator


def debug_router(name: str):
    """Decorator that adds debug output to routing functions.
    
    Usage:
        @debug_router("my_router")
        def my_router(state: MyState) -> str:
            ...
    """
    def decorator(func):
        def wrapper(state):
            result = func(state)
            print(f"🔀 ROUTER '{name}' decided: {result}")
            return result
        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    from typing import TypedDict
    
    class ExampleState(TypedDict):
        message: str
        processed: bool
    
    @debug_node("example_node")
    def example_node(state: ExampleState) -> dict:
        return {"processed": True}
    
    @debug_router("example_router")
    def example_router(state: ExampleState) -> str:
        return "next" if state.get("processed") else "process"
    
    # Test
    test_state = {"message": "Hello", "processed": False}
    result = example_node(test_state)
    decision = example_router(test_state)
