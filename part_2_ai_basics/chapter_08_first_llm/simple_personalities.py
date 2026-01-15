# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: simple_personalities.py

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

api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

# Try different personalities with the SAME question
question = "How do I make friends?"

print("🎭 Same Question, 3 Different Personalities")
print("=" * 60)

# Personality 1: Friendly buddy
print("\n1️⃣ FRIENDLY BUDDY:")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a friendly, casual buddy. Use simple language and be encouraging!"},
        {"role": "user", "content": question}
    ]
)
print(response.choices[0].message.content)

# Personality 2: Professional coach
print("\n2️⃣ PROFESSIONAL COACH:")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a professional life coach. Be formal and give structured advice."},
        {"role": "user", "content": question}
    ]
)
print(response.choices[0].message.content)

# Personality 3: Wise grandparent
print("\n3️⃣ WISE GRANDPARENT:")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a wise, caring grandparent. Share life wisdom and be warm."},
        {"role": "user", "content": question}
    ]
)
print(response.choices[0].message.content)

print("\n" + "=" * 60)
print("💡 See how the system message changes the AI's style?")
print("   You just learned how ChatGPT's 'Custom Instructions' work!")
