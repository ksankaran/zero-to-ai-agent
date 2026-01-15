# From: AI Agents Book - Chapter 13, Section 13.3
# File: exercise_1_13_3_solution.py
# Exercise: Basic Summarization

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI()

def summarize_messages(messages):
    """
    Summarize a list of conversation messages.
    
    Args:
        messages: List of dicts with 'role' and 'content' keys
    
    Returns:
        Summary string
    """
    # Format messages into readable text
    formatted = ""
    for msg in messages:
        role = msg["role"].upper()
        formatted += f"{role}: {msg['content']}\n\n"
    
    # Generate summary using LLM
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"""Summarize this conversation, preserving key facts, 
decisions, and important context:

{formatted}

Provide a concise summary:"""
        }],
        max_tokens=300
    )
    
    return response.choices[0].message.content


# Test with vacation planning conversation
test_messages = [
    {"role": "user", "content": "I want to plan a vacation to Italy in June."},
    {"role": "assistant", "content": "Italy in June is wonderful! Are you interested in cities like Rome and Florence, or coastal areas like the Amalfi Coast?"},
    {"role": "user", "content": "I'd love to see Rome and maybe some coastal areas too. I have about 10 days and a budget of $3000."},
    {"role": "assistant", "content": "With 10 days and $3000, I'd suggest 4 days in Rome, 3 days on the Amalfi Coast, and 3 days in Florence. Shall I break down the budget?"},
    {"role": "user", "content": "Yes please! Also, I'm vegetarian so I hope that won't be a problem."}
]

summary = summarize_messages(test_messages)
print("GENERATED SUMMARY:")
print("-" * 40)
print(summary)
