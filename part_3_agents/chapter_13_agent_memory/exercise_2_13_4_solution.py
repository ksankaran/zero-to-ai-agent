# From: AI Agents Book - Chapter 13, Section 13.4
# File: exercise_2_13_4_solution.py
# Exercise: Entity Memory Class

from datetime import datetime


class EntityMemory:
    """Store and retrieve entity information."""
    
    def __init__(self):
        self.entities = {}
    
    def update(self, name, entity_type, fact=None):
        """Add or update an entity with new information."""
        key = name.lower()
        if key not in self.entities:
            self.entities[key] = {
                "name": name, 
                "type": entity_type, 
                "facts": [], 
                "mentions": 0
            }
        
        self.entities[key]["mentions"] += 1
        if fact and fact not in self.entities[key]["facts"]:
            self.entities[key]["facts"].append(fact)
    
    def get(self, name):
        """Retrieve entity by name."""
        return self.entities.get(name.lower())
    
    def format_context(self, names):
        """Format specified entities for LLM context."""
        lines = []
        for name in names:
            e = self.get(name)
            if e:
                facts = "; ".join(e["facts"][-3:]) or "no details yet"
                lines.append(f"- {e['name']} ({e['type']}): {facts}")
        return "\n".join(lines) if lines else ""


# Test
memory = EntityMemory()

# Process messages with overlapping entities
memory.update("Sarah Chen", "person", "works in engineering")
memory.update("Project Atlas", "project", "deadline is March 1st")
memory.update("Sarah Chen", "person", "leading the backend team")
memory.update("Project Atlas", "project", "Sarah is the tech lead")
memory.update("Acme Corp", "org", "client for Project Atlas")

# Show results
print("Entity: Sarah Chen")
print(memory.get("sarah chen"))

print("\nContext for Sarah and Atlas:")
print(memory.format_context(["Sarah Chen", "Project Atlas"]))
