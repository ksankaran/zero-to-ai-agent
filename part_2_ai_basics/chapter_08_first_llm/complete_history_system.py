# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: complete_history_system.py

import openai
from pathlib import Path
from conversation_manager import ConversationManager
from searchable_history import search_conversations
from auto_summary import save_with_summary

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

# Set up
api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    exit()

client = openai.OpenAI(api_key=api_key)
manager = ConversationManager()

print("💾 Complete History System")
print("=" * 50)
print("Your conversations are automatically saved and searchable!")
print("\nCommands:")
print("  'new' - Start a new conversation")
print("  'search <term>' - Search conversation history")  
print("  'list' - Show recent conversations")
print("  'quit' - Exit and save")
print("-" * 50)

# Start first conversation
manager.start_new_conversation("Demo Chat")

while True:
    user_input = input("\nYou: ").strip()
    
    if user_input.lower() == 'quit':
        # Save before exiting
        manager.save_current_conversation()
        print("👋 All conversations saved. Goodbye!")
        break
    
    elif user_input.lower() == 'new':
        title = input("Conversation title (or Enter for default): ").strip()
        manager.start_new_conversation(title)
        continue
    
    elif user_input.lower().startswith('search '):
        search_term = user_input[7:]
        search_conversations(search_term, manager.storage_dir)
        continue
    
    elif user_input.lower() == 'list':
        files = list(manager.storage_dir.glob("conversation_*.json"))
        print(f"\n📚 You have {len(files)} saved conversations")
        for file in files[-5:]:  # Show last 5
            print(f"  • {file.name}")
        continue
    
    # Regular conversation
    manager.add_message("user", user_input)
    
    # Get AI response (simplified for demo)
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.extend(manager.current_conversation[-10:])  # Last 10 messages
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    ai_message = response.choices[0].message.content
    print(f"\nAI: {ai_message}")
    
    manager.add_message("assistant", ai_message)

print("\n✨ Thank you for using the Complete History System!")
