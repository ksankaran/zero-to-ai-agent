# From: AI Agents Book - Chapter 13, Section 13.4
# File: exercise_3_13_4_solution.py
# Exercise: Entity-Aware Agent

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import json

client = OpenAI()


class EntityAgent:
    """Simple agent that learns and recalls entity information."""
    
    def __init__(self):
        self.history = []
        self.entities = {}
    
    def extract_entities(self, text):
        """Extract entities from text using LLM."""
        try:
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user", 
                    "content": f'Extract entities as JSON: {{"entities": [{{"name":"...","type":"...","info":"..."}}]}} from: {text}'
                }],
                max_tokens=150
            )
            return json.loads(resp.choices[0].message.content).get("entities", [])
        except:
            return []
    
    def store_entities(self, text):
        """Extract and store entities from text."""
        for e in self.extract_entities(text):
            key = e["name"].lower()
            if key not in self.entities:
                self.entities[key] = {
                    "name": e["name"], 
                    "type": e["type"], 
                    "facts": []
                }
            if e.get("info"):
                self.entities[key]["facts"].append(e["info"])
    
    def get_context(self, message):
        """Build context from relevant entities."""
        context = []
        for key, e in self.entities.items():
            if key in message.lower():
                context.append(f"{e['name']}: {'; '.join(e['facts'][-3:])}")
        return "Known info: " + " | ".join(context) if context else ""
    
    def chat(self, user_input):
        """Process user input and return response."""
        # Handle "what do you know" queries
        if "what do you know about" in user_input.lower():
            name = user_input.lower().split("what do you know about")[-1].strip().rstrip("?")
            e = self.entities.get(name)
            if e:
                return f"I know {e['name']} is a {e['type']}. Facts: {'; '.join(e['facts']) or 'none yet'}"
            return f"I don't have information about '{name}' yet."
        
        # Build messages with entity context
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        context = self.get_context(user_input)
        if context:
            messages.append({"role": "system", "content": context})
        messages.extend(self.history[-10:])
        messages.append({"role": "user", "content": user_input})
        
        # Get response
        resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        reply = resp.choices[0].message.content
        
        # Learn and store
        self.store_entities(user_input)
        self.store_entities(reply)
        self.history.extend([
            {"role": "user", "content": user_input}, 
            {"role": "assistant", "content": reply}
        ])
        
        return reply


# Test
agent = EntityAgent()

print("Testing Entity-Aware Agent")
print("=" * 50)

print("\nUser: I'm working with Maria on the Sunrise project. She handles design.")
print(f"Agent: {agent.chat('I am working with Maria on the Sunrise project. She handles design.')}")

print("\nUser: The Sunrise project is due next Friday.")
print(f"Agent: {agent.chat('The Sunrise project is due next Friday.')}")

print("\nUser: What do you know about Maria?")
print(f"Agent: {agent.chat('What do you know about Maria?')}")

print("\nUser: What do you know about Sunrise project?")
print(f"Agent: {agent.chat('What do you know about Sunrise project?')}")
