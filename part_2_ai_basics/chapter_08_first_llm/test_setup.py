# From: Zero to AI Agent, Chapter 8, Section 8.1
# File: test_setup.py

import sys
from pathlib import Path

print("🧪 Testing Your AI Setup")
print("=" * 40)

# Test 1: Check if OpenAI is installed
try:
    import openai
    print("✅ OpenAI package installed")
except ImportError:
    print("❌ OpenAI not installed. Run: pip install openai")
    sys.exit(1)

# Test 2: Check for API key
env_file = Path(".env")
if not env_file.exists():
    print("❌ No .env file found. Run: python setup_api_key.py")
    sys.exit(1)

api_key = None
with open(env_file, 'r') as f:
    for line in f:
        if line.startswith('OPENAI_API_KEY='):
            api_key = line.split('=')[1].strip()
            break

if not api_key or api_key == 'your-key-here':
    print("❌ No valid API key in .env file")
    sys.exit(1)

print("✅ API key found")

# Test 3: Try a real API call
print("🔄 Testing API connection...")
try:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say 'test successful' in 3 words or less"}],
        max_tokens=10
    )
    result = response.choices[0].message.content
    print(f"✅ API call successful! AI said: {result}")
except Exception as e:
    print(f"❌ API call failed: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! You're ready to build AI apps!")
