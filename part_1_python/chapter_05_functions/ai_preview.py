# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: ai_preview.py

def generate_ai_response(prompt, temperature=0.7, max_tokens=150, model="gpt-3.5"):
    """
    Simulate an AI API call (we'll make this real in later chapters!)
    
    Parameters:
    - prompt: The user's input text
    - temperature: Creativity level (0=focused, 1=creative)
    - max_tokens: Maximum response length
    - model: Which AI model to use
    """
    print("🤖 AI Request:")
    print(f"  Prompt: '{prompt}'")
    print(f"  Temperature: {temperature}")
    print(f"  Max tokens: {max_tokens}")
    print(f"  Model: {model}")
    print("\n🔄 Processing... (in later chapters, this will call real AI!)")
    
    # For now, just a placeholder response
    if temperature < 0.5:
        response = "I understand your request. [Focused response]"
    else:
        response = "What an interesting question! [Creative response]"
    
    print(f"\n💬 AI Response: {response}")
    return response

# Different AI behaviors with parameters
generate_ai_response("Tell me a story", temperature=0.9)  # Creative mode
print("\n" + "="*50 + "\n")
generate_ai_response("Explain Python functions", temperature=0.2)  # Focused mode
print("\n" + "="*50 + "\n")
generate_ai_response("Write a poem", temperature=0.8, max_tokens=200)
