# From: Zero to AI Agent, Chapter 8, Section 8.3
# File: token_explorer.py

import openai
from pathlib import Path

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

def estimate_tokens(text):
    """Rough estimate: 1 token ≈ 4 characters or 0.75 words"""
    return max(len(text) // 4, len(text.split()) * 4 // 3)

# Setup
api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

# Test different prompts
test_prompts = [
    "Hi",
    "Hello, how are you today?",
    "Write a haiku about coding",
    "Explain quantum computing in simple terms",
]

print("🔬 Token Usage Explorer")
print("=" * 50)

for prompt in test_prompts:
    print(f"\n📝 Prompt: '{prompt}'")
    print(f"📏 Estimated tokens: {estimate_tokens(prompt)}")
    
    # Make API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Get actual token counts
    if response.usage:
        print(f"✅ Actual prompt tokens: {response.usage.prompt_tokens}")
        print(f"✅ Response tokens: {response.usage.completion_tokens}")
        print(f"✅ Total tokens: {response.usage.total_tokens}")
        
        # Cost
        cost = response.usage.total_tokens * 0.002 / 1000
        print(f"💰 Cost: ${cost:.6f}")
    
    # Show the response
    message = response.choices[0].message.content
    print(f"💬 Response: {message[:50]}...")

print("\n" + "=" * 50)
print("💡 Tip: Shorter prompts = lower costs!")
