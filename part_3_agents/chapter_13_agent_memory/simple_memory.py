# From: AI Agents Book - Chapter 13, Section 13.2
# File: simple_memory.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()
conversation_history = []

def chat(user_message):
    # Add the user's message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # Send entire history to the API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    
    # Extract and store the assistant's reply
    assistant_message = response.choices[0].message.content
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

# Now let's try again
print(chat("Hi! My name is Alex."))
# "Hello Alex! Nice to meet you! How can I help you today?"

print(chat("What's my name?"))
# "Your name is Alex!"
