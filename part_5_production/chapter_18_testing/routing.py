# From: AI Agents Book, Chapter 18, Section 18.1
# File: routing.py
# Description: Conditional edge routing logic for LangGraph agents


def route_after_llm(state: dict) -> str:
    """Decide where to go after the LLM responds."""
    messages = state.get("messages", [])
    
    if not messages:
        return "error_handler"
    
    last_message = messages[-1]
    
    # Check if LLM wants to use a tool
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "execute_tools"
    
    # Check if conversation should end
    if state.get("should_end", False):
        return "goodbye"
    
    # Continue conversation
    return "respond_to_user"
