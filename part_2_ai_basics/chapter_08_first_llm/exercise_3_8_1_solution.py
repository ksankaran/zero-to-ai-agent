# From: Zero to AI Agent, Chapter 8, Section 8.1
# File: exercise_3_8_1_cost_calculator.py

import openai
from pathlib import Path

def load_api_key():
    """Load API key from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

def count_tokens(text, model="gpt-3.5-turbo"):
    """Count tokens in a text string"""
    # Rough estimate: ~4 characters per token
    return len(text) // 4

def calculate_cost(input_tokens, output_tokens, model="gpt-3.5-turbo"):
    """Calculate cost based on token usage"""
    # Pricing as of 2024 (per 1K tokens)
    pricing = {
        "gpt-3.5-turbo": {
            "input": 0.0005,   # $0.50 per 1M tokens
            "output": 0.0015   # $1.50 per 1M tokens
        },
        "gpt-4": {
            "input": 0.03,     # $30 per 1M tokens
            "output": 0.06     # $60 per 1M tokens
        }
    }
    
    model_pricing = pricing.get(model, pricing["gpt-3.5-turbo"])
    
    input_cost = (input_tokens / 1000) * model_pricing["input"]
    output_cost = (output_tokens / 1000) * model_pricing["output"]
    
    return input_cost + output_cost

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found! Run setup_api_key.py first!")
    exit()

client = openai.OpenAI(api_key=api_key)

print("💰 API Cost Calculator Chat!")
print("Watch your spending as you chat!")
print("Commands: 'quit', 'cost', 'reset'")
print("-" * 40)

# Cost tracking
total_cost = 0.0
total_input_tokens = 0
total_output_tokens = 0
call_count = 0
warning_shown = False

model = "gpt-3.5-turbo"
print(f"Using model: {model}")
print(f"Input cost: $0.50 per 1M tokens")
print(f"Output cost: $1.50 per 1M tokens")
print("-" * 40)

conversation = [{"role": "system", "content": "You are a helpful assistant."}]

while True:
    user_message = input("\nYou: ")
    
    if user_message.lower() == 'quit':
        break
    
    if user_message.lower() == 'cost':
        print(f"\n📊 Cost Summary:")
        print(f"  Total API calls: {call_count}")
        print(f"  Input tokens: {total_input_tokens:,}")
        print(f"  Output tokens: {total_output_tokens:,}")
        print(f"  Total cost: ${total_cost:.6f}")
        if call_count > 0:
            print(f"  Average per call: ${total_cost/call_count:.6f}")
        continue
    
    if user_message.lower() == 'reset':
        total_cost = 0.0
        total_input_tokens = 0
        total_output_tokens = 0
        call_count = 0
        warning_shown = False
        print("✨ Cost counter reset!")
        continue
    
    # Count input tokens
    conversation.append({"role": "user", "content": user_message})
    
    # Estimate tokens for the entire conversation
    full_text = " ".join([m["content"] for m in conversation])
    input_tokens = count_tokens(full_text, model)
    
    print(f"📝 Input tokens: ~{input_tokens}")
    
    # Make API call
    try:
        response = client.chat.completions.create(
            model=model,
            messages=conversation
        )
        
        ai_message = response.choices[0].message.content
        
        # Get actual token counts from response
        if response.usage:
            actual_input = response.usage.prompt_tokens
            actual_output = response.usage.completion_tokens
            actual_total = response.usage.total_tokens
        else:
            # Estimate if not provided
            actual_input = input_tokens
            actual_output = count_tokens(ai_message, model)
            actual_total = actual_input + actual_output
        
        # Calculate cost for this call
        call_cost = calculate_cost(actual_input, actual_output, model)
        
        # Update totals
        total_input_tokens += actual_input
        total_output_tokens += actual_output
        total_cost += call_cost
        call_count += 1
        
        # Show response
        print(f"\nAI: {ai_message}")
        
        # Show cost info
        print(f"\n💰 This call: {actual_total} tokens (${call_cost:.6f})")
        print(f"   Running total: ${total_cost:.6f}")
        
        # Add to conversation
        conversation.append({"role": "assistant", "content": ai_message})
        
        # Warning at $1
        if total_cost >= 1.0 and not warning_shown:
            print("\n⚠️  WARNING: You've spent over $1.00!")
            print("   Consider resetting or stopping.")
            warning_shown = True
        
        # Keep conversation manageable
        if len(conversation) > 20:
            conversation = [conversation[0]] + conversation[-19:]
        
    except Exception as e:
        print(f"❌ Error: {e}")

# Final summary
print(f"\n📊 Final Cost Summary:")
print(f"  Total API calls: {call_count}")
print(f"  Total tokens used: {total_input_tokens + total_output_tokens:,}")
print(f"  Total cost: ${total_cost:.6f}")

if total_cost > 0.01:
    print(f"\n💡 At this rate:")
    if call_count > 0:
        avg_cost = total_cost / call_count
        print(f"  100 calls would cost: ${avg_cost * 100:.2f}")
        print(f"  1000 calls would cost: ${avg_cost * 1000:.2f}")

print("\n👋 Thanks for tracking your costs!")
