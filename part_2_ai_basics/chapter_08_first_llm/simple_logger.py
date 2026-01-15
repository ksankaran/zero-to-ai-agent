# From: Zero to AI Agent, Chapter 8, Section 8.3
# File: simple_logger.py

import openai
import json
from pathlib import Path
from datetime import datetime

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

def log_response(prompt, response):
    """Log response details to a file"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response.choices[0].message.content,
        "model": response.model,
        "tokens": {
            "prompt": response.usage.prompt_tokens,
            "completion": response.usage.completion_tokens,
            "total": response.usage.total_tokens
        },
        "finish_reason": response.choices[0].finish_reason,
        "cost_estimate": response.usage.total_tokens * 0.002 / 1000
    }
    
    # Append to log file
    log_file = "api_responses.json"
    
    # Load existing logs
    if Path(log_file).exists():
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    # Add new entry
    logs.append(log_entry)
    
    # Save
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"📝 Logged response to {log_file}")
    return log_entry

# Setup
api_key = load_api_key()
client = openai.OpenAI(api_key=api_key)

print("📊 Response Logger")
print("Type your prompts and I'll log all the details!")
print("Type 'quit' to exit, 'stats' to see statistics")
print("=" * 50)

while True:
    user_input = input("\nYour prompt: ").strip()
    
    if user_input.lower() == 'quit':
        break
    
    if user_input.lower() == 'stats':
        # Show statistics from log
        if Path("api_responses.json").exists():
            with open("api_responses.json", 'r') as f:
                logs = json.load(f)
            
            total_tokens = sum(log['tokens']['total'] for log in logs)
            total_cost = sum(log['cost_estimate'] for log in logs)
            
            print(f"\n📈 Statistics from {len(logs)} requests:")
            print(f"  Total tokens: {total_tokens:,}")
            print(f"  Total cost: ${total_cost:.6f}")
            print(f"  Average per request: ${total_cost/len(logs):.6f}")
        else:
            print("No logs yet!")
        continue
    
    # Make API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    
    # Show response
    print(f"\n🤖 Response: {response.choices[0].message.content}")
    
    # Log it
    log_entry = log_response(user_input, response)
    print(f"📊 Used {log_entry['tokens']['total']} tokens (${log_entry['cost_estimate']:.6f})")

print("\n👋 Check api_responses.json for your logged data!")
