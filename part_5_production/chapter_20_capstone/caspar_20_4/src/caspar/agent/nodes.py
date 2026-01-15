# From: Zero to AI Agent, Chapter 20, Section 20.4
# File: src/caspar/agent/nodes.py

"""
CASPAR Agent Nodes

Each node is a function that processes state and returns updates.
"""

from datetime import datetime, timezone

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage

from caspar.config import settings, get_logger
from caspar.knowledge import get_retriever
from caspar.tools import get_order_status, create_ticket, get_account_info
from .state import AgentState

logger = get_logger(__name__)


async def classify_intent(state: AgentState) -> dict:
    """Classify the customer's intent from their message."""
    
    logger.info("classify_intent_start", conversation_id=state["conversation_id"])
    
    llm = ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        temperature=0  # Deterministic for classification
    )
    
    messages = state["messages"]
    if not messages:
        return {"intent": "general", "confidence": 0.5, "last_updated": datetime.now(timezone.utc).isoformat()}
    
    last_message = messages[-1].content
    
    classification_prompt = f"""Classify this customer service message into ONE of these categories:

- faq: General questions about policies, products, services, shipping times, how things work
- order_inquiry: Questions about a SPECIFIC order (mentions order number, "my order", "my package")
- account: Questions about their account, points, profile
- complaint: Expressing dissatisfaction or problems
- handoff_request: Explicitly asking for human help
- general: Anything else, greetings, unclear intent

IMPORTANT: 
- "How long does shipping take?" = faq (general policy question)
- "Where is my order?" = order_inquiry (specific order)

Customer message: "{last_message}"

Respond with ONLY the category name, nothing else."""

    response = llm.invoke([HumanMessage(content=classification_prompt)])
    intent = response.content.strip().lower()
    
    valid_intents = ["faq", "order_inquiry", "account", "complaint", "handoff_request", "general"]
    if intent not in valid_intents:
        intent = "general"
    
    logger.info("classify_intent_complete", conversation_id=state["conversation_id"], intent=intent)
    
    return {
        "intent": intent,
        "confidence": 0.85,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def handle_faq(state: AgentState) -> dict:
    """Handle FAQ-type questions using the knowledge base."""
    
    logger.info("handle_faq_start", conversation_id=state["conversation_id"])
    
    messages = state["messages"]
    if not messages:
        return {"retrieved_context": None, "last_updated": datetime.now(timezone.utc).isoformat()}
    
    query = messages[-1].content
    
    # Retrieve relevant documents
    retriever = get_retriever()
    documents = retriever.retrieve(query=query, k=4)
    context = retriever.format_context(documents)
    
    logger.info("handle_faq_complete", conversation_id=state["conversation_id"], documents_found=len(documents))
    
    return {
        "retrieved_context": context,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def handle_order_inquiry(state: AgentState) -> dict:
    """Handle order-related inquiries by looking up order status."""
    
    logger.info("handle_order_inquiry_start", conversation_id=state["conversation_id"])
    
    messages = state["messages"]
    if not messages:
        return {"order_info": None, "last_updated": datetime.now(timezone.utc).isoformat()}
    
    last_message = messages[-1].content
    customer_id = state.get("customer_id")
    
    # Use LLM to extract order ID from the message
    llm = ChatOpenAI(
        model=settings.default_model,
        api_key=settings.openai_api_key,
        temperature=0
    )
    
    extract_prompt = f"""Extract the order ID from this customer message.
Order IDs look like: TF-10001, TF-12345, or just numbers like 10001, 12345

Customer message: "{last_message}"

If you find an order ID, respond with ONLY the ID.
If no order ID is found, respond with "NONE"."""

    response = llm.invoke([HumanMessage(content=extract_prompt)])
    extracted_id = response.content.strip()
    
    # Look up the order
    order_info = None
    if extracted_id and extracted_id != "NONE":
        result = get_order_status(extracted_id, customer_id)
        
        if result["found"]:
            order_info = {
                "order_id": extracted_id,
                "status": result["order"]["status"],
                "summary": result["summary"],
                "full_order": result["order"]
            }
        else:
            order_info = {"order_id": extracted_id, "error": result["error"]}
    else:
        order_info = {
            "error": "I couldn't find an order number in your message. Could you please provide your order ID? It looks like TF-XXXXX."
        }
    
    logger.info("handle_order_inquiry_complete", conversation_id=state["conversation_id"])
    
    return {
        "order_info": order_info,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def handle_account(state: AgentState) -> dict:
    """Handle account-related inquiries."""
    
    logger.info("handle_account_start", conversation_id=state["conversation_id"])
    
    customer_id = state.get("customer_id")
    
    if not customer_id:
        return {
            "retrieved_context": "I'd be happy to help with your account, but I need to verify your identity first. Could you please provide your customer ID or email?",
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    result = get_account_info(customer_id)
    context = result["summary"] if result["found"] else result["error"]
    
    logger.info("handle_account_complete", conversation_id=state["conversation_id"])
    
    return {
        "retrieved_context": context,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def handle_complaint(state: AgentState) -> dict:
    """Handle customer complaints - acknowledges and creates a ticket."""
    
    logger.info("handle_complaint_start", conversation_id=state["conversation_id"])
    
    messages = state["messages"]
    customer_id = state.get("customer_id") or "UNKNOWN"
    conversation_id = state.get("conversation_id")
    
    if not messages:
        return {"retrieved_context": None, "last_updated": datetime.now(timezone.utc).isoformat()}
    
    last_message = messages[-1].content
    
    # Try to get relevant KB info
    retriever = get_retriever()
    documents = retriever.retrieve(query=last_message, k=2)
    kb_context = retriever.format_context(documents) if documents else ""
    
    # Create a high-priority ticket
    ticket_result = create_ticket(
        customer_id=customer_id,
        category="general",
        subject=f"Customer Complaint: {last_message[:50]}...",
        description=last_message,
        priority="high",  # Complaints get high priority
        conversation_id=conversation_id,
    )
    
    context_parts = []
    if kb_context:
        context_parts.append(f"Relevant Information:\n{kb_context}")
    context_parts.append(f"\n{ticket_result['confirmation']}")
    
    logger.info("handle_complaint_complete", ticket_id=ticket_result["ticket"]["ticket_id"])
    
    return {
        "retrieved_context": "\n\n".join(context_parts),
        "ticket_id": ticket_result["ticket"]["ticket_id"],
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def handle_general(state: AgentState) -> dict:
    """Handle general inquiries - falls back to knowledge base search."""
    
    logger.info("handle_general_start", conversation_id=state["conversation_id"])
    
    messages = state["messages"]
    if not messages:
        return {"retrieved_context": None, "last_updated": datetime.now(timezone.utc).isoformat()}
    
    query = messages[-1].content
    
    # Try knowledge base - might find something useful
    retriever = get_retriever()
    documents = retriever.retrieve(query=query, k=2)
    context = retriever.format_context(documents) if documents else None
    
    logger.info("handle_general_complete", conversation_id=state["conversation_id"])
    
    return {
        "retrieved_context": context,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def check_sentiment(state: AgentState) -> dict:
    """Analyze customer sentiment and determine if escalation is needed."""
    
    logger.info("check_sentiment_start", conversation_id=state["conversation_id"])
    
    messages = state["messages"]
    if not messages:
        return {"sentiment_score": 0.0, "frustration_level": "low", "last_updated": datetime.now(timezone.utc).isoformat()}
    
    # Get last few messages for context
    recent_messages = messages[-3:] if len(messages) >= 3 else messages
    conversation_text = "\n".join([
        f"{'Customer' if isinstance(m, HumanMessage) else 'Agent'}: {m.content}"
        for m in recent_messages
    ])
    
    llm = ChatOpenAI(model=settings.default_model, api_key=settings.openai_api_key, temperature=0)
    
    sentiment_prompt = f"""Analyze the customer's emotional state in this conversation.

Conversation:
{conversation_text}

Provide your analysis in this exact format:
SENTIMENT: [number from -1.0 to 1.0, where -1 is very negative, 0 is neutral, 1 is very positive]
FRUSTRATION: [low, medium, or high]"""

    response = llm.invoke([HumanMessage(content=sentiment_prompt)])
    
    # Parse response
    sentiment_score = 0.0
    frustration_level = "low"
    
    for line in response.content.strip().split("\n"):
        if line.startswith("SENTIMENT:"):
            try:
                sentiment_score = float(line.split(":")[1].strip())
                sentiment_score = max(-1.0, min(1.0, sentiment_score))
            except ValueError:
                pass
        elif line.startswith("FRUSTRATION:"):
            level = line.split(":")[1].strip().lower()
            if level in ["low", "medium", "high"]:
                frustration_level = level
    
    # Check if escalation needed
    needs_escalation = sentiment_score < settings.sentiment_threshold or frustration_level == "high"
    
    result = {
        "sentiment_score": sentiment_score,
        "frustration_level": frustration_level,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    
    if needs_escalation and not state.get("needs_escalation"):
        result["needs_escalation"] = True
        result["escalation_reason"] = f"High frustration detected (score: {sentiment_score})"
        logger.warning("escalation_triggered", conversation_id=state["conversation_id"])
    
    logger.info("check_sentiment_complete", sentiment_score=sentiment_score, frustration_level=frustration_level)
    
    return result


async def respond(state: AgentState) -> dict:
    """Generate the final response to the customer."""
    
    logger.info("respond_start", conversation_id=state["conversation_id"])
    
    llm = ChatOpenAI(model=settings.default_model, api_key=settings.openai_api_key, temperature=0.7)
    
    # Build system prompt
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
- If you have specific information (order details, policies), share it clearly
- Never make up order numbers, tracking info, or policies
"""
    
    # Add context from previous nodes
    context_parts = []
    
    if state.get("retrieved_context"):
        context_parts.append(f"Relevant Information:\n{state['retrieved_context']}")
    
    if state.get("order_info"):
        order = state["order_info"]
        if "summary" in order:
            context_parts.append(f"Order Information:\n{order['summary']}")
        elif "error" in order:
            context_parts.append(f"Order Lookup Result: {order['error']}")
    
    if state.get("ticket_id"):
        context_parts.append(f"A support ticket has been created: {state['ticket_id']}")
    
    if context_parts:
        system_prompt += "\nContext for this response:\n" + "\n\n".join(context_parts)
    
    # Build messages
    llm_messages = [{"role": "system", "content": system_prompt}]
    for msg in state["messages"]:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        llm_messages.append({"role": role, "content": msg.content})
    
    response = llm.invoke(llm_messages)
    
    logger.info("respond_complete", conversation_id=state["conversation_id"])
    
    return {
        "messages": [AIMessage(content=response.content)],
        "turn_count": state.get("turn_count", 0) + 1,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


async def human_handoff(state: AgentState) -> dict:
    """Handle escalation to a human agent."""
    
    logger.info("human_handoff_start", conversation_id=state["conversation_id"])
    
    customer_id = state.get("customer_id") or "UNKNOWN"
    conversation_id = state.get("conversation_id")
    
    # Summarize conversation for the human agent
    messages = state["messages"]
    conversation_summary = "\n".join([
        f"{'Customer' if isinstance(m, HumanMessage) else 'CASPAR'}: {m.content[:200]}..."
        if len(m.content) > 200 else
        f"{'Customer' if isinstance(m, HumanMessage) else 'CASPAR'}: {m.content}"
        for m in messages[-5:]
    ])
    
    # Create urgent ticket
    ticket_result = create_ticket(
        customer_id=customer_id,
        category="general",
        subject="Human Agent Requested",
        description=f"Escalation Reason: {state.get('escalation_reason', 'Customer request')}\n\nRecent Conversation:\n{conversation_summary}",
        priority="urgent",
        conversation_id=conversation_id,
    )
    
    handoff_message = f"""I understand you'd like to speak with a human agent. I've created a priority ticket for you.

**{ticket_result['confirmation']}**

A human agent will reach out to you shortly. Is there anything else I can help you with in the meantime?"""
    
    logger.info("human_handoff_complete", ticket_id=ticket_result["ticket"]["ticket_id"])
    
    return {
        "messages": [AIMessage(content=handoff_message)],
        "needs_escalation": True,
        "escalation_reason": state.get("escalation_reason", "Customer requested human agent"),
        "ticket_id": ticket_result["ticket"]["ticket_id"],
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
