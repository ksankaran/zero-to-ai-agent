# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: demo_modular.py

"""Demonstrate the modular architecture"""

from chatbot_core import ChatBot
from api_helper import get_client
from personalities import get_personality
from memory_manager import MemoryManager

def demonstrate_modules():
    """Show how modules work together"""
    
    print("🧩 Modular Chatbot Architecture Demo")
    print("=" * 50)
    
    # 1. API Setup (one line!)
    client = get_client()
    print("✅ API client ready")
    
    # 2. Choose personality (one line!)
    personality = get_personality("friendly")
    print("✅ Personality loaded")
    
    # 3. Create chatbot (one line!)
    bot = ChatBot(client, personality)
    print("✅ Chatbot created")
    
    # 4. Memory manager (one line!)
    memory = MemoryManager(max_messages=10)
    print("✅ Memory manager ready")
    
    print("\n" + "=" * 50)
    print("Each module is independent and reusable!")
    print("Mix and match them however you need!")
    
    # Example: Quick test
    response = bot.chat("Hello! What's 2+2?")
    print(f"\nTest chat: {response}")
    
    # Show context management
    test_messages = [{"role": "user", "content": f"Message {i}"} for i in range(15)]
    context = memory.get_context(test_messages)
    print(f"\n15 messages → {len(context)} in context (truncated: {memory.should_truncate(test_messages)})")

if __name__ == "__main__":
    demonstrate_modules()
