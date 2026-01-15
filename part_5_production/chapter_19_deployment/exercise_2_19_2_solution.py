# From: Zero to AI Agent, Chapter 19, Section 19.2
# File: exercise_2_19_2_solution.py
# Exercise 2: Add Input Validation

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import APIKeyHeader
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
import operator
import uuid
import os

# Load environment variables
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("API_KEY", "dev-key-change-in-production")

# --- Pydantic Models with Validation ---

# Option 1: Using field_validator for custom validation
class ChatRequestWithValidator(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    
    @field_validator('message')
    @classmethod
    def message_must_not_be_empty(cls, v: str) -> str:
        # Strip whitespace and check if empty
        stripped = v.strip()
        if not stripped:
            raise ValueError('Message cannot be empty or whitespace only')
        return stripped  # Return the stripped version
    
    @field_validator('message')
    @classmethod
    def message_must_not_be_too_long(cls, v: str) -> str:
        if len(v) > 1000:
            raise ValueError('Message cannot exceed 1000 characters')
        return v

# Option 2: Using Field constraints (simpler approach)
class ChatRequest(BaseModel):
    message: str = Field(
        ...,  # Required
        min_length=1,
        max_length=1000,
        description="The user's message to the agent"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation ID to continue a conversation"
    )

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
app = FastAPI(title="Agent API with Validation", version="1.0.0")
agent = create_agent()

# --- Custom Error Handler for User-Friendly Messages ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    
    # Create user-friendly messages
    messages = []
    for error in errors:
        field = error['loc'][-1]
        if error['type'] == 'string_too_long':
            messages.append(f"{field}: Message cannot exceed 1000 characters")
        elif error['type'] == 'string_too_short':
            messages.append(f"{field}: Message cannot be empty")
        else:
            messages.append(f"{field}: {error['msg']}")
    
    return JSONResponse(
        status_code=400,
        content={"detail": messages}
    )

# --- Endpoints ---
@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """Send a message to the agent with input validation."""
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
