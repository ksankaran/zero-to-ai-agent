# From: AI Agents Book - Chapter 13, Section 13.4
# File: exercise_1_13_4_solution.py
# Exercise: Basic Entity Extraction

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import json

client = OpenAI()

def extract_entities(message):
    """Extract entities from a message using LLM."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"""Extract entities as JSON:
{{"entities": [{{"name": "...", "type": "person|org|project|location", "info": "..."}}]}}

Message: {message}
JSON:"""
        }],
        max_tokens=200
    )
    
    try:
        return json.loads(response.choices[0].message.content)["entities"]
    except:
        return []


# Test
message = "John from marketing wants to discuss the Phoenix project with the Tokyo team next Tuesday."
entities = extract_entities(message)

print("Extracted Entities:")
for e in entities:
    print(f"  - {e['name']} ({e['type']}): {e.get('info', 'N/A')}")
