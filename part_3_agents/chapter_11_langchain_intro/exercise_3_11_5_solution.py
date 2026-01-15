# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: exercise_3_11_5_solution.py

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import re
from datetime import datetime
import json

load_dotenv()

class PrivacyGuardianAssistant:
    def __init__(self):
        # Models
        self.cloud_model = ChatOpenAI(model="gpt-3.5-turbo")
        self.local_model = Ollama(model="llama2")
        
        # Privacy patterns
        self.pii_patterns = {
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            "address": r'\d+\s+[\w\s]+\s+(Street|St|Avenue|Ave|Road|Rd|Lane|Ln)',
            "medical": r'\b(diagnosis|prescription|medical|health condition|symptoms)\b',
            "financial": r'\b(bank account|salary|income|tax|financial)\b'
        }
        
        # Audit log
        self.audit_log = []
    
    def detect_private_info(self, text):
        """Detect if text contains private information"""
        detected = []
        
        # Check for PII patterns
        for info_type, pattern in self.pii_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                detected.append(info_type)
        
        # Check for sensitive keywords
        sensitive_keywords = [
            "password", "secret", "private", "confidential",
            "personal", "medical", "health", "diagnosis",
            "salary", "income", "bank", "account"
        ]
        
        text_lower = text.lower()
        for keyword in sensitive_keywords:
            if keyword in text_lower:
                detected.append(f"keyword:{keyword}")
        
        return detected
    
    def anonymize_text(self, text):
        """Remove or mask private information"""
        anonymized = text
        
        # Replace patterns with masks
        replacements = {
            "ssn": "[SSN REMOVED]",
            "phone": "[PHONE REMOVED]",
            "email": "[EMAIL REMOVED]",
            "credit_card": "[CARD REMOVED]",
            "address": "[ADDRESS REMOVED]"
        }
        
        for info_type, pattern in self.pii_patterns.items():
            if info_type in replacements:
                anonymized = re.sub(pattern, replacements[info_type], 
                                   anonymized, flags=re.IGNORECASE)
        
        return anonymized
    
    def select_model(self, text):
        """Select appropriate model based on privacy"""
        private_info = self.detect_private_info(text)
        
        if private_info:
            return "local", private_info
        else:
            return "cloud", []
    
    def process_query(self, query):
        """Process query with privacy protection"""
        
        # Detect private information
        model_choice, private_info = self.select_model(query)
        
        # Log the decision
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query_length": len(query),
            "model_used": model_choice,
            "private_info_detected": private_info,
            "query_hash": hash(query)  # Store hash, not actual query
        }
        
        self.audit_log.append(log_entry)
        
        # Inform user
        if model_choice == "local":
            print(f"🔒 Private information detected: {', '.join(private_info)}")
            print("   Using local model for privacy protection")
            
            # Use local model
            model = self.local_model
            
            # Process locally
            response = model.invoke(query)
            
            result = {
                "model": "local",
                "response": str(response),
                "privacy_protected": True
            }
            
        else:
            print("☁️ No private information detected")
            print("   Using cloud model for better performance")
            
            # Anonymize just in case
            safe_query = self.anonymize_text(query)
            
            # Use cloud model
            model = self.cloud_model
            response = model.invoke(safe_query)
            
            result = {
                "model": "cloud",
                "response": response.content,
                "privacy_protected": False
            }
        
        return result
    
    def get_audit_summary(self):
        """Get summary of model usage"""
        if not self.audit_log:
            return "No queries processed yet"
        
        total = len(self.audit_log)
        local_count = sum(1 for log in self.audit_log if log["model_used"] == "local")
        cloud_count = total - local_count
        
        # Count types of private info detected
        private_info_counts = {}
        for log in self.audit_log:
            for info in log["private_info_detected"]:
                private_info_counts[info] = private_info_counts.get(info, 0) + 1
        
        summary = {
            "total_queries": total,
            "local_model_used": local_count,
            "cloud_model_used": cloud_count,
            "privacy_protection_rate": (local_count / total * 100) if total > 0 else 0,
            "private_info_types": private_info_counts
        }
        
        return summary
    
    def export_audit_log(self, filename="audit_log.json"):
        """Export audit log for compliance"""
        with open(filename, 'w') as f:
            json.dump(self.audit_log, f, indent=2)
        return f"Audit log exported to {filename}"

# Test the privacy guardian
def demo_privacy_guardian():
    guardian = PrivacyGuardianAssistant()
    
    # Test queries with different privacy levels
    test_queries = [
        "What is the weather like today?",  # Safe
        "My SSN is 123-45-6789, is this format correct?",  # Private
        "How do I improve my credit score?",  # Potentially sensitive
        "My email is john@example.com",  # Private
        "What are the symptoms of flu?",  # Medical - sensitive
        "Tell me about Python programming",  # Safe
        "My bank account number is 1234567890",  # Private
        "What's the capital of France?"  # Safe
    ]
    
    print("🔒 Privacy Guardian Assistant Demo")
    print("="*60)
    
    for query in test_queries:
        print(f"\n❓ Query: {query[:50]}...")
        result = guardian.process_query(query)
        print(f"📝 Response: {result['response'][:100]}...")
        print(f"   Model: {result['model']}")
        print(f"   Protected: {result['privacy_protected']}")
    
    # Show audit summary
    print("\n" + "="*60)
    print("📊 AUDIT SUMMARY:")
    summary = guardian.get_audit_summary()
    print(json.dumps(summary, indent=2))
    
    # Export audit log
    print(f"\n📁 {guardian.export_audit_log()}")

if __name__ == "__main__":
    demo_privacy_guardian()
