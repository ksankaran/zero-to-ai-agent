# From: Zero to AI Agent, Chapter 11, Section 11.5
# File: exercise_1_11_5_solution.py

from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv
from datetime import datetime, date
import json

load_dotenv()

class CostTrackingAssistant:
    def __init__(self, daily_budget=1.0):
        self.daily_budget = daily_budget
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Cost per 1000 tokens (approximate)
        self.costs = {
            "gpt-3.5-turbo": 0.002,
            "gpt-4": 0.06,
            "llama2": 0.0  # Free local model
        }
        
        # Usage tracking
        self.daily_usage = {}
        self.conversation_costs = []
        self.current_conversation_cost = 0.0
        
        # Initialize models
        self.models = {
            "gpt-3.5-turbo": ChatOpenAI(model="gpt-3.5-turbo"),
            "gpt-4": ChatOpenAI(model="gpt-4"),
            "llama2": Ollama(model="llama2")
        }
        
        self.current_model = "gpt-3.5-turbo"
    
    def get_today_spent(self):
        """Get today's total spending"""
        today = date.today().isoformat()
        return self.daily_usage.get(today, 0.0)
    
    def select_model_by_budget(self):
        """Select model based on remaining budget"""
        today_spent = self.get_today_spent()
        remaining = self.daily_budget - today_spent
        
        if remaining <= 0:
            # No budget left, use free model
            self.current_model = "llama2"
            print(f"💰 Budget exhausted! Switching to free local model.")
        elif remaining < 0.1:
            # Low budget, use cheapest
            self.current_model = "gpt-3.5-turbo"
            print(f"⚠️ Low budget (${remaining:.3f} left). Using GPT-3.5.")
        elif remaining > 0.5:
            # Good budget, can use better model for important queries
            self.current_model = "gpt-3.5-turbo"  # Default to efficient
            print(f"✅ Budget available: ${remaining:.3f}")
        
        return self.current_model
    
    def estimate_cost(self, text, model_name):
        """Estimate cost for a query"""
        # Rough token estimation
        tokens = len(text.split()) * 1.5  # Approximate
        cost = (tokens / 1000) * self.costs[model_name]
        return cost
    
    def chat(self, message, important=False):
        """Chat with cost tracking"""
        
        # Select model based on budget and importance
        if important and self.get_today_spent() < (self.daily_budget * 0.7):
            # Use better model for important queries if budget allows
            self.current_model = "gpt-4"
            print(f"📌 Using GPT-4 for important query")
        else:
            self.select_model_by_budget()
        
        # Get model
        model = self.models[self.current_model]
        
        # Process message
        try:
            response = model.invoke(message)
            
            # Extract content
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            # Calculate cost
            estimated_cost = self.estimate_cost(message + content, self.current_model)
            
            # Track usage
            today = date.today().isoformat()
            if today not in self.daily_usage:
                self.daily_usage[today] = 0.0
            self.daily_usage[today] += estimated_cost
            
            self.current_conversation_cost += estimated_cost
            
            # Show cost
            print(f"💵 Cost: ${estimated_cost:.5f} | Today: ${self.daily_usage[today]:.4f}")
            
            return content
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return "Error processing request"
    
    def end_conversation(self):
        """End current conversation and record cost"""
        if self.current_conversation_cost > 0:
            self.conversation_costs.append({
                "timestamp": datetime.now().isoformat(),
                "cost": self.current_conversation_cost,
                "model": self.current_model
            })
            
            cost = self.current_conversation_cost
            self.current_conversation_cost = 0.0
            return f"Conversation cost: ${cost:.4f}"
        return "No conversation to end"
    
    def daily_report(self):
        """Generate daily spending report"""
        report = {
            "date": date.today().isoformat(),
            "budget": self.daily_budget,
            "spent": self.get_today_spent(),
            "remaining": self.daily_budget - self.get_today_spent(),
            "conversations": len(self.conversation_costs),
            "average_cost": sum(c["cost"] for c in self.conversation_costs) / len(self.conversation_costs) if self.conversation_costs else 0,
            "model_usage": {}
        }
        
        # Count model usage
        for conv in self.conversation_costs:
            model = conv.get("model", "unknown")
            if model not in report["model_usage"]:
                report["model_usage"][model] = 0
            report["model_usage"][model] += 1
        
        return report
    
    def spending_alert(self):
        """Check spending and alert if needed"""
        spent_percentage = (self.get_today_spent() / self.daily_budget) * 100
        
        if spent_percentage >= 100:
            return "🔴 BUDGET EXCEEDED! Using free models only."
        elif spent_percentage >= 90:
            return "🟡 WARNING: 90% of budget used!"
        elif spent_percentage >= 75:
            return "🟠 CAUTION: 75% of budget used."
        else:
            return f"🟢 Budget healthy: {spent_percentage:.1f}% used"

# Test the cost tracking assistant
def demo_cost_tracking():
    assistant = CostTrackingAssistant(daily_budget=0.50)
    
    # Simulate conversations
    queries = [
        ("What is Python?", False),
        ("Explain quantum computing in detail", True),  # Important
        ("How's the weather?", False),
        ("Write a business plan", True),  # Important
        ("Tell me a joke", False)
    ]
    
    print("💰 Cost-Aware Assistant Demo")
    print("="*60)
    
    for query, important in queries:
        print(f"\n❓ Query: {query}")
        print(f"   Important: {important}")
        
        response = assistant.chat(query, important)
        print(f"   Response: {response[:100]}...")
        print(f"   Alert: {assistant.spending_alert()}")
        
        # End conversation after each query for demo
        print(f"   {assistant.end_conversation()}")
    
    # Show daily report
    print("\n" + "="*60)
    print("📊 DAILY REPORT:")
    report = assistant.daily_report()
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    demo_cost_tracking()
