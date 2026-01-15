# From: AI Agents Book - Chapter 13
# File: personal_assistant_challenge.py
# Chapter 13 Challenge: Personal AI Assistant

from dotenv import load_dotenv
load_dotenv()

"""
Chapter 13 Challenge: Build a Complete Personal AI Assistant

Requirements:
1. Remember conversations across sessions (persistence)
2. Track entities mentioned in conversations (people, projects, preferences)
3. Use tools (at least 2: calculator and weather/time)
4. Implement semantic search to recall relevant past conversations
5. Auto-summarize when conversations get long (>500 tokens)
6. Handle privacy with PII filtering
7. Implement cleanup with 30-day retention policy
8. Support multiple users with isolated memories

Bonus Challenges:
- Add a "remember" command for explicit fact storage
- Implement importance-based cleanup (keep important convos longer)
- Add conversation export feature (GDPR compliance)
- Build a simple CLI or web interface
- Track and report memory system metrics

Time Estimate: 3-5 hours
"""

from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
# import chromadb  # Uncomment when implementing semantic search


class PersonalAssistant:
    """Your personal AI assistant with production-ready memory."""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.setup_memory()
        self.setup_agent()
    
    def setup_memory(self):
        """Set up conversation memory, entity memory, vector memory."""
        # TODO: Initialize conversation memory (SQLite-backed)
        # TODO: Initialize entity memory
        # TODO: Initialize vector memory (ChromaDB)
        # TODO: Initialize PII filter
        # TODO: Set up retention policy
        pass
    
    def setup_agent(self):
        """Create agent with tools and memory."""
        # TODO: Define tools (calculator, weather, etc.)
        # TODO: Create prompt with memory context
        # TODO: Set up agent with summarization
        pass
    
    def chat(self, message):
        """Process message, use tools, store in memory."""
        # TODO: Filter PII from input
        # TODO: Retrieve relevant memories
        # TODO: Get entity context
        # TODO: Run agent
        # TODO: Store conversation in memory
        # TODO: Extract and store entities
        # TODO: Check if summarization needed
        pass
    
    def remember(self, fact):
        """Store explicit fact in semantic memory."""
        # TODO: Add fact to vector database
        pass
    
    def recall(self, query):
        """Search relevant past conversations."""
        # TODO: Semantic search in vector database
        # TODO: Return relevant memories
        pass
    
    def export_data(self):
        """Export all user data (GDPR compliance)."""
        # TODO: Gather all user data
        # TODO: Format for export
        pass
    
    def delete_data(self):
        """Delete all user data (GDPR right to erasure)."""
        # TODO: Delete from all memory systems
        pass
    
    def cleanup(self):
        """Run retention policy."""
        # TODO: Delete old conversations
        # TODO: Report metrics
        pass


# Define your tools here
@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression like '2+2' or '10*5'."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Mock implementation - replace with real API
    weather_data = {
        "Seattle": "Rainy, 55°F",
        "NYC": "Sunny, 68°F",
        "Austin": "Hot, 95°F",
    }
    return weather_data.get(city, f"Weather in {city}: Partly cloudy, 70°F")


@tool
def get_time(timezone: str = "UTC") -> str:
    """Get current time in specified timezone."""
    from datetime import datetime
    # Simple implementation - enhance with pytz for real timezones
    return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


# Test your assistant
if __name__ == "__main__":
    print("=" * 60)
    print("Chapter 13 Challenge: Personal AI Assistant")
    print("=" * 60)
    print("\nThis is a starter template. Implement the TODO items!")
    print("\nExpected behavior when complete:")
    print("  1. assistant.chat() processes messages with memory")
    print("  2. assistant.remember() stores facts")
    print("  3. assistant.recall() searches past conversations")
    print("  4. PII is filtered automatically")
    print("  5. Old conversations are cleaned up")
    print("  6. Multiple users have isolated memories")
    print("\n" + "=" * 60)
    
    # Uncomment when implementing:
    # assistant = PersonalAssistant("user_123")
    # assistant.chat("My name is Alice and I'm a Python developer.")
    # assistant.chat("What's the weather in Seattle?")
    # assistant.chat("What did I tell you about myself?")
    # assistant.remember("Alice prefers dark mode")
    # print(assistant.recall("preferences"))
