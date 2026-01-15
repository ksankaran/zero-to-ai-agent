# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: readable_format.py

def save_as_text(messages, filename=None):
    """Save conversation in human-readable text format"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_transcript_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        # Write header
        f.write("=" * 60 + "\n")
        f.write(f"CONVERSATION TRANSCRIPT\n")
        f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
        f.write("=" * 60 + "\n\n")
        
        # Write each message
        for i, msg in enumerate(messages, 1):
            role = msg['role'].upper()
            content = msg['content']
            
            # Format based on role
            if role == 'USER':
                f.write(f"👤 YOU (Message {i}):\n")
            elif role == 'ASSISTANT':
                f.write(f"🤖 AI (Message {i}):\n")
            else:
                f.write(f"📋 {role} (Message {i}):\n")
            
            f.write(f"{content}\n")
            f.write("-" * 40 + "\n\n")
        
        # Write footer
        f.write("=" * 60 + "\n")
        f.write(f"End of conversation - {len(messages)} messages total\n")
    
    print(f"📄 Readable transcript saved to {filename}")
    return filename
