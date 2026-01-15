# From: AI Agents Book - Chapter 13, Section 13.4
# File: context_aware_agent.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from entity_memory import EntityMemory
from knowledge_graph import KnowledgeGraph
from entity_extraction import extract_entities


class ContextAwareAgent:
    """
    Agent pattern combining conversation history, entity memory, and knowledge graph.
    This forms the backbone of production AI assistants.
    """
    
    def __init__(self, name, system_prompt):
        self.name = name
        self.client = OpenAI()
        self.system_prompt = system_prompt
        
        # Memory systems
        self.conversation = []
        self.entities = EntityMemory()
        self.graph = KnowledgeGraph()
    
    def build_context(self, user_message):
        """Assemble full context for the agent."""
        # Start with system prompt
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add entity context
        relevant = self.entities.get_relevant_entities(user_message)
        if relevant:
            entity_info = self.entities.format_for_context(relevant)
            messages.append({"role": "system", "content": entity_info})
        
        # Add conversation history (last N messages)
        messages.extend(self.conversation[-20:])
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def run(self, user_message):
        """Main agent loop."""
        # Build context with entity knowledge
        messages = self.build_context(user_message)
        
        # Get response
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        
        # Learn from this exchange
        self._learn(user_message)
        self._learn(reply)
        
        # Update conversation
        self.conversation.append({"role": "user", "content": user_message})
        self.conversation.append({"role": "assistant", "content": reply})
        
        return reply
    
    def _learn(self, text):
        """Extract entities and relationships from text."""
        # Extract entities
        entities = extract_entities(text, self.client)
        for e in entities:
            self.entities.update_entity(e["name"], e["type"], e.get("info"))
        
        # Extract relationships
        self.graph.extract_relationships(text, self.client)
    
    def get_memory_stats(self):
        """Return statistics about what the agent has learned."""
        return {
            "conversation_messages": len(self.conversation),
            "known_entities": len(self.entities.entities),
            "relationships": len(self.graph.relationships)
        }


# Example usage
if __name__ == "__main__":
    agent = ContextAwareAgent(
        name="ProjectBot",
        system_prompt="You are a helpful project management assistant. Track people, projects, and deadlines."
    )
    
    # Simulate a conversation
    messages = [
        "I'm starting a new project called Phoenix with my team lead Maria.",
        "Maria said the deadline is end of Q1. She's also working with Tom on design.",
        "What do you know about the Phoenix project so far?",
        "Who is working on Phoenix?"
    ]
    
    for msg in messages:
        print(f"User: {msg}")
        response = agent.run(msg)
        print(f"Agent: {response}\n")
    
    # Show what was learned
    print("=" * 50)
    print("Memory Stats:", agent.get_memory_stats())
    print("\nKnown Entities:")
    for entity in agent.entities.get_all_entities():
        print(f"  - {entity['name']} ({entity['type']})")
