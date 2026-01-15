# From: AI Agents Book - Chapter 13, Section 13.2
# File: exercise_1_13_2_solution.py
# Exercise: Basic Memory Implementation

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

# Initialize
client = OpenAI()
conversation_history = []

# Add system prompt
conversation_history.append({
    "role": "system",
    "content": "You are a helpful math tutor."
})

def chat(user_message):
    # Add user message
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Make API call with full history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    
    # Store assistant response
    assistant_message = response.choices[0].message.content
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    # Print message count
    print(f"[Total messages: {len(conversation_history)}]")
    
    return assistant_message

# Test the conversation
print("User: What is 5 + 3?")
print(f"Assistant: {chat('What is 5 + 3?')}\n")

print("User: Now multiply that by 2")
print(f"Assistant: {chat('Now multiply that by 2')}\n")

print("User: What were we calculating?")
print(f"Assistant: {chat('What were we calculating?')}\n")
