# From: Zero to AI Agent, Chapter 8, Section 8.2
# File: mini_chatgpt.py

import openai
from pathlib import Path
import json
from datetime import datetime
import sys

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

class MiniChatGPT:
    """Your own mini version of ChatGPT!"""
    
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.conversations = {}  # Multiple conversation threads
        self.current_conversation_id = None
        self.settings = {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 500,
            "stream": True
        }
    
    def new_conversation(self, title=None):
        """Start a new conversation thread"""
        conv_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        title = title or f"Chat {conv_id}"
        
        self.conversations[conv_id] = {
            "id": conv_id,
            "title": title,
            "messages": [],
            "created": datetime.now().isoformat(),
            "token_count": 0,
            "cost": 0.0
        }
        
        self.current_conversation_id = conv_id
        return conv_id
    
    def list_conversations(self):
        """List all conversations"""
        if not self.conversations:
            print("No conversations yet.")
            return
        
        print("\n📚 Your Conversations:")
        for i, (conv_id, conv) in enumerate(self.conversations.items(), 1):
            msg_count = len(conv["messages"])
            print(f"  {i}. {conv['title']} ({msg_count} messages)")
            if conv_id == self.current_conversation_id:
                print("     ^ Current")
    
    def switch_conversation(self, conv_id):
        """Switch to a different conversation"""
        if conv_id in self.conversations:
            self.current_conversation_id = conv_id
            print(f"Switched to: {self.conversations[conv_id]['title']}")
            return True
        return False
    
    def get_current_messages(self):
        """Get messages for current conversation"""
        if not self.current_conversation_id:
            self.new_conversation()
        
        conv = self.conversations[self.current_conversation_id]
        
        # System message + conversation history
        messages = [
            {"role": "system", "content": "You are ChatGPT, a helpful AI assistant."}
        ]
        
        # Add conversation messages (limit to last 20 for token management)
        for msg in conv["messages"][-20:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return messages
    
    def chat(self, user_message):
        """Send message and get response"""
        if not self.current_conversation_id:
            self.new_conversation()
        
        conv = self.conversations[self.current_conversation_id]
        
        # Add user message
        conv["messages"].append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get messages for API
        messages = self.get_current_messages()
        
        print("\n🤖 ChatGPT: ", end="", flush=True)
        
        full_response = ""
        
        try:
            if self.settings["stream"]:
                # Streaming response
                stream = self.client.chat.completions.create(
                    model=self.settings["model"],
                    messages=messages,
                    temperature=self.settings["temperature"],
                    max_tokens=self.settings["max_tokens"],
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        print(content, end="", flush=True)
                        full_response += content
                
            else:
                # Non-streaming response
                response = self.client.chat.completions.create(
                    model=self.settings["model"],
                    messages=messages,
                    temperature=self.settings["temperature"],
                    max_tokens=self.settings["max_tokens"]
                )
                
                full_response = response.choices[0].message.content
                print(full_response)
                
                # Track usage
                if response.usage:
                    conv["token_count"] += response.usage.total_tokens
                    conv["cost"] += (response.usage.total_tokens / 1000) * 0.002
            
            print()  # New line
            
            # Add assistant response
            conv["messages"].append({
                "role": "assistant",
                "content": full_response,
                "timestamp": datetime.now().isoformat()
            })
            
            return full_response
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None
    
    def save_all_conversations(self):
        """Save all conversations to file"""
        filename = f"conversations_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.conversations, f, indent=2)
        
        print(f"💾 Saved all conversations to {filename}")
    
    def show_settings(self):
        """Show current settings"""
        print("\n⚙️ Current Settings:")
        for key, value in self.settings.items():
            print(f"  {key}: {value}")
    
    def change_setting(self, key, value):
        """Change a setting"""
        if key in self.settings:
            old_value = self.settings[key]
            self.settings[key] = value
            print(f"✅ Changed {key}: {old_value} → {value}")
        else:
            print(f"❌ Unknown setting: {key}")
    
    def show_help(self):
        """Show available commands"""
        print("\n📖 Available Commands:")
        print("  'new' - Start new conversation")
        print("  'list' - List all conversations")
        print("  'switch' - Switch to another conversation")
        print("  'settings' - Show current settings")
        print("  'temp <value>' - Change temperature (0-2)")
        print("  'model <name>' - Change model")
        print("  'save' - Save all conversations")
        print("  'help' - Show this help")
        print("  'quit' - Exit")
    
    def run(self):
        """Run the ChatGPT clone"""
        print("🚀 Mini ChatGPT")
        print("=" * 60)
        print("Welcome to your own ChatGPT clone!")
        print("Type 'help' for commands or just start chatting!")
        print("=" * 60)
        
        # Start first conversation
        self.new_conversation("Welcome Chat")
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                if user_input.lower() == 'quit':
                    print("\n👋 Goodbye!")
                    break
                
                elif user_input.lower() == 'help':
                    self.show_help()
                
                elif user_input.lower() == 'new':
                    title = input("Conversation title (or Enter for default): ").strip()
                    conv_id = self.new_conversation(title)
                    print(f"✨ Started new conversation: {self.conversations[conv_id]['title']}")
                
                elif user_input.lower() == 'list':
                    self.list_conversations()
                
                elif user_input.lower() == 'switch':
                    self.list_conversations()
                    choice = input("Choose conversation number: ").strip()
                    try:
                        idx = int(choice) - 1
                        conv_list = list(self.conversations.keys())
                        if 0 <= idx < len(conv_list):
                            self.switch_conversation(conv_list[idx])
                    except:
                        print("Invalid choice")
                
                elif user_input.lower() == 'settings':
                    self.show_settings()
                
                elif user_input.lower().startswith('temp '):
                    try:
                        temp = float(user_input.split()[1])
                        if 0 <= temp <= 2:
                            self.change_setting('temperature', temp)
                        else:
                            print("Temperature must be between 0 and 2")
                    except:
                        print("Invalid temperature value")
                
                elif user_input.lower().startswith('model '):
                    model = user_input[6:].strip()
                    self.change_setting('model', model)
                
                elif user_input.lower() == 'save':
                    self.save_all_conversations()
                
                else:
                    # Regular chat message
                    self.chat(user_input)
                    
            except KeyboardInterrupt:
                print("\n⚠️ Interrupted! Type 'quit' to exit.")
            except Exception as e:
                print(f"\n❌ Error: {e}")

# Run Mini ChatGPT!
if __name__ == "__main__":
    api_key = load_api_key()
    if not api_key:
        print("❌ No API key found! Run setup_api_key.py first!")
        exit()
    
    chatgpt = MiniChatGPT(api_key)
    chatgpt.run()
