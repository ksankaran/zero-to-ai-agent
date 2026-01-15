# From: AI Agents Book, Chapter 18, Section 18.1
# File: nodes.py
# Description: Agent node functions - demonstrates LLM integration pattern

from langchain_openai import ChatOpenAI


async def analyze_sentiment(state: dict, llm: ChatOpenAI) -> dict:
    """Analyze the sentiment of the user's last message."""
    messages = state["messages"]
    last_user_message = None
    
    for msg in reversed(messages):
        if msg.type == "human":
            last_user_message = msg.content
            break
    
    if not last_user_message:
        return {"sentiment": "unknown", "confidence": 0.0}
    
    response = await llm.ainvoke([
        {"role": "system", "content": "Analyze sentiment. Respond with only: positive, negative, or neutral"},
        {"role": "user", "content": last_user_message}
    ])
    
    sentiment = response.content.strip().lower()
    
    # Validate the response
    if sentiment not in ["positive", "negative", "neutral"]:
        sentiment = "unknown"
    
    return {"sentiment": sentiment, "confidence": 0.85}
