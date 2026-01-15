# From: Zero to AI Agent, Chapter 17, Section 17.7
# Save as: production_patterns.py
# Reference patterns for production LangGraph deployment
# Note: These are illustrative patterns, not a complete runnable application

import logging
import time
from datetime import datetime
from typing import TypedDict
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# PATTERN 1: RETRY WITH BACKOFF
# =============================================================================
# Use tenacity for robust retry logic with transient failures

from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_llm_with_retry(llm, prompt):
    """Retry LLM calls with exponential backoff.
    
    - Retries up to 3 times
    - Waits 2s, then 4s, then 8s between retries (capped at 10s)
    - Handles transient API failures gracefully
    """
    return llm.invoke(prompt)


# =============================================================================
# PATTERN 2: ASYNC TIMEOUT
# =============================================================================
# Prevent hanging nodes with async timeouts

from asyncio import timeout

async def node_with_timeout(state, llm, timeout_seconds=30):
    """Execute node with timeout to prevent hanging.
    
    Args:
        state: Current graph state
        llm: Language model instance
        timeout_seconds: Maximum execution time
        
    Raises:
        TimeoutError: If execution exceeds timeout
    """
    async with timeout(timeout_seconds):
        return await llm.ainvoke(state["messages"])


# =============================================================================
# PATTERN 3: SAFE NODE WITH FALLBACK
# =============================================================================
# Always provide fallback responses

def safe_node(state, process_fn, logger):
    """Wrap node processing with error handling and fallback.
    
    Args:
        state: Current graph state
        process_fn: The actual processing function
        logger: Logger instance for error tracking
        
    Returns:
        Either the processed result or a fallback error response
    """
    try:
        return process_fn(state)
    except Exception as e:
        logger.error(f"Node failed: {e}", exc_info=True)
        return {"error": "I encountered an issue. Please try again."}


# =============================================================================
# PATTERN 4: TOKEN USAGE TRACKING
# =============================================================================
# Track and limit token usage per session

MAX_TOKENS_PER_SESSION = 50000  # Example limit

def track_usage(state):
    """Check token usage and enforce limits.
    
    Add this as a node or check within nodes to prevent
    runaway costs from long conversations or loops.
    """
    usage = state.get("total_tokens", 0)
    if usage > MAX_TOKENS_PER_SESSION:
        return {"error": "Session token limit reached. Please start a new session."}
    return state


# =============================================================================
# PATTERN 5: ITERATION LIMITS
# =============================================================================
# Always cap loops to prevent infinite execution

MAX_ITERATIONS = 5

def should_continue(state):
    """Route function with mandatory iteration cap.
    
    Always include iteration checks in feedback loops
    to prevent infinite execution and runaway costs.
    """
    if state["iteration"] >= MAX_ITERATIONS:
        return "end"  # Force exit regardless of other conditions
    
    # Your other routing logic here
    if state.get("task_complete"):
        return "end"
    
    return "continue"


# =============================================================================
# PATTERN 6: MODEL TIERING
# =============================================================================
# Use cheaper models for simple tasks, expensive for complex

def get_appropriate_model(task_type):
    """Select model based on task complexity.
    
    Saves costs by using cheaper models for simple tasks
    while reserving expensive models for complex reasoning.
    """
    from langchain_openai import ChatOpenAI
    
    if task_type in ["classification", "extraction", "simple_qa"]:
        return ChatOpenAI(model="gpt-3.5-turbo")  # Cheaper
    elif task_type in ["complex_reasoning", "code_generation", "analysis"]:
        return ChatOpenAI(model="gpt-4")  # More capable
    else:
        return ChatOpenAI(model="gpt-3.5-turbo")  # Default to cheaper


# =============================================================================
# PATTERN 7: STRUCTURED LOGGING
# =============================================================================
# Essential logging for production observability

logger = logging.getLogger("agent")

def logged_node(state, node_name, process_fn):
    """Wrap node with comprehensive logging.
    
    Logs:
    - Node start with context (thread_id, iteration)
    - Execution duration
    - Errors with full stack traces
    """
    start = datetime.now()
    
    logger.info(f"[{node_name}] Starting", extra={
        "thread_id": state.get("thread_id"),
        "iteration": state.get("iteration"),
        "node": node_name
    })
    
    try:
        result = process_fn(state)
        duration = (datetime.now() - start).total_seconds()
        
        logger.info(f"[{node_name}] Completed in {duration:.2f}s", extra={
            "thread_id": state.get("thread_id"),
            "duration": duration,
            "node": node_name
        })
        return result
        
    except Exception as e:
        logger.error(f"[{node_name}] Failed: {e}", exc_info=True, extra={
            "thread_id": state.get("thread_id"),
            "node": node_name,
            "error": str(e)
        })
        raise


# =============================================================================
# PATTERN 8: INPUT VALIDATION
# =============================================================================
# Never trust user input

MAX_MESSAGE_LENGTH = 10000
BLOCKED_PATTERNS = ["ignore previous instructions", "system prompt"]

def validate_input(user_message: str) -> str:
    """Validate and sanitize user input.
    
    Checks:
    - Message length limits
    - Blocked patterns (basic prompt injection defense)
    - Empty input
    
    Returns:
        Sanitized message
        
    Raises:
        ValueError: If validation fails
    """
    if not user_message or not user_message.strip():
        raise ValueError("Empty message")
    
    if len(user_message) > MAX_MESSAGE_LENGTH:
        raise ValueError(f"Message too long (max {MAX_MESSAGE_LENGTH} chars)")
    
    # Basic prompt injection check
    message_lower = user_message.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in message_lower:
            raise ValueError("Invalid input detected")
    
    return user_message.strip()


