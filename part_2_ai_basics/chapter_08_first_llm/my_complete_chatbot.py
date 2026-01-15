# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: my_complete_chatbot.py

import openai
from pathlib import Path
import json
from datetime import datetime

def load_api_key():
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

print("🤖 Your Complete Chatbot")
print("=" * 50)
print("Features:")
print("  • Adjustable temperature (creative vs focused)")
print("  • Streaming responses")
print("  • Conversation memory")
print("  • Save conversations")
print("\nCommands: 'quit', 'save', 'temp <value>', 'clear'")
print("=" * 50)

# Settings
temperature = 0.7
conversation = [{"role": "system", "content": "You are a helpful, friendly assistant."}]

while True:
    user_input = input("\nYou: ").strip()
    
    # Handle commands
    if user_input.lower() == 'quit':
        print("👋 Goodbye!")
        break
    
    elif user_input.lower() == 'clear':
        conversation = [conversation[0]]  # Keep only system message
        print("🧹 Conversation cleared!")
        continue
    
    elif user_input.lower() == 'save':
        # Save conversation to file
        filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump({
                "conversation": conversation,
                "temperature": temperature,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        print(f"💾 Saved to {filename}")
        continue
    
    elif user_input.lower().startswith('temp '):
        # Change temperature
        try:
            new_temp = float(user_input.split()[1])
            if 0 <= new_temp <= 2:
                temperature = new_temp
                print(f"🌡️ Temperature set to {temperature}")
            else:
                print("Temperature must be between 0 and 2")
        except:
            print("Invalid temperature")
        continue
    
    # Regular chat message
    if user_input:
        # Add to conversation
        conversation.append({"role": "user", "content": user_input})
        
        # Keep conversation manageable (max 20 messages)
        if len(conversation) > 20:
            conversation = [conversation[0]] + conversation[-19:]
        
        print("\nAI: ", end="", flush=True)
        
        try:
            # Stream the response
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=temperature,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            
            print()  # New line
            
            # Add AI response to conversation
            conversation.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

print("\n🎉 Thanks for using your complete chatbot!")
