# From: Zero to AI Agent, Chapter 19, Section 19.2
# File: production_api.py

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Optional
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

class HealthResponse(BaseModel):
    status: str
    version: str

# --- Agent Setup ---
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

def process_message(state: AgentState) -> AgentState:
    """Process the conversation and generate a response."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def create_agent():
    """Create the agent with a checkpointer for conversation persistence."""
    graph = StateGraph(AgentState)
    graph.add_node("process", process_message)
    graph.add_edge(START, "process")
    graph.add_edge("process", END)
    
    # MemorySaver for development
    # For production, use PostgresSaver:
    # from langgraph.checkpoint.postgres import PostgresSaver
    # checkpointer = PostgresSaver.from_conn_string(os.getenv("DATABASE_URL"))
    checkpointer = MemorySaver()
    
    return graph.compile(checkpointer=checkpointer)

# --- Security ---
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: Optional[str] = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key

# --- API Setup ---
app = FastAPI(
    title="Production Agent API",
    description="A production-ready conversational agent with memory",
    version="1.0.0"
)

agent = create_agent()

# --- Endpoints ---
@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint - no authentication required."""
    return HealthResponse(status="healthy", version="1.0.0")

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest, 
    api_key: str = Depends(verify_api_key)
):
    """
    Send a message to the agent and receive a response.
    
    The conversation_id is used to maintain context across messages.
    Reuse the same conversation_id to continue a conversation.
    """
    start_time = time.time()
    
    # Use conversation_id as thread_id for checkpointer
    conv_id = request.conversation_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": conv_id}}
    
    logger.info(f"Processing request for conversation {conv_id}")
    
    try:
        # Invoke agent with the new message
        # The checkpointer automatically loads previous messages
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config
        )
        
        # Extract the AI response (last message in the list)
        ai_response = result["messages"][-1].content
        
        processing_time = int((time.time() - start_time) * 1000)
        
        logger.info(f"Request completed in {processing_time}ms")
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conv_id,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred processing your request"
        )
