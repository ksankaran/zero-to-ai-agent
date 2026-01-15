# From: AI Agents Book - Chapter 13, Section 13.2
# File: no_memory_demo.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()

def chat(user_message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

# Conversation attempt
print(chat("Hi! My name is Alex."))
# "Hello Alex! Nice to meet you!"

print(chat("What's my name?"))
# "I don't know your name. Could you tell me?"
