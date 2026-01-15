# From: Zero to AI Agent, Chapter 19, Section 19.6
# File: exercise_1_19_6_solution.py (smart_router.py)
# Description: Smart model routing with logging and cost tracking

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("model_router")


@dataclass
class RoutingDecision:
    """Record of a routing decision."""
    timestamp: datetime
    message_preview: str
    complexity: str
    model_selected: str
    reason: str
    estimated_cost: float
    baseline_cost: float  # What GPT-4 would have cost


class SmartModelRouter:
    """Route requests to appropriate models based on complexity."""
    
    # Model definitions with costs per 1K tokens (average of input/output)
    MODELS = {
        "simple": {
            "name": "gpt-4o-mini",
            "cost_per_1k": 0.0004,
            "instance": None  # Created on first use
        },
        "medium": {
            "name": "gpt-4o",
            "cost_per_1k": 0.01,
            "instance": None
        },
        "complex": {
            "name": "gpt-4-turbo",
            "cost_per_1k": 0.02,
            "instance": None
        }
    }
    
    BASELINE_COST_PER_1K = 0.02  # GPT-4 Turbo as baseline
    
    def __init__(self):
        self.decisions: List[RoutingDecision] = []
        
        # Create model instances
        for complexity in self.MODELS:
            self.MODELS[complexity]["instance"] = ChatOpenAI(
                model=self.MODELS[complexity]["name"],
                temperature=0.7
            )
    
    def classify_complexity(self, message: str) -> Tuple[str, str]:
        """
        Classify message complexity.
        Returns: (complexity_level, reason)
        """
        message_lower = message.lower()
        word_count = len(message.split())
        
        # Simple patterns
        simple_patterns = [
            "hello", "hi", "hey", "thanks", "thank you", "bye",
            "yes", "no", "ok", "okay", "sure",
            "what time", "what date", "what day",
            "how are you", "good morning", "good night"
        ]
        
        for pattern in simple_patterns:
            if pattern in message_lower:
                return "simple", f"Matched simple pattern: '{pattern}'"
        
        # Complex patterns
        complex_patterns = [
            ("analyze", "Requires analysis"),
            ("compare", "Requires comparison"),
            ("explain why", "Requires reasoning"),
            ("write code", "Code generation"),
            ("debug", "Debugging task"),
            ("evaluate", "Evaluation task"),
            ("create a plan", "Planning task"),
            ("step by step", "Multi-step reasoning"),
            ("pros and cons", "Analysis task"),
            ("summarize this document", "Document processing"),
        ]
        
        for pattern, reason in complex_patterns:
            if pattern in message_lower:
                return "complex", reason
        
        # Medium complexity indicators
        medium_patterns = [
            ("how do i", "How-to question"),
            ("what is", "Explanation request"),
            ("can you help", "Help request"),
            ("explain", "Explanation request"),
            ("describe", "Description request"),
        ]
        
        for pattern, reason in medium_patterns:
            if pattern in message_lower:
                return "medium", reason
        
        # Length-based heuristics
        if word_count < 5:
            return "simple", f"Short message ({word_count} words)"
        elif word_count > 50:
            return "complex", f"Long message ({word_count} words)"
        else:
            return "medium", f"Medium length ({word_count} words)"
    
    def select_model(self, message: str, estimated_tokens: int = 500) -> ChatOpenAI:
        """Select the appropriate model and log the decision."""
        complexity, reason = self.classify_complexity(message)
        
        model_info = self.MODELS[complexity]
        selected_model = model_info["instance"]
        
        # Calculate costs
        estimated_cost = (estimated_tokens / 1000) * model_info["cost_per_1k"]
        baseline_cost = (estimated_tokens / 1000) * self.BASELINE_COST_PER_1K
        savings = baseline_cost - estimated_cost
        
        # Log the decision
        decision = RoutingDecision(
            timestamp=datetime.now(),
            message_preview=message[:50] + "..." if len(message) > 50 else message,
            complexity=complexity,
            model_selected=model_info["name"],
            reason=reason,
            estimated_cost=estimated_cost,
            baseline_cost=baseline_cost
        )
        self.decisions.append(decision)
        
        logger.info(
            f"Routed to {model_info['name']} | "
            f"Complexity: {complexity} | "
            f"Reason: {reason} | "
            f"Savings: ${savings:.4f}"
        )
        
        return selected_model
    
    def get_savings_report(self) -> dict:
        """Generate a report of cost savings."""
        if not self.decisions:
            return {"message": "No requests processed yet"}
        
        total_estimated = sum(d.estimated_cost for d in self.decisions)
        total_baseline = sum(d.baseline_cost for d in self.decisions)
        total_savings = total_baseline - total_estimated
        
        by_complexity = {}
        for complexity in ["simple", "medium", "complex"]:
            decisions = [d for d in self.decisions if d.complexity == complexity]
            by_complexity[complexity] = {
                "count": len(decisions),
                "estimated_cost": round(sum(d.estimated_cost for d in decisions), 4),
                "baseline_cost": round(sum(d.baseline_cost for d in decisions), 4)
            }
        
        return {
            "total_requests": len(self.decisions),
            "total_estimated_cost": round(total_estimated, 4),
            "total_baseline_cost": round(total_baseline, 4),
            "total_savings": round(total_savings, 4),
            "savings_percent": round((total_savings / total_baseline) * 100, 1) if total_baseline > 0 else 0,
            "by_complexity": by_complexity,
            "recent_decisions": [
                {
                    "message": d.message_preview,
                    "complexity": d.complexity,
                    "model": d.model_selected,
                    "reason": d.reason
                }
                for d in self.decisions[-5:]
            ]
        }


# Test the router
if __name__ == "__main__":
    router = SmartModelRouter()
    
    test_messages = [
        "Hi!",
        "Hello, how are you?",
        "Thanks for your help!",
        "What time is it?",
        "What is Python?",
        "How do I create a list in Python?",
        "Can you help me understand recursion?",
        "Explain the difference between lists and tuples",
        "Analyze this code and find the bug: def foo(): return bar",
        "Write code to implement a binary search tree",
        "Compare and contrast REST and GraphQL APIs, explaining the pros and cons of each approach",
        "Create a step-by-step plan for migrating a monolithic application to microservices",
        "Debug this function and explain why it's not working correctly",
        "Evaluate whether we should use PostgreSQL or MongoDB for our application",
        "What are the pros and cons of using Docker?",
        "Bye!",
        "Yes",
        "No thanks",
        "Ok sounds good",
        "Summarize this document and extract the key points for our quarterly review",
    ]
    
    print("=" * 60)
    print("Testing Smart Model Router")
    print("=" * 60)
    
    for msg in test_messages:
        model = router.select_model(msg)
    
    print("\n" + "=" * 60)
    print("Savings Report")
    print("=" * 60)
    
    import json
    print(json.dumps(router.get_savings_report(), indent=2))
