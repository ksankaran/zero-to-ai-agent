# From: AI Agents Book - Chapter 13, Section 13.4
# File: entity_aware_agent.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from entity_memory import EntityMemory
from entity_extraction import extract_entities


class EntityAwareAgent:
    """An agent that automatically learns and recalls entity information."""
    
    def __init__(self, system_prompt):
        self.client = OpenAI()
        self.entity_memory = EntityMemory()
        self.conversation = [{"role": "system", "content": system_prompt}]
    
    def process_message(self, user_message):
        # 1. RETRIEVE: Find relevant entities
        relevant = self.entity_memory.get_relevant_entities(user_message)
        entity_context = self.entity_memory.format_for_context(relevant)
        
        # 2. BUILD CONTEXT: Inject entity knowledge
        messages = self.conversation.copy()
        if entity_context:
            messages.insert(1, {
                "role": "system", 
                "content": entity_context
            })
        messages.append({"role": "user", "content": user_message})
        
        # 3. REASON & ACT: Get agent response
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        
        # 4. STORE: Extract and save new entities
        self._extract_and_store(user_message)
        self._extract_and_store(reply)
        
        # Update conversation
        self.conversation.append({"role": "user", "content": user_message})
        self.conversation.append({"role": "assistant", "content": reply})
        
        return reply
    
    def _extract_and_store(self, text):
        """Extract entities from text and update memory."""
        entities = extract_entities(text, self.client)
        for e in entities:
            self.entity_memory.update_entity(
                e["name"], e["type"], e.get("info", "")
            )
    
    def get_known_entities(self):
        """Return all entities the agent knows about."""
        return self.entity_memory.get_all_entities()


# Example usage
if __name__ == "__main__":
    agent = EntityAwareAgent(
        system_prompt="You are a helpful project management assistant."
    )
    
    # Have a conversation
    print("User: I'm working with Sarah Chen on the Q4 Launch project.")
    response = agent.process_message("I'm working with Sarah Chen on the Q4 Launch project.")
    print(f"Agent: {response}\n")
    
    print("User: Sarah said the deadline is December 15th.")
    response = agent.process_message("Sarah said the deadline is December 15th.")
    print(f"Agent: {response}\n")
    
    # Show what the agent learned
    print("Known entities:")
    for entity in agent.get_known_entities():
        print(f"  - {entity['name']} ({entity['type']}): {entity['facts']}")
