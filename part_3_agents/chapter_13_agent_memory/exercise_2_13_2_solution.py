# From: AI Agents Book - Chapter 13, Section 13.2
# File: exercise_2_13_2_solution.py
# Exercise: Smart Token-Aware Trimming

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()

class TokenAwareMemory:
    def __init__(self, system_prompt, max_tokens=500):
        self.max_tokens = max_tokens
        self.messages = [{"role": "system", "content": system_prompt}]
    
    def estimate_tokens(self, text):
        """Simple token estimation: words * 1.3"""
        return int(len(text.split()) * 1.3)
    
    def total_tokens(self):
        """Calculate total tokens in conversation."""
        total = 0
        for msg in self.messages:
            total += self.estimate_tokens(msg["content"])
        return total
    
    def trim_if_needed(self):
        """Remove oldest non-system messages if over token limit."""
        trimmed = False
        while self.total_tokens() > self.max_tokens and len(self.messages) > 2:
            # Find and remove oldest non-system message
            for i, msg in enumerate(self.messages):
                if msg["role"] != "system":
                    removed = self.messages.pop(i)
                    trimmed = True
                    print(f"⚠️  TRIMMED: Removed {msg['role']} message ({self.estimate_tokens(removed['content'])} tokens)")
                    break
        
        if trimmed:
            print(f"   Current token count: {self.total_tokens()}/{self.max_tokens}")
    
    def chat(self, user_message):
        # Add user message
        self.messages.append({"role": "user", "content": user_message})
        self.trim_if_needed()
        
        # Make API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        
        # Store response
        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})
        self.trim_if_needed()
        
        print(f"[Tokens: {self.total_tokens()}/{self.max_tokens}, Messages: {len(self.messages)}]")
        return assistant_message

# Test with conversation that exceeds limit
memory = TokenAwareMemory(
    system_prompt="You are a storyteller who gives detailed responses.",
    max_tokens=500
)

# These longer exchanges should trigger trimming
prompts = [
    "Tell me a short story about a brave knight.",
    "What happened next to the knight?",
    "Did the knight find what they were looking for?",
    "How does the story end?",
    "What lesson does this story teach?"
]

for prompt in prompts:
    print(f"\nUser: {prompt}")
    response = memory.chat(prompt)
    print(f"Assistant: {response[:100]}...")
