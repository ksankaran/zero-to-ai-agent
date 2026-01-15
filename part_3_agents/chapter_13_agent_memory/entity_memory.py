# From: AI Agents Book - Chapter 13, Section 13.4
# File: entity_memory.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from datetime import datetime


class EntityMemory:
    """Store and retrieve entity information from conversations."""
    
    def __init__(self):
        self.entities = {}  # name -> entity data
        self.client = OpenAI()
    
    def update_entity(self, name, entity_type, new_info):
        """Add or update an entity with new information."""
        name_key = name.lower().strip()
        
        if name_key not in self.entities:
            self.entities[name_key] = {
                "name": name,
                "type": entity_type,
                "facts": [],
                "first_seen": datetime.now().isoformat(),
                "mention_count": 0
            }
        
        entity = self.entities[name_key]
        entity["mention_count"] += 1
        entity["last_seen"] = datetime.now().isoformat()
        
        # Add new fact if not duplicate
        if new_info and new_info not in entity["facts"]:
            entity["facts"].append(new_info)
    
    def get_entity(self, name):
        """Retrieve entity by name."""
        return self.entities.get(name.lower().strip())
    
    def get_relevant_entities(self, message):
        """Find entities mentioned in a message."""
        relevant = []
        message_lower = message.lower()
        
        for key, entity in self.entities.items():
            if key in message_lower or entity["name"].lower() in message_lower:
                relevant.append(entity)
        
        return relevant
    
    def format_for_context(self, entities):
        """Format entities for injection into LLM context."""
        if not entities:
            return ""
        
        lines = ["Relevant information about mentioned entities:"]
        for e in entities:
            facts = "; ".join(e["facts"][-5:])  # Last 5 facts
            lines.append(f"- {e['name']} ({e['type']}): {facts}")
        
        return "\n".join(lines)
    
    def get_all_entities(self):
        """Return all stored entities."""
        return list(self.entities.values())


# Example usage
if __name__ == "__main__":
    memory = EntityMemory()
    
    # Add some entities
    memory.update_entity("Sarah Chen", "person", "Account Manager at Acme")
    memory.update_entity("Sarah Chen", "person", "prefers Slack over email")
    memory.update_entity("Globex", "org", "major client")
    memory.update_entity("Q4 Launch", "project", "deadline is December 15")
    
    # Retrieve
    print("Sarah's info:", memory.get_entity("sarah chen"))
    
    # Find relevant entities in a message
    relevant = memory.get_relevant_entities("What's the status of Q4 Launch?")
    print("\nRelevant entities:")
    print(memory.format_for_context(relevant))
