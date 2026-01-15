# From: Zero to AI Agent, Chapter 8, Section 8.4
# File: error_types_demo.py

# Let's trigger different types of errors and see what happens!

import openai
from pathlib import Path
import time

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

def test_error(description, test_function):
    """Test an error condition and show what happens"""
    print(f"\n🧪 Testing: {description}")
    print("-" * 40)
    try:
        test_function()
        print("✅ No error occurred")
    except Exception as e:
        error_type = type(e).__name__
        print(f"❌ Error Type: {error_type}")
        print(f"📝 Error Message: {str(e)}")
        
        # Show useful error details if available
        if hasattr(e, 'response'):
            print(f"📊 Status Code: {getattr(e, 'status_code', 'N/A')}")
        
        return error_type
    return None

# Setup
print("🔬 API Error Types Explorer")
print("=" * 50)

# Test 1: Invalid API Key
print("\n1️⃣ Invalid API Key Test:")
try:
    bad_client = openai.OpenAI(api_key="sk-invalid-key-12345")
    response = bad_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hi"}]
    )
except Exception as e:
    print(f"❌ {type(e).__name__}: {str(e)[:100]}...")

# Test 2: No API Key
print("\n2️⃣ Missing API Key Test:")
try:
    no_key_client = openai.OpenAI(api_key=None)
    response = no_key_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hi"}]
    )
except Exception as e:
    print(f"❌ {type(e).__name__}: {str(e)[:100]}...")

# Test 3: Invalid Model
api_key = load_api_key()
if api_key:
    client = openai.OpenAI(api_key=api_key)
    
    print("\n3️⃣ Invalid Model Test:")
    try:
        response = client.chat.completions.create(
            model="gpt-99-ultra",  # This model doesn't exist!
            messages=[{"role": "user", "content": "Hi"}]
        )
    except Exception as e:
        print(f"❌ {type(e).__name__}: {str(e)[:100]}...")
    
    # Test 4: Invalid Parameters
    print("\n4️⃣ Invalid Parameters Test:")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            temperature=5.0  # Too high! Max is 2.0
        )
    except Exception as e:
        print(f"❌ {type(e).__name__}: {str(e)[:100]}...")
    
    # Test 5: Empty Messages
    print("\n5️⃣ Empty Messages Test:")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[]  # No messages!
        )
    except Exception as e:
        print(f"❌ {type(e).__name__}: {str(e)[:100]}...")

print("\n" + "=" * 50)
print("💡 Common error types:")
print("  • AuthenticationError: Bad API key")
print("  • NotFoundError: Invalid model or endpoint")
print("  • BadRequestError: Invalid parameters")
print("  • RateLimitError: Too many requests")
print("  • APIConnectionError: Network issues")
