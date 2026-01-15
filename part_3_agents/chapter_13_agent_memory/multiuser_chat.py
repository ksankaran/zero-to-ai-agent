# From: AI Agents Book - Chapter 13, Section 13.6
# File: multiuser_chat.py
#
# Demonstrates multi-user support with isolated memory per user.
# Each user_id (session_id) gets completely separate conversation history.
#
# Note: Uses LangChain's SQLChatMessageHistory which does not include
# timestamps. For production with retention policies, see Section 13.7.

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory


# Unique database for multi-user demo
DB_PATH = "sqlite:///multiuser.db"


def get_session_history(session_id: str):
    """Get isolated SQLite history per user.
    
    Each session_id gets completely separate conversation history.
    Users cannot see each other's messages.
    """
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=DB_PATH
    )


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Remember what each user tells you."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | ChatOpenAI(model="gpt-3.5-turbo")

chat = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


def send_message(user_id: str, message: str) -> str:
    """Send a message as a specific user."""
    config = {"configurable": {"session_id": user_id}}
    response = chat.invoke({"input": message}, config=config)
    return response.content


# Different users, different memories
if __name__ == "__main__":
    print("=" * 50)
    print("Multi-User Chat Demo")
    print("=" * 50)
    print(f"Database: {DB_PATH}")
    print()
    
    # Alice and Bob have separate memories
    print("--- Setting up preferences ---")
    print("Alice: I love Python.")
    print(f"  AI: {send_message('alice', 'I love Python.')}")
    print()
    
    print("Bob: I prefer JavaScript.")
    print(f"  AI: {send_message('bob', 'I prefer JavaScript.')}")
    print()
    
    # Each user's memory is isolated
    print("--- Testing memory isolation ---")
    print("Alice: What language do I love?")
    print(f"  AI: {send_message('alice', 'What language do I love?')}")
    print()
    
    print("Bob: What language do I prefer?")
    print(f"  AI: {send_message('bob', 'What language do I prefer?')}")
    print()
    
    print("=" * 50)
    print("Notice: Alice and Bob have separate memories!")
    print("Alice knows about Python, Bob knows about JavaScript.")
    print("=" * 50)