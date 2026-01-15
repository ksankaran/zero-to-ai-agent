# From: Zero to AI Agent, Chapter 16, Section 16.7
# File: exercise_2_16_7_solution.py

"""
Exercise 2 Solution: Implement Timeout

Agent wrapper that adds timeout handling using concurrent.futures.

Features:
- Decorator pattern for easy application
- Configurable timeout per agent
- Default response on timeout
- Logging of timeout events
"""

from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Callable, Any
from functools import wraps
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import logging
import time

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("timeout_wrapper")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


# =============================================================================
# TIMEOUT DECORATOR
# =============================================================================

def with_timeout(timeout_seconds: float, default_response: dict):
    """
    Decorator that adds timeout to an agent function.
    
    Args:
        timeout_seconds: Maximum time allowed for agent
        default_response: Response to return if timeout occurs
    
    Usage:
        @with_timeout(10.0, {"output": "Timed out"})
        def my_agent(state):
            ...
    """
    def decorator(agent_func: Callable) -> Callable:
        @wraps(agent_func)
        def wrapper(state: dict) -> dict:
            agent_name = agent_func.__name__
            
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(agent_func, state)
                
                try:
                    result = future.result(timeout=timeout_seconds)
                    return result
                
                except TimeoutError:
                    logger.warning(
                        f"[{agent_name}] Timeout after {timeout_seconds}s - using default"
                    )
                    return default_response
                
                except Exception as e:
                    logger.error(f"[{agent_name}] Error: {e}")
                    return default_response
        
        return wrapper
    return decorator


# =============================================================================
# EXAMPLE AGENTS
# =============================================================================

@with_timeout(timeout_seconds=10.0, default_response={"output": "Request timed out"})
def slow_agent(state: dict) -> dict:
    """Agent that might take too long."""
    response = llm.invoke(state["prompt"])
    return {"output": response.content}


@with_timeout(timeout_seconds=2.0, default_response={"output": "Timeout - using fallback"})
def deliberately_slow_agent(state: dict) -> dict:
    """Agent that will definitely timeout (for testing)."""
    time.sleep(5)  # Sleep longer than timeout
    return {"output": "This won't be reached"}


@with_timeout(
    timeout_seconds=15.0, 
    default_response={
        "analysis": "Unable to complete analysis in time",
        "status": "timeout"
    }
)
def analysis_agent(state: dict) -> dict:
    """Complex analysis that might take a while."""
    prompt = f"Provide a detailed analysis of: {state['topic']}"
    response = llm.invoke(prompt)
    return {
        "analysis": response.content,
        "status": "complete"
    }


# =============================================================================
# TIMEOUT WITH RETRY COMBINATION
# =============================================================================

def with_timeout_and_retry(
    timeout_seconds: float, 
    max_retries: int = 3,
    default_response: dict = None
):
    """
    Decorator that combines timeout with retry logic.
    
    Args:
        timeout_seconds: Maximum time per attempt
        max_retries: Number of retries before giving up
        default_response: Response to return if all retries fail
    """
    def decorator(agent_func: Callable) -> Callable:
        @wraps(agent_func)
        def wrapper(state: dict) -> dict:
            agent_name = agent_func.__name__
            
            for attempt in range(max_retries):
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(agent_func, state)
                    
                    try:
                        result = future.result(timeout=timeout_seconds)
                        return result
                    
                    except TimeoutError:
                        logger.warning(
                            f"[{agent_name}] Timeout on attempt {attempt + 1}/{max_retries}"
                        )
                        if attempt < max_retries - 1:
                            continue
                    
                    except Exception as e:
                        logger.error(f"[{agent_name}] Error: {e}")
                        if attempt < max_retries - 1:
                            continue
            
            # All retries exhausted
            logger.error(f"[{agent_name}] All {max_retries} attempts failed")
            return default_response or {"error": "All attempts failed"}
        
        return wrapper
    return decorator


# Example with retry
@with_timeout_and_retry(
    timeout_seconds=5.0, 
    max_retries=3,
    default_response={"summary": "Could not generate summary"}
)
def summarize_agent(state: dict) -> dict:
    """Agent that summarizes content with retry logic."""
    response = llm.invoke(f"Summarize in one sentence: {state['content']}")
    return {"summary": response.content}


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    # Test normal agent (should complete)
    print("=" * 50)
    print("Test 1: Normal agent (should complete)")
    print("=" * 50)
    result = slow_agent({"prompt": "Say hello in 3 words"})
    print(f"Result: {result}")
    
    # Test slow agent (should timeout)
    print("\n" + "=" * 50)
    print("Test 2: Deliberately slow agent (should timeout)")
    print("=" * 50)
    result = deliberately_slow_agent({"prompt": "anything"})
    print(f"Result: {result}")
    
    # Test analysis agent
    print("\n" + "=" * 50)
    print("Test 3: Analysis agent")
    print("=" * 50)
    result = analysis_agent({"topic": "machine learning"})
    print(f"Status: {result['status']}")
    print(f"Analysis: {result['analysis'][:100]}...")
    
    # Test summarize agent with retry
    print("\n" + "=" * 50)
    print("Test 4: Summarize agent with retry")
    print("=" * 50)
    result = summarize_agent({"content": "Python is a versatile programming language."})
    print(f"Summary: {result['summary']}")
