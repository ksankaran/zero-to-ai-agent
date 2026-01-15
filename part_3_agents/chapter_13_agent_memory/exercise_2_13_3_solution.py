# From: AI Agents Book - Chapter 13, Section 13.3
# File: exercise_2_13_3_solution.py
# Exercise: Triggered Summarization

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()

class SmartMemory:
    def __init__(self, system_prompt=None, max_messages=15, keep_recent=5):
        self.max_messages = max_messages
        self.keep_recent = keep_recent
        self.messages = []
        
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
    
    def _count_conversation_messages(self):
        """Count non-system messages (excluding summary)."""
        return len([m for m in self.messages 
                    if m["role"] != "system" or "Summary:" in m.get("content", "")])
    
    def _generate_summary(self, messages):
        """Generate summary of given messages."""
        text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Summarize this conversation concisely:\n\n{text}"
            }],
            max_tokens=250
        )
        return response.choices[0].message.content
    
    def _maybe_summarize(self):
        """Check if summarization is needed and perform it."""
        # Get non-system messages
        conversation = [m for m in self.messages if m["role"] in ("user", "assistant")]
        
        if len(conversation) <= self.max_messages:
            return  # No summarization needed
        
        # Split messages
        to_summarize = conversation[:-self.keep_recent]
        to_keep = conversation[-self.keep_recent:]
        
        # Generate summary
        summary = self._generate_summary(to_summarize)
        
        # Rebuild message list
        system_prompt = [m for m in self.messages 
                         if m["role"] == "system" and "Summary:" not in m["content"]]
        
        summary_msg = {
            "role": "system",
            "content": f"Summary: {summary}"
        }
        
        self.messages = system_prompt + [summary_msg] + to_keep
        
        # Notification
        print(f"\n🔄 SUMMARIZATION TRIGGERED")
        print(f"   Compressed {len(to_summarize)} messages → {len(summary.split())} words")
        print(f"   Kept {len(to_keep)} recent messages")
        print(f"   New total: {len(self.messages)} messages\n")
    
    def chat(self, user_input):
        """Process user input and return assistant response."""
        self.messages.append({"role": "user", "content": user_input})
        
        # Check for summarization
        self._maybe_summarize()
        
        # Get response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        
        return reply
    
    def message_count(self):
        return len(self.messages)


# Test - conversation that exceeds threshold
memory = SmartMemory(
    system_prompt="You are a helpful travel assistant.",
    max_messages=15,
    keep_recent=5
)

test_inputs = [
    "I want to visit Japan.",
    "When is the best time to go?",
    "What about cherry blossom season?",
    "How expensive is it?",
    "What cities should I visit?",
    "Tell me about Tokyo.",
    "What about Kyoto?",
    "How do I get between cities?",
    "Is the rail pass worth it?",
    "What food should I try?",
    "Any vegetarian options?",
    "What about accommodation?",
    "Hotels or ryokans?",
    "How much should I budget per day?",
    "Any cultural tips?",
    "What should I pack?",  # This should trigger summarization
    "Remind me what cities we discussed?"
]

for user_input in test_inputs:
    print(f"User: {user_input}")
    response = memory.chat(user_input)
    print(f"Assistant: {response[:100]}...")
    print(f"[Messages: {memory.message_count()}]\n")
