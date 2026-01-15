# From: Zero to AI Agent, Chapter 11, Section 11.3
# File: few_shot_prompt.py

from langchain_core.prompts import ChatPromptTemplate

# Teaching by example
examples = [
    {"input": "happy", "output": "😊"},
    {"input": "sad", "output": "😢"},
    {"input": "love", "output": "❤️"}
]

# Build the teaching prompt
messages = [
    ("system", "Convert words to emojis. Learn from these examples:"),
    ("human", "happy"),
    ("assistant", "😊"),
    ("human", "sad"), 
    ("assistant", "😢"),
    ("human", "love"),
    ("assistant", "❤️"),
    ("human", "{word}")  # The actual input
]

prompt = ChatPromptTemplate.from_messages(messages)

# Test it
test_prompt = prompt.format_messages(word="excited")
print(test_prompt[-1])  # Just show the last message
