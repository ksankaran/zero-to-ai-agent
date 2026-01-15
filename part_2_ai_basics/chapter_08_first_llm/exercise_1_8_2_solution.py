# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: exercise_1_8_2_temperature_tester.py

import openai
from pathlib import Path

def load_api_key():
    """Load API key from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

api_key = load_api_key()
if not api_key:
    print("❌ No API key found! Run setup_api_key.py first!")
    exit()

client = openai.OpenAI(api_key=api_key)

print("🌡️ Temperature Tester")
print("=" * 50)

# Get user's prompt
prompt = input("Enter your prompt: ")

print("\nGenerating 3 responses at different temperatures...\n")

# Store responses
responses = {}
temperatures = [0, 0.7, 1.5]

for temp in temperatures:
    print(f"Temperature {temp}:")
    print("-" * 30)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=temp,
        max_tokens=150
    )
    
    response_text = response.choices[0].message.content
    responses[temp] = response_text
    print(response_text)
    print()

# Let user pick favorite
print("=" * 50)
print("Which response did you like best?")
print("1. Temperature 0 (Focused)")
print("2. Temperature 0.7 (Balanced)")  
print("3. Temperature 1.5 (Creative)")

choice = input("\nYour choice (1-3): ")

try:
    idx = int(choice) - 1
    if 0 <= idx < 3:
        chosen_temp = temperatures[idx]
        print(f"\n✅ You preferred temperature {chosen_temp}")
        print("Good to know for future conversations!")
except:
    print("Invalid choice")

print("\n🎉 Thanks for testing temperatures!")