# =============================================================================
# PATTERN 9: OUTPUT FILTERING
# =============================================================================
# Filter sensitive information from responses

SENSITIVE_PATTERNS = ["API_KEY", "password", "secret"]

def filter_output(response: str) -> str:
    """Filter potentially sensitive content from responses.
    
    Production systems should implement more sophisticated
    content filtering based on their specific requirements.
    """
    filtered = response
    
    # Remove any accidentally leaked sensitive patterns
    for pattern in SENSITIVE_PATTERNS:
        if pattern.lower() in filtered.lower():
            filtered = filtered.replace(pattern, "[REDACTED]")
    
    return filtered


# =============================================================================
# PATTERN 10: RATE LIMITING
# =============================================================================
# Protect against abuse with rate limits

request_counts = defaultdict(list)

def rate_limit(user_id: str, max_requests: int = 10, window_seconds: int = 60):
    """Enforce per-user rate limits.
    
    Args:
        user_id: Unique identifier for the user
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
        
    Raises:
        Exception: If rate limit exceeded
    """
    now = time.time()
    
    # Clean old requests outside the window
    request_counts[user_id] = [
        t for t in request_counts[user_id] 
        if now - t < window_seconds
    ]
    
    if len(request_counts[user_id]) >= max_requests:
        raise Exception(f"Rate limit exceeded. Max {max_requests} requests per {window_seconds}s")
    
    request_counts[user_id].append(now)


# =============================================================================
# PATTERN 11: PRODUCTION CHECKPOINTER
# =============================================================================
# Use external storage for scalable state persistence

def get_production_checkpointer(connection_string: str):
    """Create a production-ready checkpointer.
    
    For production, use PostgreSQL or another persistent store
    instead of in-memory checkpointing.
    
    Args:
        connection_string: Database connection string
        
    Returns:
        PostgresSaver checkpointer instance
    """
    from langgraph.checkpoint.postgres import PostgresSaver
    
    return PostgresSaver.from_conn_string(connection_string)


# Example usage:
# checkpointer = get_production_checkpointer(
#     "postgresql://user:pass@host:5432/db"
# )
# graph = builder.compile(checkpointer=checkpointer)


# =============================================================================
# PATTERN 12: SIMPLE TEST EXAMPLE
# =============================================================================
# Basic test pattern for agents

def test_agent_handles_greeting(graph):
    """Example test: agent handles basic greeting.
    
    Production agents should have comprehensive test suites:
    - Unit tests for individual nodes
    - Integration tests for full flows
    - End-to-end tests for conversations
    - Load tests for performance
    - Adversarial tests for security
    """
    result = graph.invoke({
        "messages": [{"role": "user", "content": "Hello!"}]
    })
    
    assert "error" not in result, "Agent should not return error for greeting"
    assert len(result.get("messages", [])) > 1, "Agent should respond to greeting"
    
    return True


# =============================================================================
# COMBINED EXAMPLE: Production-Ready Node
# =============================================================================

def create_production_node(node_name, process_fn, llm):
    """Factory for creating production-ready nodes.
    
    Combines multiple patterns:
    - Retry logic
    - Timeout handling
    - Logging
    - Error handling with fallback
    - Usage tracking
    """
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def production_node(state):
        start = datetime.now()
        
        logger.info(f"[{node_name}] Starting", extra={
            "thread_id": state.get("thread_id"),
            "iteration": state.get("iteration")
        })
        
        try:
            # Check token limits
            if state.get("total_tokens", 0) > MAX_TOKENS_PER_SESSION:
                return {"error": "Token limit reached"}
            
            # Process
            result = process_fn(state, llm)
            
            # Log success
            duration = (datetime.now() - start).total_seconds()
            logger.info(f"[{node_name}] Completed in {duration:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"[{node_name}] Failed: {e}", exc_info=True)
            return {"error": f"Node {node_name} failed. Please try again."}
    
    return production_node


# =============================================================================
# PRODUCTION CHECKLIST SUMMARY
# =============================================================================
"""
Production Deployment Checklist:

RELIABILITY:
□ Retry logic with exponential backoff
□ Timeouts on all external calls
□ Fallback responses for failures
□ Graceful degradation

COST MANAGEMENT:
□ Token usage tracking
□ Iteration limits on all loops
□ Model tiering (cheap vs expensive)
□ Session duration limits

OBSERVABILITY:
□ Structured logging (JSON format)
□ Request tracing (thread_id)
□ Duration tracking
□ Error tracking with stack traces
□ Consider LangSmith for traces

SECURITY:
□ Input validation and length limits
□ Output filtering for sensitive data
□ Rate limiting per user
□ Prompt injection defenses

SCALING:
□ External checkpointer (PostgreSQL)
□ Async nodes for concurrency
□ Connection pooling
□ Load balancer ready

TESTING:
□ Unit tests for nodes
□ Integration tests for flows
□ End-to-end conversation tests
□ Load tests
□ Adversarial/security tests
"""

if __name__ == "__main__":
    print("Production Patterns Reference File")
    print("=" * 50)
    print("This file contains reference patterns for production deployment.")
    print("Import and adapt these patterns for your specific use case.")
    print("\nPatterns included:")
    print("  1. Retry with backoff")
    print("  2. Async timeout")
    print("  3. Safe node with fallback")
    print("  4. Token usage tracking")
    print("  5. Iteration limits")
    print("  6. Model tiering")
    print("  7. Structured logging")
    print("  8. Input validation")
    print("  9. Output filtering")
    print("  10. Rate limiting")
    print("  11. Production checkpointer")
    print("  12. Test example")
