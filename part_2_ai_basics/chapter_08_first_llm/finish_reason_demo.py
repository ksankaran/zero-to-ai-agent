# From: Zero to AI Agent, Chapter 8, Section 8.3
# File: finish_reason_demo.py

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

def explain_finish_reason(reason):
    """Explain what each finish reason means"""
    reasons = {
        "stop": "✅ Natural ending - AI completed its thought",
        "length": "✂️ Hit token limit - response was cut off",
        "content_filter": "🚫 Blocked by safety filter",
        "null": "⏳ Still generating (in streaming)",
    }
    return reasons.get(reason, f"❓ Unknown: {reason}")

# Setup
api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

print("🔬 Finish Reason Explorer")
print("=" * 50)

# Test 1: Natural completion
print("\n1️⃣ Natural completion test:")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Count to 5"}],
)
print(f"Response: {response.choices[0].message.content}")
print(f"Finish reason: {response.choices[0].finish_reason}")
print(explain_finish_reason(response.choices[0].finish_reason))

# Test 2: Length limit
print("\n2️⃣ Length limit test:")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Tell me a long story"}],
    max_tokens=10  # Very short limit!
)
print(f"Response: {response.choices[0].message.content}")
print(f"Finish reason: {response.choices[0].finish_reason}")
print(explain_finish_reason(response.choices[0].finish_reason))

# Test 3: Quick task
print("\n3️⃣ Quick task test:")
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What's 2+2?"}],
)
print(f"Response: {response.choices[0].message.content}")
print(f"Finish reason: {response.choices[0].finish_reason}")
print(explain_finish_reason(response.choices[0].finish_reason))

print("\n" + "=" * 50)
print("💡 Understanding finish reasons helps you:")
print("  • Know if responses are complete")
print("  • Detect when you need higher token limits")
print("  • Handle truncated responses properly")
