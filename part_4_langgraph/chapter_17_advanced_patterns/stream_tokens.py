# From: Zero to AI Agent, Chapter 17, Section 17.2
# Save as: stream_tokens.py

import asyncio
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, streaming=True)

async def chat_node(state: ChatState) -> dict:
    """Generate a response to the user's message."""
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}

def build_chat_graph():
    workflow = StateGraph(ChatState)
    workflow.add_node("chat", chat_node)
    workflow.add_edge(START, "chat")
    workflow.add_edge("chat", END)
    return workflow.compile()

async def chat_with_streaming(user_message: str):
    """Chat with token-by-token streaming."""
    
    graph = build_chat_graph()
    
    initial_state = {
        "messages": [{"role": "user", "content": user_message}]
    }
    
    print(f"You: {user_message}")
    print("AI: ", end="", flush=True)
    
    # astream_events gives us fine-grained events including tokens
    async for event in graph.astream_events(initial_state, version="v2"):
        # We're looking for chat model stream events
        if event["event"] == "on_chat_model_stream":
            # Extract the token content
            chunk = event["data"]["chunk"]
            if hasattr(chunk, "content") and chunk.content:
                print(chunk.content, end="", flush=True)
    
    print()  # New line after response

async def main():
    print("💬 Streaming Chat Demo")
    print("=" * 50)
    
    await chat_with_streaming("Explain quantum computing in simple terms.")
    print()
    await chat_with_streaming("What are its practical applications?")

if __name__ == "__main__":
    asyncio.run(main())
