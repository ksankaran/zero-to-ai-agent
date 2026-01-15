# From: Zero to AI Agent, Chapter 20, Section 20.2
# File: src/caspar/agent/nodes.py

"""
CASPAR Agent Nodes

Each node is a function that processes the current state and returns updates.
Nodes are the "workers" in our LangGraph workflow.
"""

from datetime import datetime, timezone
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from caspar.config import settings, get_logger
from .state import AgentState

logger = get_logger(__name__)


# We'll implement these fully in later sections - this is the structure
# For now, we create placeholder implementations


async def classify_intent(state: AgentState) -> dict:
    """
    Analyze the customer's message to determine their intent.
    
    This node examines the latest message and classifies it into
    one of our known intent categories. The classification drives
    which handler node processes the request.
    
    Possible intents:
    - faq: General question answerable from knowledge base
    - order_inquiry: Question about an order (status, tracking, etc.)
    - complaint: Customer expressing dissatisfaction
    - general: Casual conversation or unclear intent
    - handoff_request: Customer explicitly asking for human agent
    
    Returns:
        Dict with 'intent', 'confidence', and 'last_updated' fields
    """
    logger.info("classify_intent_start", conversation_id=state["conversation_id"])
    
    # Get the latest human message
    messages = state["messages"]
    if not messages:
        return {
            "intent": "general",
            "confidence": 1.0,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    latest_message = messages[-1]
    
    # Use LLM to classify intent
    llm = ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        temperature=0  # We want consistent classification
    )
    
    classification_prompt = f"""Classify the customer's intent into exactly one category.

Customer message: {latest_message.content}

Categories:
- faq: General questions about policies, products, services, shipping times, return policies, how things work
- order_inquiry: Questions about a SPECIFIC order (mentions order number, tracking number, "my order", "my package")
- complaint: Customer expressing frustration, dissatisfaction, or reporting a problem
- general: Casual conversation, greetings, or unclear intent
- handoff_request: Customer explicitly asking to speak with a human agent

IMPORTANT: 
- "How long does shipping take?" = faq (general policy question)
- "Where is my order?" or "Track order #123" = order_inquiry (specific order)

Respond with ONLY the category name, nothing else."""

    response = await llm.ainvoke([HumanMessage(content=classification_prompt)])
    intent = response.content.strip().lower()
    
    # Validate intent
    valid_intents = ["faq", "order_inquiry", "complaint", "general", "handoff_request"]
    if intent not in valid_intents:
        intent = "general"
    
    logger.info(
        "classify_intent_complete",
        conversation_id=state["conversation_id"],
        intent=intent
    )
    
    return {
        "intent": intent,
        "confidence": 0.9,  # We'll improve this with actual confidence scoring later
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def handle_faq(state: AgentState) -> dict:
    """
    Handle FAQ-type questions using the knowledge base.
    
    This node retrieves relevant information from ChromaDB
    and prepares context for response generation.
    
    Returns:
        Dict with 'retrieved_context' field
    """
    logger.info("handle_faq_start", conversation_id=state["conversation_id"])
    
    # RAG implementation will be added in Section 20.3
    # For now, return placeholder
    
    return {
        "retrieved_context": "Knowledge base context will be retrieved here.",
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def handle_order_inquiry(state: AgentState) -> dict:
    """
    Handle order-related inquiries using the order lookup tool.
    
    This node extracts order information from the message,
    calls the order lookup tool, and prepares the response context.
    
    Returns:
        Dict with 'order_info' and optionally 'retrieved_context'
    """
    logger.info("handle_order_inquiry_start", conversation_id=state["conversation_id"])
    
    # Tool implementation will be added in Section 20.4
    # For now, return placeholder
    
    return {
        "order_info": {"status": "Tool integration pending"},
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def handle_complaint(state: AgentState) -> dict:
    """
    Handle customer complaints with empathy and appropriate actions.
    
    This node:
    1. Acknowledges the customer's frustration
    2. Retrieves relevant policy information
    3. Determines if a support ticket should be created
    4. May trigger escalation for serious complaints
    
    Returns:
        Dict with context and potentially escalation flags
    """
    logger.info("handle_complaint_start", conversation_id=state["conversation_id"])
    
    # Complaints often need escalation - we'll implement this fully later
    
    return {
        "retrieved_context": "Complaint handling context will be added.",
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def handle_general(state: AgentState) -> dict:
    """
    Handle general conversation and unclear intents.
    
    This is the fallback handler for messages that don't fit
    other categories. It provides helpful, friendly responses
    and tries to guide the customer toward a specific intent.
    
    Returns:
        Dict with minimal updates (general chat doesn't need much context)
    """
    logger.info("handle_general_start", conversation_id=state["conversation_id"])
    
    return {
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def check_sentiment(state: AgentState) -> dict:
    """
    Analyze customer sentiment and determine frustration level.
    
    This node runs after every handler to assess how the customer
    is feeling. High frustration triggers escalation to human agents.
    
    Sentiment analysis considers:
    - Current message tone
    - Conversation trajectory (getting worse or better?)
    - Explicit frustration markers (caps, punctuation, keywords)
    
    Returns:
        Dict with 'sentiment_score', 'frustration_level', and potentially
        'needs_escalation' and 'escalation_reason'
    """
    logger.info("check_sentiment_start", conversation_id=state["conversation_id"])
    
    messages = state["messages"]
    if not messages:
        return {
            "sentiment_score": 0.0,
            "frustration_level": "low",
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    latest_message = messages[-1]
    
    # Use LLM for sentiment analysis
    llm = ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        temperature=0
    )
    
    sentiment_prompt = f"""Analyze the sentiment of this customer message.

Message: {latest_message.content}

Rate the sentiment from -1.0 (very negative/frustrated) to 1.0 (very positive/happy).
Also determine the frustration level: low, medium, or high.

Respond in this exact format:
SCORE: <number>
LEVEL: <low/medium/high>"""

    response = await llm.ainvoke([HumanMessage(content=sentiment_prompt)])
    
    # Parse response
    lines = response.content.strip().split("\n")
    sentiment_score = 0.0
    frustration_level = "low"
    
    for line in lines:
        if line.startswith("SCORE:"):
            try:
                sentiment_score = float(line.replace("SCORE:", "").strip())
                sentiment_score = max(-1.0, min(1.0, sentiment_score))  # Clamp
            except ValueError:
                pass
        elif line.startswith("LEVEL:"):
            level = line.replace("LEVEL:", "").strip().lower()
            if level in ["low", "medium", "high"]:
                frustration_level = level
    
    # Determine if escalation is needed based on sentiment
    needs_escalation = (
        sentiment_score < settings.sentiment_threshold or
        frustration_level == "high"
    )
    
    result = {
        "sentiment_score": sentiment_score,
        "frustration_level": frustration_level,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    
    if needs_escalation and not state.get("needs_escalation"):
        result["needs_escalation"] = True
        result["escalation_reason"] = f"High frustration detected (score: {sentiment_score})"
        logger.warning(
            "escalation_triggered",
            conversation_id=state["conversation_id"],
            sentiment_score=sentiment_score,
            frustration_level=frustration_level
        )
    
    logger.info(
        "check_sentiment_complete",
        conversation_id=state["conversation_id"],
        sentiment_score=sentiment_score,
        frustration_level=frustration_level
    )
    
    return result


async def respond(state: AgentState) -> dict:
    """
    Generate the final response to the customer.
    
    This node synthesizes all the context gathered by previous nodes
    (knowledge base results, order info, etc.) into a helpful,
    friendly response.
    
    Returns:
        Dict with new AI message added to messages
    """
    logger.info("respond_start", conversation_id=state["conversation_id"])
    
    llm = ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        temperature=0.7  # Slightly creative for natural responses
    )
    
    # Build system prompt with context
    system_prompt = """You are CASPAR, TechFlow's friendly customer service assistant.

TechFlow is an online electronics retailer. You help customers with:
- Product questions
- Order status and tracking
- Returns and refunds
- Shipping information
- Technical support

Guidelines:
- Be warm, helpful, and professional
- Keep responses concise but complete
- If you don't know something, say so honestly
- Never make up order information or policies
- For complex issues, offer to connect with a human agent"""

    # Add context if available
    if state.get("retrieved_context"):
        system_prompt += f"\n\nRelevant information:\n{state['retrieved_context']}"
    
    if state.get("order_info"):
        system_prompt += f"\n\nOrder information:\n{state['order_info']}"
    
    # Build messages for LLM
    llm_messages = [SystemMessage(content=system_prompt)]
    
    # Add conversation history (last 10 messages to manage context)
    for msg in state["messages"][-10:]:
        llm_messages.append(msg)
    
    # Generate response
    response = await llm.ainvoke(llm_messages)
    
    logger.info("respond_complete", conversation_id=state["conversation_id"])
    
    return {
        "messages": [AIMessage(content=response.content)],
        "turn_count": state["turn_count"] + 1,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def human_handoff(state: AgentState) -> dict:
    """
    Handle escalation to a human agent.
    
    This node is triggered when:
    - Customer explicitly requests a human
    - Sentiment analysis detects high frustration
    - The issue is beyond CASPAR's capabilities
    
    Returns:
        Dict with handoff message and updated state
    """
    logger.info(
        "human_handoff_triggered",
        conversation_id=state["conversation_id"],
        reason=state.get("escalation_reason", "Customer request")
    )
    
    reason = state.get("escalation_reason", "You've requested to speak with a human agent")
    
    handoff_message = f"""I understand you'd like to speak with a human agent. {reason}.

I'm connecting you with one of our support specialists now. They'll have access to our conversation history, so you won't need to repeat yourself.

Current wait time is approximately 2-3 minutes. Thank you for your patience!

Is there anything specific you'd like me to note for the human agent?"""
    
    return {
        "messages": [AIMessage(content=handoff_message)],
        "needs_escalation": True,
        "turn_count": state["turn_count"] + 1,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
