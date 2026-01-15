# From: Zero to AI Agent, Chapter 5, Section 5.3
# File: ai_preview.py

def preprocess_text(text):
    """Prepare text for AI processing"""
    # Remove extra spaces
    text = " ".join(text.split())
    # Convert to lowercase for consistency
    text = text.lower()
    # Remove special characters (simplified)
    cleaned = ''.join(c for c in text if c.isalnum() or c.isspace())
    return cleaned  # Return cleaned text for AI

def get_ai_response(prompt):
    """Simulate getting response from AI"""
    # In later chapters, this will actually call an AI API!
    # For now, we'll simulate
    responses = {
        "hello": "Hi there! How can I help you?",
        "weather": "I'd need to check current data for weather info.",
        "python": "Python is a great programming language!"
    }
    
    # Simple keyword matching (real AI is much smarter!)
    for keyword, response in responses.items():
        if keyword in prompt.lower():
            return response  # Return the matched response
    
    return "I'm not sure how to respond to that."  # Default return

def format_conversation(user_input, ai_response):
    """Format the conversation nicely"""
    formatted = f"""
    USER: {user_input}
    AI: {ai_response}
    """
    return formatted  # Return formatted string

# Chain everything together
user_text = "Tell me about Python programming"
clean_text = preprocess_text(user_text)
response = get_ai_response(clean_text)
conversation = format_conversation(user_text, response)
print(conversation)