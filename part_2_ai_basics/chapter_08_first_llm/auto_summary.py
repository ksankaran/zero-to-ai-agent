# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: auto_summary.py

import openai

def create_conversation_summary(messages, client):
    """Generate a summary of a conversation using AI"""
    
    # Don't summarize very short conversations
    if len(messages) < 5:
        return "Conversation too short to summarize"
    
    # Prepare the conversation as text
    conversation_text = ""
    for msg in messages[:20]:  # Limit to prevent token overflow
        role = "Human" if msg['role'] == 'user' else "AI"
        conversation_text += f"{role}: {msg['content']}\n\n"
    
    # Ask AI to summarize
    prompt = f"""Please summarize this conversation in 2-3 sentences. 
Focus on the main topics discussed and any conclusions reached:

{conversation_text}

Summary:"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,  # Lower temperature for factual summary
            max_tokens=100
        )
        
        summary = response.choices[0].message.content
        return summary
    
    except Exception as e:
        return f"Could not generate summary: {str(e)}"

def save_with_summary(messages, client, filename=None):
    """Save conversation with an auto-generated summary"""
    
    # Generate summary
    print("📝 Generating summary...")
    summary = create_conversation_summary(messages, client)
    
    # Prepare data
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summarized_chat_{timestamp}.json"
    
    data = {
        "saved_at": datetime.now().isoformat(),
        "summary": summary,
        "message_count": len(messages),
        "messages": messages
    }
    
    # Save
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"💾 Saved with summary: {summary}")
    return filename
