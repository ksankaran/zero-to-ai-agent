# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: temperature_experiments.py

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

def test_temperature(prompt, temperature, description):
    """Test how temperature affects responses"""
    print(f"\n🌡️ Temperature {temperature} - {description}")
    print("-" * 50)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=100
    )
    
    print(f"Response: {response.choices[0].message.content}")
    return response.choices[0].message.content

# Same prompt, different temperatures
prompt = "Write a one-sentence story about a robot"

print("🧪 Temperature Experiment: Same prompt, different creativity levels")
print("=" * 60)

# Temperature 0: Maximum consistency (almost deterministic)
test_temperature(prompt, 0, "Focused/Factual")

# Temperature 0.3: Slightly creative but still focused
test_temperature(prompt, 0.3, "Balanced/Professional")

# Temperature 0.7: Default - good balance
test_temperature(prompt, 0.7, "Creative/Natural")

# Temperature 1.0: More creative and varied
test_temperature(prompt, 1.0, "Very Creative")

# Temperature 1.5: Wild and unpredictable
test_temperature(prompt, 1.5, "Experimental/Wild")

print("\n" + "=" * 60)
print("💡 When to use different temperatures:")
print("  📊 0.0-0.3: Code generation, facts, math, analysis")
print("  📝 0.4-0.7: General chat, explanations, summaries")
print("  🎨 0.8-1.2: Creative writing, brainstorming, stories")
print("  🎲 1.3-2.0: Experimental, poetry, wild ideas")
