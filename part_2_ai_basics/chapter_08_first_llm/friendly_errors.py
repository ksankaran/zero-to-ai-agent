# From: Zero to AI Agent, Chapter 8, Section 8.4
# File: friendly_errors.py

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

def friendly_error_message(error):
    """Convert technical errors into user-friendly messages"""
    
    error_type = type(error).__name__
    
    friendly_messages = {
        'AuthenticationError': {
            'message': "🔑 There's an issue with the API key.",
            'suggestion': "Please check that your API key is valid and properly set up.",
            'action': "Visit https://platform.openai.com/api-keys to verify your key."
        },
        'RateLimitError': {
            'message': "⏳ We're sending too many requests too quickly.",
            'suggestion': "Please wait a moment before trying again.",
            'action': "Try again in about 60 seconds, or upgrade your API plan for higher limits."
        },
        'BadRequestError': {
            'message': "❌ The request couldn't be processed.",
            'suggestion': "There might be an issue with the message format.",
            'action': "Try rephrasing your message or making it shorter."
        },
        'APIConnectionError': {
            'message': "🌐 Can't connect to the AI service.",
            'suggestion': "Please check your internet connection.",
            'action': "Make sure you're connected to the internet and try again."
        },
        'APITimeoutError': {
            'message': "⏱️ The request took too long.",
            'suggestion': "The service might be busy right now.",
            'action': "Try again in a moment, or try a simpler request."
        },
        'ServiceUnavailableError': {
            'message': "🔧 The AI service is temporarily unavailable.",
            'suggestion': "OpenAI's servers might be under maintenance.",
            'action': "Please try again in a few minutes."
        }
    }
    
    # Get friendly message or default
    if error_type in friendly_messages:
        return friendly_messages[error_type]
    else:
        return {
            'message': f"😕 An unexpected error occurred.",
            'suggestion': f"Error type: {error_type}",
            'action': "Try again, or contact support if the problem persists."
        }

def make_safe_request(client, messages):
    """Make a request with friendly error handling"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content, None
    
    except Exception as e:
        return None, friendly_error_message(e)

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    print("💡 Please create a .env file with your OpenAI API key.")
    print("📝 Format: OPENAI_API_KEY=sk-...")
    exit()

client = openai.OpenAI(api_key=api_key)

print("😊 Friendly Error Handler")
print("=" * 50)
print("All errors are explained in a helpful way!")
print("Commands: 'test_error', 'quit'")
print("-" * 50)

while True:
    user_input = input("\nYour message: ").strip()
    
    if user_input.lower() == 'quit':
        break
    
    elif user_input.lower() == 'test_error':
        # Intentionally trigger different errors for testing
        print("\n🧪 Testing error messages...")
        
        # Test with bad model
        try:
            client.chat.completions.create(
                model="gpt-99",
                messages=[{"role": "user", "content": "Hi"}]
            )
        except Exception as e:
            error_info = friendly_error_message(e)
            print(f"\n{error_info['message']}")
            print(f"💡 {error_info['suggestion']}")
            print(f"➡️ {error_info['action']}")
        continue
    
    # Normal request
    messages = [{"role": "user", "content": user_input}]
    response, error_info = make_safe_request(client, messages)
    
    if response:
        print(f"\n🤖 {response}")
    else:
        print(f"\n{error_info['message']}")
        print(f"💡 {error_info['suggestion']}")
        print(f"➡️ {error_info['action']}")

print("\n👋 Thanks for chatting!")
