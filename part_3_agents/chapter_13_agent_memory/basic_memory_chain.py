# From: AI Agents Book - Chapter 13, Section 13.6
# File: basic_memory_chain.py

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Store for session histories (in production, use a database)
store = {}


def get_session_history(session_id: str):
    """Retrieve or create history for a session."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# Create the prompt with a placeholder for history
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Create the chain
llm = ChatOpenAI(model="gpt-3.5-turbo")
chain = prompt | llm

# Wrap with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use it with a session ID
config = {"configurable": {"session_id": "user_123"}}

response1 = chain_with_history.invoke(
    {"input": "Hi! My name is Alice."},
    config=config
)
print(response1.content)

response2 = chain_with_history.invoke(
    {"input": "What's my name?"},
    config=config
)
print(response2.content)  # It remembers Alice!
