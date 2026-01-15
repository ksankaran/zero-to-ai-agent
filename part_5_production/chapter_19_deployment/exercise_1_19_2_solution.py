# From: Zero to AI Agent, Chapter 19, Section 19.2
# File: exercise_1_19_2_solution.py
# Exercise 1: Add Conversations Endpoint

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Optional, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
import operator
import uuid
import time
import logging
import os

# Load environment variables
load_dotenv()

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
API_KEY = os.getenv("API_KEY", "dev-key-change-in-production")

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    processing_time_ms: int

class MessageOut(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ConversationDetail(BaseModel):
    conversation_id: str
    messages: List[MessageOut]
    message_count: int

class ConversationList(BaseModel):
    conversations: List[str]
    count: int

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

# --- Security ---
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: Optional[str] = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key

# --- API Setup ---
app = FastAPI(title="Agent API with Conversations", version="1.0.0")
agent = create_agent()

# Track conversation IDs (in production, use a database)
conversation_ids: set[str] = set()

# --- Endpoints ---
@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """Send a message to the agent and receive a response."""
    start_time = time.time()
    
    conv_id = request.conversation_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": conv_id}}
    
    # Track this conversation ID
    conversation_ids.add(conv_id)
    
    logger.info(f"Processing request for conversation {conv_id}")
    
    try:
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config
        )
        
        ai_response = result["messages"][-1].content
        processing_time = int((time.time() - start_time) * 1000)
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conv_id,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="An error occurred")

@app.get("/v1/conversations", response_model=ConversationList)
async def list_conversations(api_key: str = Depends(verify_api_key)):
    """List all conversation IDs."""
    return ConversationList(
        conversations=list(conversation_ids),
        count=len(conversation_ids)
    )

@app.get("/v1/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get all messages for a specific conversation."""
    if conversation_id not in conversation_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Conversation {conversation_id} not found"
        )
    
    # Get state from checkpointer
    config = {"configurable": {"thread_id": conversation_id}}
    state = agent.get_state(config)
    
    if not state.values or "messages" not in state.values:
        raise HTTPException(
            status_code=404,
            detail=f"No messages found for conversation {conversation_id}"
        )
    
    # Convert LangChain messages to our output format
    messages_out = []
    for msg in state.values["messages"]:
        if hasattr(msg, 'content'):
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            messages_out.append(MessageOut(role=role, content=msg.content))
    
    return ConversationDetail(
        conversation_id=conversation_id,
        messages=messages_out,
        message_count=len(messages_out)
    )

@app.get("/health")
def health():
    return {"status": "healthy"}
