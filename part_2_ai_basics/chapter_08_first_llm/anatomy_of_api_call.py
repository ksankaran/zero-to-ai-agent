# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: anatomy_of_api_call.py

import openai
from pathlib import Path

# Load API key (you know this part!)
def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

# Let's explore EVERY parameter you can use!
response = client.chat.completions.create(
    # 1. MODEL - Which AI brain to use
    model="gpt-3.5-turbo",  # Fast and cheap!
    # model="gpt-4",        # Smarter but slower
    # model="gpt-3.5-turbo-1106",  # Specific version
    
    # 2. MESSAGES - The conversation history
    messages=[
        # System message: Sets the AI's personality/role
        {"role": "system", "content": "You are a helpful assistant who explains things simply."},
        
        # User message: What the human says
        {"role": "user", "content": "What is Python?"},
        
        # Assistant message: Previous AI responses (for context)
        # {"role": "assistant", "content": "Previous response here..."},
    ],
    
    # 3. TEMPERATURE - Creativity control (0.0 to 2.0)
    temperature=0.7,  # 0 = focused/deterministic, 2 = very creative/random
    
    # 4. MAX_TOKENS - Maximum response length
    max_tokens=150,  # Roughly 1 token = 0.75 words
    
    # 5. TOP_P - Another way to control randomness (usually use temperature OR top_p, not both)
    top_p=1.0,  # 0.1 = only most likely words, 1.0 = consider all words
    
    # 6. FREQUENCY_PENALTY - Reduce repetition (-2.0 to 2.0)
    frequency_penalty=0.0,  # Positive = less repetition
    
    # 7. PRESENCE_PENALTY - Encourage new topics (-2.0 to 2.0)  
    presence_penalty=0.0,  # Positive = talk about new things
    
    # 8. STOP - Stop sequences (where to cut off response)
    stop=None,  # Can be a list like ["\n", ".", "END"]
    
    # 9. N - How many responses to generate
    n=1,  # Generate multiple responses and pick the best!
    
    # 10. STREAM - Get response as it's generated
    stream=False,  # True = see response word by word
    
    # 11. USER - Unique identifier for the user (for OpenAI's monitoring)
    user=None,  # Can be a user ID for tracking
)

# Understanding the response structure
print("🔍 API Response Structure:")
print(f"ID: {response.id}")
print(f"Model used: {response.model}")
print(f"Created at: {response.created}")

# The actual message
message = response.choices[0].message
print(f"\n💬 Response: {message.content}")

# Token usage (this is what costs money!)
if response.usage:
    print(f"\n📊 Token Usage:")
    print(f"  Prompt tokens: {response.usage.prompt_tokens}")
    print(f"  Response tokens: {response.usage.completion_tokens}")
    print(f"  Total tokens: {response.usage.total_tokens}")
    
    # Cost calculation (GPT-3.5-turbo pricing)
    cost = (response.usage.total_tokens / 1000) * 0.002
    print(f"  Estimated cost: ${cost:.6f}")

# Why the response was cut off (if applicable)
print(f"\n🛑 Finish reason: {response.choices[0].finish_reason}")
# Possible values:
# - "stop": Natural ending
# - "length": Hit max_tokens limit  
# - "content_filter": Blocked by safety filter
# - "null": Still generating (if streaming)
