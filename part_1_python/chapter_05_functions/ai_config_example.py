# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: ai_config_example.py

# Global configuration constants
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 150

# Global state (use sparingly!)
api_calls_made = 0

def create_ai_config(model=None, temperature=None, max_tokens=None):
    """Create configuration with defaults"""
    # Use provided values or defaults
    config = {
        "model": model if model else DEFAULT_MODEL,
        "temperature": temperature if temperature is not None else DEFAULT_TEMPERATURE,
        "max_tokens": max_tokens if max_tokens else DEFAULT_MAX_TOKENS
    }
    return config

def make_api_call(prompt, config=None):
    """Simulate API call with configuration"""
    global api_calls_made  # We want to track total calls
    
    # Use provided config or create default
    if config is None:
        config = create_ai_config()
    
    api_calls_made += 1
    
    # Simulate processing
    response = f"Response to '{prompt}' using {config['model']}"
    
    # Local variable for this call's details
    call_details = {
        "prompt": prompt,
        "config": config,
        "response": response,
        "call_number": api_calls_made
    }
    
    return call_details

# Make some API calls
result1 = make_api_call("Hello, AI!")
print(f"Call #{result1['call_number']}: {result1['response']}")

custom_config = create_ai_config(model="gpt-4", temperature=0.9)
result2 = make_api_call("Write a poem", custom_config)
print(f"Call #{result2['call_number']}: {result2['response']}")

print(f"\nTotal API calls made: {api_calls_made}")