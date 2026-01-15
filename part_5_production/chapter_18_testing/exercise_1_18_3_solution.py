# From: AI Agents Book, Chapter 18, Section 18.3
# File: exercise_1_18_3_solution.py
# Description: Exercise 1 Solution - Customer service evaluator with 4 criteria

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


class CustomerServiceEvaluator:
    """
    Evaluate customer service agent responses across four criteria:
    - Accuracy: Factual correctness of information provided
    - Empathy: Emotional tone and understanding
    - Actionability: Does it help solve the problem?
    - Policy Compliance: Stays within company guidelines
    """
    
    def __init__(self, model: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model, temperature=0)
        
        # Define the rubric for each criterion
        self.rubrics = {
            "accuracy": """
Evaluate the ACCURACY of the response - is the information factually correct?

1 = Contains significant factual errors or misinformation
2 = Contains some inaccuracies that could mislead the customer
3 = Mostly accurate with minor errors that don't affect the outcome
4 = Accurate information with only trivial imprecisions
5 = Completely accurate, all facts verified and correct
""",
            "empathy": """
Evaluate the EMPATHY of the response - does it show understanding and care?

1 = Cold, dismissive, or robotic with no acknowledgment of customer feelings
2 = Minimal acknowledgment, feels scripted and impersonal
3 = Adequate acknowledgment but could be warmer
4 = Warm and understanding, makes customer feel heard
5 = Exceptional empathy, perfectly balances professionalism with genuine care
""",
            "actionability": """
Evaluate the ACTIONABILITY of the response - does it help solve the problem?

1 = No clear next steps, customer left confused about what to do
2 = Vague suggestions that don't directly address the issue
3 = Some helpful guidance but incomplete or unclear
4 = Clear, specific steps that should resolve the issue
5 = Comprehensive solution with alternatives and proactive help
""",
            "policy_compliance": """
Evaluate POLICY COMPLIANCE - does the response stay within appropriate boundaries?

1 = Violates policies (unauthorized promises, shares restricted info, etc.)
2 = Bends rules inappropriately or makes questionable commitments
3 = Follows policies but rigidly, missing opportunities to help within bounds
4 = Good policy adherence while still being helpful
5 = Perfect balance of policy compliance and customer advocacy
"""
        }
    
    def evaluate(
        self,
        customer_query: str,
        agent_response: str,
        context: dict | None = None
    ) -> dict:
        """
        Evaluate a customer service response across all criteria.
        
        Args:
            customer_query: The customer's original message
            agent_response: The agent's response to evaluate
            context: Optional context (e.g., company policies, customer history)
        
        Returns:
            Comprehensive evaluation with scores and feedback
        """
        results = {
            "customer_query": customer_query,
            "agent_response": agent_response[:300] + "..." if len(agent_response) > 300 else agent_response,
            "criteria_scores": {},
            "detailed_feedback": {},
            "summary": {}
        }
        
        context_str = ""
        if context:
            context_str = f"\n\nCONTEXT:\n{self._format_context(context)}"
        
        # Evaluate each criterion
        for criterion, rubric in self.rubrics.items():
            score, feedback = self._evaluate_criterion(
                customer_query=customer_query,
                agent_response=agent_response,
                criterion=criterion,
                rubric=rubric,
                context_str=context_str
            )
            results["criteria_scores"][criterion] = score
            results["detailed_feedback"][criterion] = feedback
        
        # Calculate summary
        scores = list(results["criteria_scores"].values())
        results["summary"] = {
            "average_score": sum(scores) / len(scores),
            "lowest_criterion": min(results["criteria_scores"], key=results["criteria_scores"].get),
            "highest_criterion": max(results["criteria_scores"], key=results["criteria_scores"].get),
            "passed": all(s >= 3 for s in scores),
            "needs_improvement": [c for c, s in results["criteria_scores"].items() if s < 3]
        }
        
        return results
    
    def _evaluate_criterion(
        self,
        customer_query: str,
        agent_response: str,
        criterion: str,
        rubric: str,
        context_str: str
    ) -> tuple[int, str]:
        """Evaluate a single criterion using LLM."""
        
        system_prompt = f"""You are an expert evaluator for customer service interactions.
Your task is to evaluate responses based on specific criteria.

{rubric}

Respond in exactly this format:
SCORE: [1-5]
FEEDBACK: [Specific feedback explaining the score with examples from the response]
SUGGESTION: [One specific way to improve, if score < 5]"""

        evaluation_prompt = f"""CUSTOMER QUERY:
{customer_query}

AGENT RESPONSE:
{agent_response}
{context_str}

Evaluate this response for {criterion.upper()}."""

        result = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=evaluation_prompt)
        ])
        
        # Parse response
        content = result.content
        score = self._extract_score(content)
        feedback = self._extract_section(content, "FEEDBACK:")
        suggestion = self._extract_section(content, "SUGGESTION:")
        
        full_feedback = feedback
        if suggestion and score < 5:
            full_feedback += f"\n\nSuggestion: {suggestion}"
        
        return score, full_feedback
    
    def _extract_score(self, content: str) -> int:
        """Extract numeric score from response."""
        for line in content.split('\n'):
            if line.strip().startswith('SCORE:'):
                try:
                    return int(line.split(':')[1].strip().split()[0])
                except (ValueError, IndexError):
                    pass
        return 3
    
    def _extract_section(self, content: str, header: str) -> str:
        """Extract a section from the response."""
        lines = content.split('\n')
        capture = False
        result = []
        
        for line in lines:
            if line.strip().startswith(header):
                capture = True
                result.append(line.split(':', 1)[1].strip() if ':' in line else '')
            elif capture and line.strip().startswith(('SCORE:', 'FEEDBACK:', 'SUGGESTION:')):
                break
            elif capture:
                result.append(line)
        
        return ' '.join(result).strip()
    
    def _format_context(self, context: dict) -> str:
        """Format context dictionary as string."""
        lines = []
        for key, value in context.items():
            lines.append(f"- {key}: {value}")
        return '\n'.join(lines)


# Example usage and test
if __name__ == "__main__":
    evaluator = CustomerServiceEvaluator()
    
    # Test case
    result = evaluator.evaluate(
        customer_query="I ordered a laptop 2 weeks ago and it still hasn't arrived. This is ridiculous! I need it for work!",
        agent_response="I understand how frustrating this must be, especially when you need the laptop for work. Let me look into this right away. I can see your order #12345 was shipped on the 5th. It appears there's been a delay at the carrier's hub. I'm going to: 1) Contact the carrier directly to expedite delivery, 2) Send you tracking updates every 24 hours, and 3) If it's not delivered by Friday, I'll arrange for a replacement with overnight shipping at no extra cost. Does that work for you?",
        context={
            "company_policy": "Can offer replacement or refund after 14 days of delay",
            "customer_tier": "Premium member"
        }
    )
    
    print("Evaluation Results:")
    print(f"Scores: {result['criteria_scores']}")
    print(f"Average: {result['summary']['average_score']:.2f}")
    print(f"Passed: {result['summary']['passed']}")
