# From: AI Agents Book - Chapter 13, Section 13.4
# File: entity_extraction.py

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import json


def extract_entities(message, client):
    """Extract entities (people, orgs, projects, locations) from a message."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"""Extract entities from this message. Return JSON:
{{
    "entities": [
        {{"name": "...", "type": "person|org|project|location|concept", "info": "..."}}
    ]
}}

Message: {message}

Return ONLY valid JSON:"""
        }],
        max_tokens=300
    )
    
    try:
        return json.loads(response.choices[0].message.content)["entities"]
    except:
        return []


# Example usage
if __name__ == "__main__":
    client = OpenAI()
    
    test_message = "Tell Sarah Chen to schedule a meeting with the Globex team about the Q4 launch."
    entities = extract_entities(test_message, client)
    
    print("Extracted entities:")
    for e in entities:
        print(f"  - {e['name']} ({e['type']}): {e.get('info', 'N/A')}")
