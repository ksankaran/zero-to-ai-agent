# From: AI Agents Book - Chapter 13, Section 13.6
# File: trimmed_memory.py
#
# Demonstrates using trim_messages to limit conversation history size.
# This prevents context window overflow in long conversations.

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import trim_messages
from langchain_community.chat_message_histories import ChatMessageHistory

store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# Create a message trimmer
trimmer = trim_messages(
    max_tokens=200,  # Keep roughly this many tokens
    strategy="last",  # Keep the most recent messages
    token_counter=ChatOpenAI(model="gpt-3.5-turbo"),  # Use LLM to count
    include_system=True,  # Always keep system message
    start_on="human",  # Start sequence on human message
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Remember details users share with you."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

llm = ChatOpenAI(model="gpt-3.5-turbo")


# Use RunnablePassthrough.assign to trim history before passing to prompt
chain = (
    RunnablePassthrough.assign(
        history=lambda x: trimmer.invoke(x.get("history", []))
    )
    | prompt
    | llm
)

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


def chat(message: str, session_id: str = "user_456") -> str:
    """Send a message and get a response."""
    config = {"configurable": {"session_id": session_id}}
    response = chain_with_history.invoke({"input": message}, config=config)
    return response.content


# Long conversation - older messages will be trimmed
if __name__ == "__main__":
    messages = [
        "My name is Bob.",
        "I live in Seattle.",
        "I work as a data scientist.",
        "My favorite language is Python.",
        "I have a dog named Max.",
        "I enjoy hiking on weekends.",
        "What do you remember about me?"
    ]
    
    print("=" * 50)
    print("Trimmed Memory Demo (200 token limit)")
    print("=" * 50)
    print()
    
    for msg in messages:
        print(f"Human: {msg}")
        response = chat(msg)
        print(f"AI: {response}")
        print()
    
    print("=" * 50)
    print("With only ~200 tokens, early messages get trimmed.")
    print("The bot may not remember name/city from the start.")
    print("=" * 50)