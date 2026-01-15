# From: Zero to AI Agent, Chapter 17, Section 17.2
# Save as: streaming_chat.py

import asyncio
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

class ConversationState(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, streaming=True)

async def respond(state: ConversationState) -> dict:
    """Generate a response."""
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}

def build_conversation_graph():
    workflow = StateGraph(ConversationState)
    workflow.add_node("respond", respond)
    workflow.add_edge(START, "respond")
    workflow.add_edge("respond", END)
    return workflow.compile()

async def stream_response(graph, messages: list) -> str:
    """Stream a response and return the complete text."""
    
    full_response = ""
    
    async for event in graph.astream_events(
        {"messages": messages}, 
        version="v2"
    ):
        if event["event"] == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if hasattr(chunk, "content") and chunk.content:
                print(chunk.content, end="", flush=True)
                full_response += chunk.content
    
    print()  # New line
    return full_response

async def chat_loop():
    """Interactive chat with streaming responses."""
    
    graph = build_conversation_graph()
    messages = []
    
    print("💬 Streaming Chat")
    print("=" * 50)
    print("Type 'quit' to exit, 'clear' to reset conversation")
    print("=" * 50)
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == 'clear':
            messages = []
            print("🔄 Conversation cleared!")
            continue
        
        if not user_input:
            continue
        
        # Add user message to history
        messages.append({"role": "user", "content": user_input})
        
        # Stream the response
        print("AI: ", end="", flush=True)
        response = await stream_response(graph, messages)
        
        # Add AI response to history
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    asyncio.run(chat_loop())
