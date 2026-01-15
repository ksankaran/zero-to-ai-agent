# From: Zero to AI Agent, Chapter 8, Section 8.4
# File: smart_retry.py

import openai
from pathlib import Path
import time
import random

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

def exponential_backoff(attempt):
    """Calculate wait time with exponential backoff"""
    # 1st attempt: 1 sec, 2nd: 2 sec, 3rd: 4 sec, etc.
    base_wait = 2 ** attempt
    
    # Add jitter to prevent thundering herd
    jitter = random.uniform(0, 0.5)
    
    return min(base_wait + jitter, 32)  # Max 32 seconds

def api_call_with_retry(client, messages, max_retries=3):
    """Make API call with automatic retry on failure"""
    last_error = None
    
    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempt {attempt + 1}/{max_retries}...")
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            print("✅ Success!")
            return response.choices[0].message.content, None
        
        except openai.RateLimitError as e:
            last_error = e
            if attempt < max_retries - 1:
                wait_time = exponential_backoff(attempt)
                print(f"⏳ Rate limit hit. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            else:
                print("❌ Rate limit persists after retries")
        
        except openai.APITimeoutError as e:
            last_error = e
            if attempt < max_retries - 1:
                wait_time = exponential_backoff(attempt)
                print(f"⏱️ Timeout. Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            else:
                print("❌ Timeout after all retries")
        
        except openai.APIConnectionError as e:
            last_error = e
            if attempt < max_retries - 1:
                wait_time = exponential_backoff(attempt)
                print(f"🌐 Connection error. Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            else:
                print("❌ Connection failed after all retries")
        
        except openai.AuthenticationError:
            # Don't retry auth errors - they won't fix themselves
            print("❌ Authentication failed - check your API key")
            return None, "Invalid API key"
        
        except Exception as e:
            # Don't retry unexpected errors
            print(f"❌ Unexpected error: {type(e).__name__}")
            return None, str(e)
    
    # All retries failed
    return None, f"Failed after {max_retries} attempts: {str(last_error)}"

# Test the retry mechanism
api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    exit()

client = openai.OpenAI(api_key=api_key)

print("🔄 Smart Retry Demo")
print("=" * 50)
print("Testing retry mechanism with different scenarios")
print("-" * 50)

# Test 1: Normal request (should succeed on first try)
print("\n📝 Test 1: Normal request")
messages = [{"role": "user", "content": "Say hello!"}]
response, error = api_call_with_retry(client, messages)
if response:
    print(f"Response: {response}")

# Test 2: Simulate rate limit (you can trigger this with rapid requests)
print("\n📝 Test 2: Multiple rapid requests")
for i in range(3):
    print(f"\nRequest {i+1}:")
    messages = [{"role": "user", "content": f"Count to {i+1}"}]
    response, error = api_call_with_retry(client, messages)
    if response:
        print(f"Response: {response[:50]}...")
    else:
        print(f"Failed: {error}")

print("\n" + "=" * 50)
print("💡 Retry best practices:")
print("  • Use exponential backoff (wait longer each retry)")
print("  • Add jitter to prevent synchronized retries")
print("  • Don't retry authentication errors")
print("  • Set a reasonable max retry limit")
