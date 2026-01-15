# From: Zero to AI Agent, Chapter 19, Section 19.6
# File: model_selector.py
# Description: Simple model routing based on task complexity

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


# Define models for different tasks
cheap_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
powerful_model = ChatOpenAI(model="gpt-4o", temperature=0.7)


def select_model(message: str) -> ChatOpenAI:
    """Select model based on task complexity."""
    
    # Simple patterns that don't need expensive models
    simple_patterns = [
        "hello", "hi", "hey", "thanks", "bye",
        "what time", "what date", "how are you"
    ]
    
    message_lower = message.lower()
    
    # Check for simple patterns
    for pattern in simple_patterns:
        if pattern in message_lower:
            return cheap_model
    
    # Check message length (short = probably simple)
    if len(message.split()) < 10:
        return cheap_model
    
    # Complex keywords that need better models
    complex_patterns = [
        "analyze", "compare", "explain why", "write code",
        "debug", "review", "evaluate", "recommend"
    ]
    
    for pattern in complex_patterns:
        if pattern in message_lower:
            return powerful_model
    
    # Default to cheaper model
    return cheap_model


# Example usage
if __name__ == "__main__":
    test_messages = [
        "Hello!",
        "What time is it?",
        "Analyze this code and explain why it fails",
        "Write code to implement binary search",
        "Thanks for your help!",
    ]
    
    for msg in test_messages:
        model = select_model(msg)
        print(f"'{msg[:40]}...' -> {model.model_name}")
