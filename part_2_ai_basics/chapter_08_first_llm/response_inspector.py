# From: Zero to AI Agent, Chapter 8, Section 8.3
# File: response_inspector.py

# Simple tools to understand API responses

def inspect_response(response):
    """Print all the interesting parts of a response"""
    print("\n🔍 Response Inspector")
    print("=" * 50)
    
    # Basic info
    print(f"Response ID: {response.id}")
    print(f"Model: {response.model}")
    print(f"Created: {response.created}")
    
    # The actual message
    if response.choices:
        message = response.choices[0].message.content
        print(f"\nMessage: {message[:100]}...")
        print(f"Finish reason: {response.choices[0].finish_reason}")
    
    # Token usage
    if hasattr(response, 'usage') and response.usage:
        print(f"\n📊 Token Usage:")
        print(f"  Prompt: {response.usage.prompt_tokens}")
        print(f"  Response: {response.usage.completion_tokens}")
        print(f"  Total: {response.usage.total_tokens}")
    
    print("=" * 50)

def calculate_simple_cost(tokens, model="gpt-3.5-turbo"):
    """Simple cost calculator"""
    # Rough pricing (as of 2024)
    if model == "gpt-3.5-turbo":
        return tokens * 0.002 / 1000  # $0.002 per 1K tokens
    elif model == "gpt-4":
        return tokens * 0.03 / 1000   # $0.03 per 1K tokens
    return 0
