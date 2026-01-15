# From: AI Agents Book - Chapter 13, Section 13.6
# File: persistent_sqlite.py
#
# IMPORTANT: This uses LangChain's built-in SQLChatMessageHistory, which
# creates a schema WITHOUT timestamps. For retention policies and cleanup
# that require timestamps, see retention_policy.py and production_memory_manager.py
# which use a custom schema.
#
# The SQLChatMessageHistory schema:
#   - id (INTEGER PRIMARY KEY)
#   - session_id (TEXT)
#   - message (TEXT - JSON blob)
#
# For timestamp-based retention, use the custom schema in Section 13.7 files.

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory


# Use a unique database name to avoid conflicts with other examples
DB_PATH = "sqlite:///langchain_chat.db"


def get_session_history(session_id: str):
    """Get SQLite-backed message history.
    
    Note: LangChain's SQLChatMessageHistory does not store timestamps.
    For production use with retention policies, consider using a custom
    schema (see retention_policy.py).
    """
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=DB_PATH
    )


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Remember what the user tells you."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | ChatOpenAI(model="gpt-3.5-turbo")

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


def chat(session_id: str, message: str) -> str:
    """Send a message and get a response."""
    config = {"configurable": {"session_id": session_id}}
    response = chain_with_history.invoke({"input": message}, config=config)
    return response.content


if __name__ == "__main__":
    print("=" * 50)
    print("Persistent SQLite Memory Demo")
    print("=" * 50)
    print(f"Database: {DB_PATH}")
    print()
    
    # First interaction
    print("Human: My favorite color is blue.")
    response = chat("alice_session", "My favorite color is blue.")
    print(f"AI: {response}")
    print()
    
    # Second interaction - should remember
    print("Human: What's my favorite color?")
    response = chat("alice_session", "What's my favorite color?")
    print(f"AI: {response}")
    print()
    
    print("=" * 50)
    print("Try stopping and restarting this script.")
    print("The memory will persist in langchain_chat.db!")
    print("=" * 50)