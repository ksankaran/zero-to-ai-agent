# From: Zero to AI Agent, Chapter 19, Section 19.2
# File: agent_api.py

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
import operator
import uuid

# Load environment variables
load_dotenv()

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# --- Agent Setup ---
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

def process_message(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def create_agent():
    graph = StateGraph(AgentState)
    graph.add_node("process", process_message)
    graph.add_edge(START, "process")
    graph.add_edge("process", END)
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)

# --- API Setup ---
app = FastAPI(
    title="My Agent API",
    description="A conversational agent with memory",
    version="1.0.0"
)

agent = create_agent()

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Use conversation_id as thread_id for the checkpointer
    conv_id = request.conversation_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": conv_id}}
    
    # Run the agent with the new message
    result = agent.invoke(
        {"messages": [HumanMessage(content=request.message)]},
        config=config
    )
    
    # Get the last message (the AI response)
    ai_response = result["messages"][-1].content
    
    return ChatResponse(
        response=ai_response,
        conversation_id=conv_id
    )

@app.get("/health")
def health():
    return {"status": "healthy"}
