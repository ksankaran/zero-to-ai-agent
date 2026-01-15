# From: Zero to AI Agent, Chapter 7, Section 7.1
# File: ai_api_preview.py

"""
Preview of what you'll build soon - integrating with AI APIs.
This demonstrates how your Python skills directly apply to AI development.
"""

import json
import requests
from typing import Dict, Optional

def ask_ai(question: str, api_key: str = "YOUR_KEY", max_tokens: int = 100) -> str:
    """
    Example of calling an AI API - you already know every part of this code!
    
    Your existing Python skills:
    - JSON for data format ✓ (Chapter 6)
    - Requests for API calls ✓ (Chapter 6)
    - Error handling ✓ (Chapter 6)
    - Functions for organization ✓ (Chapter 5)
    - Type hints ✓ (Throughout)
    
    Args:
        question: The prompt to send to the AI
        api_key: Your API key (you'll get this in Chapter 8)
        max_tokens: Maximum length of response
    
    Returns:
        The AI's response text
    
    Note: This is a template. In Chapter 8, you'll make this work
    with real AI services like OpenAI, Anthropic, etc.
    """
    try:
        # Prepare the API request (Chapter 6 skills!)
        api_data = {
            "prompt": question,
            "max_tokens": max_tokens,
            "temperature": 0.7,  # Creativity level (0=focused, 1=creative)
            "model": "gpt-3.5-turbo"  # Which AI model to use
        }
        
        # Make the API call (You did this in Chapter 6!)
        response = requests.post(
            "https://api.ai-service.com/chat",  # You'll use real endpoints soon
            json=api_data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=30  # Good practice: always set timeouts
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse the JSON response (Chapter 6 again!)
        result = response.json()
        
        # Extract the AI's response
        # Different APIs structure this differently
        # OpenAI: result["choices"][0]["message"]["content"]
        # Anthropic: result["completion"]
        # You'll learn the specifics for each provider
        
        return result.get("response", "No response received")
        
    except requests.exceptions.RequestException as e:
        # Network errors
        return f"Network error: {str(e)}"
    except json.JSONDecodeError as e:
        # Invalid JSON response
        return f"Invalid response format: {str(e)}"
    except KeyError as e:
        # Missing expected fields
        return f"Unexpected response structure: {str(e)}"
    except Exception as e:
        # Catch-all for other errors
        return f"Unexpected error: {str(e)}"


def demonstrate_conversation_flow():
    """
    Shows how you'll manage conversations with AI.
    This pattern works with any AI provider.
    """
    
    # Conversation history (like a chat app)
    conversation = []
    
    def add_message(role: str, content: str):
        """Add a message to the conversation."""
        conversation.append({
            "role": role,  # "user", "assistant", or "system"
            "content": content,
            "timestamp": "2024-01-01 12:00:00"  # You might track time
        })
    
    def get_ai_response(user_input: str) -> str:
        """Get AI response while maintaining context."""
        # Add user message
        add_message("user", user_input)
        
        # In real implementation, you'd send the entire
        # conversation history for context
        # response = ask_ai_with_context(conversation)
        
        # For now, just echo
        response = f"AI would respond to: '{user_input}'"
        
        # Add AI response
        add_message("assistant", response)
        
        return response
    
    # Simulate a conversation
    print("="*60)
    print("CONVERSATION FLOW EXAMPLE")
    print("="*60)
    
    # System message sets the AI's behavior
    add_message("system", "You are a helpful Python tutor.")
    
    # User interactions
    questions = [
        "What is a list in Python?",
        "Can you show me an example?",
        "How is it different from a tuple?"
    ]
    
    for question in questions:
        print(f"\n👤 User: {question}")
        response = get_ai_response(question)
        print(f"🤖 AI: {response}")
    
    # Show conversation history
    print("\n" + "="*60)
    print("CONVERSATION HISTORY (What we send to AI):")
    print("="*60)
    for msg in conversation:
        print(f"{msg['role'].upper()}: {msg['content'][:50]}...")


def show_different_ai_tasks():
    """
    Examples of different tasks you'll accomplish with AI APIs.
    """
    
    print("="*60)
    print("WHAT YOU'LL BUILD WITH AI APIs")
    print("="*60)
    
    tasks = {
        "Translation": {
            "prompt": "Translate 'Hello, how are you?' to Spanish",
            "expected": "Hola, ¿cómo estás?"
        },
        "Summarization": {
            "prompt": "Summarize this text in one sentence: [long article]",
            "expected": "One sentence summary of the article"
        },
        "Code Generation": {
            "prompt": "Write a Python function to reverse a string",
            "expected": "def reverse_string(s): return s[::-1]"
        },
        "Question Answering": {
            "prompt": "What is the capital of France?",
            "expected": "Paris"
        },
        "Creative Writing": {
            "prompt": "Write a haiku about programming",
            "expected": "Code flows like water / Bugs hide in the silent depths / Debug brings the light"
        },
        "Data Extraction": {
            "prompt": "Extract the date from: 'Meeting on January 15th at 3pm'",
            "expected": "January 15th"
        }
    }
    
    for task_name, task_info in tasks.items():
        print(f"\n📌 {task_name}:")
        print(f"   Prompt: {task_info['prompt']}")
        print(f"   AI Output: {task_info['expected']}")
    
    print("\n" + "="*60)
    print("🎯 Each task uses the same simple pattern:")
    print("1. Prepare your prompt")
    print("2. Call the AI API")
    print("3. Process the response")
    print("That's it! You already know how to do all three!")


if __name__ == "__main__":
    # Show what's coming
    print("="*60)
    print("🚀 PREVIEW: AI API INTEGRATION")
    print("="*60)
    print("\nYou already have ALL the Python skills needed!")
    print("\nWhat you know:")
    print("✓ Making API calls (requests library)")
    print("✓ Working with JSON data")
    print("✓ Error handling")
    print("✓ Functions and organization")
    print("\nWhat you'll learn:")
    print("• How to get API keys")
    print("• Specific endpoints for each AI service")
    print("• How to structure prompts effectively")
    print("• Managing conversation context")
    print("• Cost optimization strategies")
    
    # Demonstrate the patterns
    print("\n")
    demonstrate_conversation_flow()
    print("\n")
    show_different_ai_tasks()
    
    print("\n" + "="*60)
    print("💡 Remember: AI APIs are just web APIs!")
    print("You've already done this in Chapter 6!")
    print("="*60)
