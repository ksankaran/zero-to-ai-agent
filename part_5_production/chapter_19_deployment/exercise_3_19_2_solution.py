# From: Zero to AI Agent, Chapter 19, Section 19.2
# File: exercise_3_19_2_solution.py
# Exercise 3: Add Rate Limiting

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from collections import defaultdict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
import operator
import uuid
import time
import os

# Load environment variables
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("API_KEY", "dev-key-change-in-production")
RATE_LIMIT_REQUESTS = 10  # Max requests
RATE_LIMIT_WINDOW = 60    # Per 60 seconds

# --- Rate Limiting ---
# Store request timestamps per API key
request_timestamps: Dict[str, List[float]] = defaultdict(list)

def check_rate_limit(api_key: str) -> tuple[bool, int]:
    """
    Check if the API key has exceeded the rate limit.
    Returns (is_allowed, retry_after_seconds)
    """
    current_time = time.time()
    window_start = current_time - RATE_LIMIT_WINDOW
    
    # Get timestamps for this API key
    timestamps = request_timestamps[api_key]
    
    # Remove timestamps outside the current window
    timestamps = [ts for ts in timestamps if ts > window_start]
    request_timestamps[api_key] = timestamps
    
    # Check if limit exceeded
    if len(timestamps) >= RATE_LIMIT_REQUESTS:
        # Calculate when the oldest request in window will expire
        oldest_in_window = min(timestamps)
        retry_after = int(oldest_in_window + RATE_LIMIT_WINDOW - current_time) + 1
        return False, retry_after
    
    # Record this request
    timestamps.append(current_time)
    return True, 0

# --- Rate Limit Middleware ---
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for certain paths
        if request.url.path in ["/health", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        # Get API key from header
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return await call_next(request)  # Let auth handle missing key
        
        # Check rate limit
        is_allowed, retry_after = check_rate_limit(api_key)
        if not is_allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
                headers={"Retry-After": str(retry_after)}
            )
        
        return await call_next(request)

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

# --- Security ---
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: Optional[str] = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key

# --- API Setup ---
app = FastAPI(title="Agent API with Rate Limiting", version="1.0.0")

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

agent = create_agent()

# --- Endpoints ---
@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """Send a message to the agent (rate limited)."""
    conv_id = request.conversation_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": conv_id}}
    
    try:
        result = await agent.ainvoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config
        )
        
        ai_response = result["messages"][-1].content
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conv_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred")

@app.get("/health")
def health():
    return {"status": "healthy"}


# --- Alternative: Rate limiting in dependency ---
def verify_api_key_with_rate_limit(
    api_key: Optional[str] = Depends(api_key_header)
):
    """Combined API key verification and rate limiting."""
    # First check the API key is valid
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    
    # Then check rate limit
    is_allowed, retry_after = check_rate_limit(api_key)
    if not is_allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": str(retry_after)}
        )
    
    return api_key
