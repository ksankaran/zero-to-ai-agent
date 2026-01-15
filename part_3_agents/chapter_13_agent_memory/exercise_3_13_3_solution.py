# From: AI Agents Book - Chapter 13, Section 13.3
# File: exercise_3_13_3_solution.py
# Exercise: Domain-Specific Medical Summaries

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import json

client = OpenAI()

class MedicalConsultationMemory:
    def __init__(self):
        self.messages = [{
            "role": "system",
            "content": """You are a medical consultation assistant. Help users 
understand their symptoms and provide general health guidance. Always recommend 
consulting a healthcare professional for diagnosis and treatment."""
        }]
        self.medical_summary = {
            "symptoms": [],
            "duration": None,
            "medications_discussed": [],
            "recommendations": [],
            "follow_up_items": []
        }
        self.summary_generated = False
    
    def _extract_medical_info(self, conversation_messages):
        """Extract structured medical information from conversation."""
        text = "\n".join(
            f"{m['role'].upper()}: {m['content']}" 
            for m in conversation_messages
        )
        
        extraction_prompt = f"""Analyze this medical consultation and extract information 
into the following JSON structure. Only include information explicitly mentioned.

CONVERSATION:
{text}

Extract into this exact JSON format:
{{
    "symptoms": ["list of symptoms mentioned"],
    "duration": "how long symptoms have been present, or null",
    "medications_discussed": ["medications mentioned"],
    "recommendations": ["advice or recommendations given"],
    "follow_up_items": ["things to monitor, tests to take, when to return"]
}}

Return ONLY valid JSON:"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": extraction_prompt}],
            max_tokens=500
        )
        
        try:
            # Parse JSON from response
            json_str = response.choices[0].message.content.strip()
            # Handle potential markdown code blocks
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    
    def _generate_summary_text(self):
        """Generate prose summary from structured data."""
        s = self.medical_summary
        
        parts = []
        if s["symptoms"]:
            parts.append(f"Symptoms: {', '.join(s['symptoms'])}")
        if s["duration"]:
            parts.append(f"Duration: {s['duration']}")
        if s["medications_discussed"]:
            parts.append(f"Medications discussed: {', '.join(s['medications_discussed'])}")
        if s["recommendations"]:
            parts.append(f"Recommendations: {'; '.join(s['recommendations'])}")
        if s["follow_up_items"]:
            parts.append(f"Follow-up: {'; '.join(s['follow_up_items'])}")
        
        return " | ".join(parts) if parts else "No medical information extracted yet."
    
    def _validate_summary(self, new_data):
        """Ensure key medical info isn't lost when updating summary."""
        # Merge rather than replace - never lose symptom data
        if new_data:
            for symptom in new_data.get("symptoms", []):
                if symptom not in self.medical_summary["symptoms"]:
                    self.medical_summary["symptoms"].append(symptom)
            
            if new_data.get("duration"):
                self.medical_summary["duration"] = new_data["duration"]
            
            for med in new_data.get("medications_discussed", []):
                if med not in self.medical_summary["medications_discussed"]:
                    self.medical_summary["medications_discussed"].append(med)
            
            for rec in new_data.get("recommendations", []):
                if rec not in self.medical_summary["recommendations"]:
                    self.medical_summary["recommendations"].append(rec)
            
            for item in new_data.get("follow_up_items", []):
                if item not in self.medical_summary["follow_up_items"]:
                    self.medical_summary["follow_up_items"].append(item)
    
    def chat(self, user_input):
        """Process user input and update medical summary."""
        self.messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        
        # Extract and validate medical info after each exchange
        conversation = [m for m in self.messages if m["role"] != "system"]
        extracted = self._extract_medical_info(conversation[-4:])  # Last 2 exchanges
        self._validate_summary(extracted)
        
        return reply
    
    def get_medical_summary(self):
        """Return structured medical summary."""
        return {
            "structured_data": self.medical_summary,
            "text_summary": self._generate_summary_text(),
            "message_count": len([m for m in self.messages if m["role"] != "system"])
        }


# Test with mock consultation
consultation = MedicalConsultationMemory()

test_conversation = [
    "I've been having headaches for about a week now.",
    "They're mostly in the front of my head, kind of a pressure feeling.",
    "I've been taking ibuprofen but it only helps temporarily.",
    "I also noticed I'm more tired than usual.",
    "Could it be related to stress? I've had a lot going on at work.",
    "What else should I try besides ibuprofen?",
    "Should I see a doctor about this?"
]

print("MEDICAL CONSULTATION SIMULATION")
print("=" * 50)

for user_input in test_conversation:
    print(f"\nPatient: {user_input}")
    response = consultation.chat(user_input)
    print(f"Assistant: {response[:150]}...")

# Display final medical summary
print("\n" + "=" * 50)
print("MEDICAL SUMMARY")
print("=" * 50)

summary = consultation.get_medical_summary()

print("\nSTRUCTURED DATA:")
for key, value in summary["structured_data"].items():
    print(f"  {key}: {value}")

print(f"\nTEXT SUMMARY:\n  {summary['text_summary']}")
print(f"\nTotal exchanges: {summary['message_count'] // 2}")
