# From: Zero to AI Agent, Chapter 9, Section 9.2
# File: ai_assistant.py

"""
Simple demonstration of system + user prompt pattern
"""

class AIAssistant:
    """Simple demonstration of system + user prompt pattern"""
    
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.conversation = [
            {"role": "system", "content": system_prompt}
        ]
    
    def ask(self, user_prompt: str) -> str:
        # Add user message to conversation
        self.conversation.append({"role": "user", "content": user_prompt})
        
        # In real implementation, you'd call the API here
        # response = client.chat.completions.create(...)
        
        # For demonstration, we'll just show the structure
        print(f"System Context: {self.system_prompt[:50]}...")
        print(f"User Asked: {user_prompt}")
        print("AI responds based on both prompts")
        
        # Add assistant response to conversation history
        # self.conversation.append({"role": "assistant", "content": response})
        
        return "Response that follows system prompt rules"

# Example usage
if __name__ == "__main__":
    # Create specialized assistants
    python_tutor = AIAssistant(
        "You are a patient Python tutor for beginners. "
        "Use simple language and provide examples."
    )
    
    sql_expert = AIAssistant(
        "You are a SQL optimization expert. "
        "Focus on query performance and index usage."
    )
    
    # Same user question, different responses based on system prompt
    question = "How do I select data?"
    
    print("Python Tutor Response:")
    python_tutor.ask(question)  # Will explain Python data selection
    
    print("\nSQL Expert Response:")
    sql_expert.ask(question)     # Will explain SQL SELECT statements