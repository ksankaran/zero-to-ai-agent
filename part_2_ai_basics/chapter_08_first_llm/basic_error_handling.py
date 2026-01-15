# From: Zero to AI Agent, Chapter 8, Section 8.4
# File: basic_error_handling.py

import openai
from pathlib import Path
import sys

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

def safe_api_call(client, messages, max_tokens=None):
    """Make an API call with proper error handling"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content, None
    
    except openai.AuthenticationError:
        return None, "❌ Invalid API key. Please check your credentials."
    
    except openai.RateLimitError as e:
        return None, "⏳ Rate limit hit. Please wait a moment and try again."
    
    except openai.BadRequestError as e:
        return None, f"❌ Invalid request: {str(e)}"
    
    except openai.APIConnectionError:
        return None, "🌐 Network error. Please check your internet connection."
    
    except openai.APITimeoutError:
        return None, "⏱️ Request timed out. Please try again."
    
    except Exception as e:
        # Catch any other errors
        return None, f"❌ Unexpected error: {type(e).__name__}: {str(e)}"

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found! Please set up your .env file.")
    sys.exit(1)

client = openai.OpenAI(api_key=api_key)

print("🛡️ Safe API Caller")
print("=" * 50)
print("This handles errors gracefully!")
print("Type 'quit' to exit")
print("-" * 50)

while True:
    user_input = input("\nYour message: ").strip()
    
    if user_input.lower() == 'quit':
        break
    
    # Make safe API call
    messages = [{"role": "user", "content": user_input}]
    response, error = safe_api_call(client, messages)
    
    if error:
        print(f"\n{error}")
        print("💡 Tip: The application didn't crash! You can try again.")
    else:
        print(f"\n🤖 Response: {response}")

print("\n👋 Goodbye!")
