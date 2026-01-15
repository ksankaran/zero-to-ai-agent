# From: Zero to AI Agent, Chapter 8, Section 8.3
# File: response_comparison.py

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

# Setup
api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

prompt = "Write a creative tagline for a coffee shop"

print("☕ Comparing Different Temperatures")
print("=" * 50)
print(f"Prompt: {prompt}\n")

temperatures = [0.2, 0.7, 1.2]
total_tokens = 0
total_cost = 0

for temp in temperatures:
    print(f"\n🌡️ Temperature: {temp}")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=temp
    )
    
    message = response.choices[0].message.content
    tokens = response.usage.total_tokens
    cost = tokens * 0.002 / 1000
    
    print(f"Response: {message}")
    print(f"Tokens: {tokens}")
    print(f"Cost: ${cost:.6f}")
    
    total_tokens += tokens
    total_cost += cost

print("\n" + "=" * 50)
print(f"📊 Totals:")
print(f"  Total tokens: {total_tokens}")
print(f"  Total cost: ${total_cost:.6f}")
print(f"  Average per response: ${total_cost/len(temperatures):.6f}")
