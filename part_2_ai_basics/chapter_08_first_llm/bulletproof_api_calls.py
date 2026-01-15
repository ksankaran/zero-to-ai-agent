# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: bulletproof_api_calls.py

import openai
import time
from pathlib import Path

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

class SmartAIClient:
    """A smarter way to call the OpenAI API with retry logic"""
    
    def __init__(self, api_key, max_retries=3):
        self.client = openai.OpenAI(api_key=api_key)
        self.max_retries = max_retries
    
    def chat(self, messages, **kwargs):
        """Make an API call with automatic retry on failure"""
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Try to make the API call
                print(f"🔄 Attempt {attempt + 1}...")
                
                response = self.client.chat.completions.create(
                    model=kwargs.get('model', 'gpt-3.5-turbo'),
                    messages=messages,
                    **kwargs
                )
                
                print("✅ Success!")
                return response
                
            except openai.RateLimitError as e:
                # Hit rate limit - wait and retry
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"⏱️ Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                last_error = e
                
            except openai.APIConnectionError as e:
                # Network problem
                print(f"🌐 Connection error: {e}")
                print(f"   Retrying in 3 seconds...")
                time.sleep(3)
                last_error = e
                
            except openai.AuthenticationError as e:
                # Bad API key - don't retry
                print(f"🔑 Authentication failed: {e}")
                print("   Check your API key in .env file!")
                raise
                
            except openai.BadRequestError as e:
                # Our request is wrong - don't retry
                print(f"❌ Bad request: {e}")
                print("   Check your parameters!")
                raise
                
            except openai.APIError as e:
                # OpenAI server error - retry
                print(f"🚨 OpenAI server error: {e}")
                wait_time = 5
                print(f"   Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                last_error = e
                
            except Exception as e:
                # Something unexpected
                print(f"😱 Unexpected error: {e}")
                last_error = e
        
        # All retries failed
        print(f"😔 All {self.max_retries} attempts failed.")
        raise last_error

# Test it out!
api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    exit()

# Create our smart client
smart_client = SmartAIClient(api_key)

print("🛡️ Bulletproof API Calls Demo")
print("=" * 50)

# Test 1: Normal call
print("\n📝 Test 1: Normal API call")
try:
    response = smart_client.chat(
        messages=[{"role": "user", "content": "Say 'Hello, bulletproof world!'"}],
        max_tokens=50
    )
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Failed: {e}")

# Test 2: Call with bad parameter (will fail immediately)
print("\n📝 Test 2: Bad parameter (should fail fast)")
try:
    response = smart_client.chat(
        messages=[{"role": "user", "content": "Test"}],
        temperature=10.0  # Invalid! Max is 2.0
    )
except Exception as e:
    print(f"Caught error as expected: {type(e).__name__}")

# Test 3: Simulate network issues (if you disconnect internet)
print("\n📝 Test 3: Ready for network issues")
print("(This would retry 3 times if network is down)")

print("\n✨ Your API calls are now bulletproof!")
