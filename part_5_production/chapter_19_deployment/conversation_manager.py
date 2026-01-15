# From: Zero to AI Agent, Chapter 19, Section 19.6
# File: conversation_manager.py
# Description: Tools for managing conversation history to control costs

from typing import List, Dict


def trim_conversation(messages: List[Dict], max_messages: int = 10) -> List[Dict]:
    """
    Keep only recent messages (sliding window approach).
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        max_messages: Maximum number of messages to keep
    
    Returns:
        Trimmed list of messages
    """
    if len(messages) <= max_messages:
        return messages
    
    # Always keep system message + recent messages
    system_msgs = [m for m in messages if m["role"] == "system"]
    other_msgs = [m for m in messages if m["role"] != "system"]
    
    return system_msgs + other_msgs[-(max_messages - len(system_msgs)):]


async def summarize_conversation(messages: List[Dict], llm) -> str:
    """
    Create a summary of conversation history.
    
    Args:
        messages: List of message dicts
        llm: LLM instance to use for summarization
    
    Returns:
        Summary string
    """
    conversation_text = "\n".join([
        f"{m['role']}: {m['content']}" 
        for m in messages
    ])
    
    summary_prompt = f"""Summarize this conversation in 2-3 sentences, 
capturing key points and decisions:

{conversation_text}"""
    
    response = await llm.ainvoke(summary_prompt)
    return response.content


async def compress_history(messages: List[Dict], llm, threshold: int = 15) -> List[Dict]:
    """
    Compress old messages into a summary when history gets long.
    
    Args:
        messages: Full message history
        llm: LLM instance for summarization
        threshold: Number of messages before compression
    
    Returns:
        Compressed message list
    """
    if len(messages) < threshold:
        return messages
    
    # Keep system message
    system_msgs = [m for m in messages if m["role"] == "system"]
    other_msgs = [m for m in messages if m["role"] != "system"]
    
    # Summarize older messages
    old_messages = other_msgs[:-5]  # All but last 5
    recent_messages = other_msgs[-5:]  # Keep last 5 intact
    
    summary = await summarize_conversation(old_messages, llm)
    
    # Create compressed history
    return system_msgs + [
        {"role": "system", "content": f"Previous conversation summary: {summary}"}
    ] + recent_messages


def smart_truncate(messages: List[Dict], max_tokens: int = 2000) -> List[Dict]:
    """
    Truncate messages while preserving important content.
    Keeps first and last messages intact, shortens middle ones.
    
    Args:
        messages: List of message dicts
        max_tokens: Approximate token limit
    
    Returns:
        Truncated message list
    """
    # Rough token estimation (4 chars per token)
    def estimate_tokens(text: str) -> int:
        return len(text) // 4
    
    total_tokens = sum(estimate_tokens(m["content"]) for m in messages)
    
    if total_tokens <= max_tokens:
        return messages
    
    # Strategy: shorten middle messages more aggressively
    result = []
    for i, msg in enumerate(messages):
        if i == 0 or i >= len(messages) - 2:
            # Keep first and last messages intact
            result.append(msg)
        else:
            # Truncate middle messages
            content = msg["content"]
            if len(content) > 200:
                content = content[:100] + "..." + content[-100:]
            result.append({**msg, "content": content})
    
    return result


# Example usage
if __name__ == "__main__":
    # Test trim_conversation
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Message 1"},
        {"role": "assistant", "content": "Response 1"},
        {"role": "user", "content": "Message 2"},
        {"role": "assistant", "content": "Response 2"},
        {"role": "user", "content": "Message 3"},
        {"role": "assistant", "content": "Response 3"},
        {"role": "user", "content": "Message 4"},
        {"role": "assistant", "content": "Response 4"},
        {"role": "user", "content": "Message 5"},
        {"role": "assistant", "content": "Response 5"},
    ]
    
    print("Original messages:", len(messages))
    trimmed = trim_conversation(messages, max_messages=6)
    print("After trimming to 6:", len(trimmed))
    print("Kept:", [m["content"][:20] for m in trimmed])
