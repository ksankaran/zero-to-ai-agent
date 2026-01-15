# From: AI Agents Book - Chapter 13, Section 13.6
# File: exercise_1_13_6_solution.py
# Exercise: Basic Chat with Memory

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are friendly."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | ChatOpenAI(model="gpt-3.5-turbo")

chat = RunnableWithMessageHistory(
    chain, get_session_history,
    input_messages_key="input", history_messages_key="history"
)

config = {"configurable": {"session_id": "demo"}}

# 3-message conversation
for msg in ["Hi! My name is Sarah.", "I'm an engineer.", "What's my name and job?"]:
    print(f"Human: {msg}")
    response = chat.invoke({"input": msg}, config=config)
    print(f"AI: {response.content}\n")

# Print full history
print("--- Full History ---")
for msg in store["demo"].messages:
    print(f"{msg.type}: {msg.content[:50]}...")
