# From: AI Agents Book - Chapter 13, Section 13.2
# File: conversation_memory.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from datetime import datetime

class ConversationMemory:
    def __init__(self, system_prompt=None, max_messages=50):
        self.client = OpenAI()
        self.max_messages = max_messages
        self.messages = []
        
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
    
    def add_user_message(self, content):
        self.messages.append({
            "role": "user",
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self._trim_if_needed()
    
    def add_assistant_message(self, content):
        self.messages.append({
            "role": "assistant", 
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def _trim_if_needed(self):
        """Remove oldest messages if we exceed max_messages."""
        while len(self.messages) > self.max_messages:
            # Find first non-system message and remove it
            for i, msg in enumerate(self.messages):
                if msg["role"] != "system":
                    self.messages.pop(i)
                    break
    
    def get_messages_for_api(self):
        """Return messages formatted for API call (without timestamps)."""
        return [
            {"role": m["role"], "content": m["content"]} 
            for m in self.messages
        ]
    
    def chat(self, user_input):
        self.add_user_message(user_input)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.get_messages_for_api()
        )
        
        assistant_reply = response.choices[0].message.content
        self.add_assistant_message(assistant_reply)
        
        return assistant_reply
    
    def get_history(self):
        """Return conversation history for inspection."""
        return self.messages.copy()
    
    def clear(self):
        """Clear conversation but keep system prompt."""
        system_msgs = [m for m in self.messages if m["role"] == "system"]
        self.messages = system_msgs


# Example usage
if __name__ == "__main__":
    # Create a memory-enabled conversation
    memory = ConversationMemory(
        system_prompt="You are a friendly travel advisor.",
        max_messages=30
    )

    # Chat naturally
    print(memory.chat("I'm planning a trip to Japan."))
    print(memory.chat("What's the best time to visit?"))
    print(memory.chat("And what about the trip I mentioned?"))  # It remembers!

    # Check history if needed
    for msg in memory.get_history():
        print(f"{msg['role']}: {msg['content'][:50]}...")
