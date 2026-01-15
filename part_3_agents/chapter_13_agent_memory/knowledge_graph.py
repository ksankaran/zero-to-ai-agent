# From: AI Agents Book - Chapter 13, Section 13.4
# File: knowledge_graph.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from datetime import datetime
import json


class KnowledgeGraph:
    """Store entities and their relationships."""
    
    def __init__(self):
        self.entities = {}      # name -> attributes
        self.relationships = [] # (entity1, relation, entity2)
    
    def add_entity(self, name, entity_type, attributes=None):
        """Add or update an entity."""
        key = name.lower()
        if key not in self.entities:
            self.entities[key] = {
                "name": name,
                "type": entity_type,
                "attributes": attributes or {}
            }
        elif attributes:
            self.entities[key]["attributes"].update(attributes)
    
    def add_relationship(self, entity1, relation, entity2):
        """Add a relationship between entities."""
        self.relationships.append({
            "from": entity1.lower(),
            "relation": relation,
            "to": entity2.lower(),
            "added": datetime.now().isoformat()
        })
    
    def get_connections(self, entity_name):
        """Get all relationships involving an entity."""
        name = entity_name.lower()
        connections = []
        
        for rel in self.relationships:
            if rel["from"] == name:
                connections.append(f"{rel['relation']} {rel['to']}")
            elif rel["to"] == name:
                connections.append(f"{rel['from']} {rel['relation']} this")
        
        return connections
    
    def extract_relationships(self, message, client):
        """Use LLM to extract relationships from text."""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"""Extract relationships from this message.
Return JSON: {{"relationships": [{{"from": "...", "relation": "...", "to": "..."}}]}}

Examples of relations: works_on, manages, reports_to, is_part_of, depends_on, located_in

Message: {message}
JSON:"""
            }],
            max_tokens=200
        )
        
        try:
            data = json.loads(response.choices[0].message.content)
            for rel in data.get("relationships", []):
                self.add_relationship(rel["from"], rel["relation"], rel["to"])
        except:
            pass
    
    def format_graph(self):
        """Return a formatted string representation of the graph."""
        lines = ["Entities:"]
        for key, entity in self.entities.items():
            lines.append(f"  - {entity['name']} ({entity['type']})")
        
        lines.append("\nRelationships:")
        for rel in self.relationships:
            lines.append(f"  - {rel['from']} --{rel['relation']}--> {rel['to']}")
        
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    client = OpenAI()
    graph = KnowledgeGraph()
    
    # Add entities
    graph.add_entity("Sarah Chen", "person", {"role": "Engineer"})
    graph.add_entity("Q4 Launch", "project")
    graph.add_entity("Acme Corp", "org")
    
    # Add relationships manually
    graph.add_relationship("Sarah Chen", "works_on", "Q4 Launch")
    graph.add_relationship("Q4 Launch", "is_for", "Acme Corp")
    
    # Extract relationships from text
    graph.extract_relationships(
        "The marketing team reports to Jennifer, who manages the NYC office.",
        client
    )
    
    print(graph.format_graph())
    print("\nConnections for Sarah Chen:", graph.get_connections("Sarah Chen"))
