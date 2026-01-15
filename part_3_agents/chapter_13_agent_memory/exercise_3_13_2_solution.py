# From: AI Agents Book - Chapter 13, Section 13.2
# File: exercise_3_13_2_solution.py
# Exercise: Conversation Analytics

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from openai import OpenAI

client = OpenAI()

class AnalyticsMemory:
    def __init__(self, system_prompt=None):
        self.messages = []
        self.start_time = None
        self.last_activity = None
        
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt,
                "timestamp": datetime.now(),
                "char_count": len(system_prompt)
            })
    
    def add_message(self, role, content):
        now = datetime.now()
        if self.start_time is None:
            self.start_time = now
        self.last_activity = now
        
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": now,
            "char_count": len(content)
        })
    
    def chat(self, user_message):
        self.add_message("user", user_message)
        
        # Prepare messages for API (without metadata)
        api_messages = [{"role": m["role"], "content": m["content"]} for m in self.messages]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=api_messages
        )
        
        assistant_reply = response.choices[0].message.content
        self.add_message("assistant", assistant_reply)
        
        return assistant_reply
    
    def get_stats(self):
        """Calculate and return conversation analytics."""
        # Count by role
        role_counts = {"user": 0, "assistant": 0, "system": 0}
        role_lengths = {"user": [], "assistant": [], "system": []}
        
        longest_msg = {"content": "", "role": "", "length": 0}
        
        for msg in self.messages:
            role = msg["role"]
            length = msg["char_count"]
            
            role_counts[role] += 1
            role_lengths[role].append(length)
            
            if length > longest_msg["length"]:
                longest_msg = {
                    "content": msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"],
                    "role": role,
                    "length": length
                }
        
        # Calculate averages
        avg_lengths = {}
        for role, lengths in role_lengths.items():
            avg_lengths[role] = sum(lengths) / len(lengths) if lengths else 0
        
        # Calculate duration
        duration = None
        if self.start_time and self.last_activity:
            duration = (self.last_activity - self.start_time).total_seconds()
        
        return {
            "total_messages": len(self.messages),
            "message_counts": role_counts,
            "average_lengths": {k: round(v, 1) for k, v in avg_lengths.items()},
            "longest_message": longest_msg,
            "conversation_duration_seconds": round(duration, 2) if duration else 0,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }

# Create and test
memory = AnalyticsMemory(system_prompt="You are a concise assistant.")

# Have a sample conversation
memory.chat("Hello! How are you today?")
memory.chat("Can you explain what machine learning is in simple terms?")
memory.chat("What's the difference between AI and machine learning?")
memory.chat("Thanks for the explanation!")

# Display statistics
stats = memory.get_stats()

print("=" * 50)
print("CONVERSATION ANALYTICS")
print("=" * 50)
print(f"Total Messages: {stats['total_messages']}")
print(f"\nMessage Counts:")
print(f"  - User: {stats['message_counts']['user']}")
print(f"  - Assistant: {stats['message_counts']['assistant']}")
print(f"  - System: {stats['message_counts']['system']}")
print(f"\nAverage Message Length (chars):")
print(f"  - User: {stats['average_lengths']['user']}")
print(f"  - Assistant: {stats['average_lengths']['assistant']}")
print(f"\nLongest Message:")
print(f"  - Role: {stats['longest_message']['role']}")
print(f"  - Length: {stats['longest_message']['length']} chars")
print(f"  - Preview: {stats['longest_message']['content']}")
print(f"\nConversation Duration: {stats['conversation_duration_seconds']} seconds")
print(f"Started: {stats['start_time']}")
print(f"Last Activity: {stats['last_activity']}")
