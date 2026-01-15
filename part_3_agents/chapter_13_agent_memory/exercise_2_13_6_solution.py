# From: AI Agents Book - Chapter 13, Section 13.6
# File: exercise_2_13_6_solution.py
# Exercise: Windowed Memory with trim_messages

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import trim_messages
from langchain_community.chat_message_histories import ChatMessageHistory

store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# Create trimmer with ~100 tokens limit
trimmer = trim_messages(
    max_tokens=100,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-3.5-turbo"),
    include_system=True,
    start_on="human"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful. Remember details the user shares."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

llm = ChatOpenAI(model="gpt-3.5-turbo")


# Function to trim history within the chain
def trim_history(input_dict):
    """Apply trimmer to history messages only."""
    history = input_dict.get("history", [])
    trimmed = trimmer.invoke(history)
    return {**input_dict, "history": trimmed}


# Build chain: trim history -> prompt -> llm
chain = RunnableLambda(trim_history) | prompt | llm

chat = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

config = {"configurable": {"session_id": "window"}}

# 6-message conversation - early messages should be forgotten
messages = [
    "My name is Alex.",              # Should be forgotten
    "I live in Boston.",             # Should be forgotten  
    "I have a cat named Whiskers.",  # Should be forgotten
    "I work at a tech startup.",
    "My favorite food is pizza.",
    "What do you remember about me?"
]

print("=" * 50)
print("Windowed Memory Demo (100 token limit)")
print("=" * 50)

for msg in messages:
    print(f"\nHuman: {msg}")
    response = chat.invoke({"input": msg}, config=config)
    print(f"AI: {response.content}")

print("\n" + "=" * 50)
print("Expected behavior:")
print("- Bot should NOT remember: name, city, cat (trimmed away)")
print("- Bot SHOULD remember: job, favorite food (recent enough)")
print("=" * 50)