# From: Zero to AI Agent, Chapter 20, Section 20.3
# File: src/caspar/agent/nodes_faq_update.py
#
# This file shows the UPDATED handle_faq function from nodes.py
# that integrates the knowledge base. Merge this into your existing nodes.py.

"""
Updated handle_faq function with knowledge base integration.

To use this, update your src/caspar/agent/nodes.py file:
1. Add the import: from caspar.knowledge import get_retriever
2. Replace the handle_faq function with the version below
"""

from datetime import datetime, timezone

from caspar.config import get_logger
from caspar.knowledge import get_retriever
from .state import AgentState

logger = get_logger(__name__)


async def handle_faq(state: AgentState) -> dict:
    """
    Handle FAQ-type questions using the knowledge base.
    
    This node retrieves relevant information from ChromaDB
    and prepares context for response generation.
    
    Returns:
        Dict with 'retrieved_context' field
    """
    logger.info("handle_faq_start", conversation_id=state["conversation_id"])
    
    # Get the latest message
    messages = state["messages"]
    if not messages:
        return {
            "retrieved_context": None,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    query = messages[-1].content
    
    # Retrieve relevant documents
    retriever = get_retriever()
    documents = retriever.retrieve(query=query, k=4)
    
    # Format context for the LLM
    context = retriever.format_context(documents)
    
    logger.info(
        "handle_faq_complete",
        conversation_id=state["conversation_id"],
        documents_found=len(documents)
    )
    
    return {
        "retrieved_context": context,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
