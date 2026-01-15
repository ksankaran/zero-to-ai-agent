# From: AI Agents Book, Chapter 18, Section 18.3
# File: exercise_2_18_3_solution.py
# Description: Exercise 2 Solution - Comparative evaluator for A/B testing

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


class ComparativeEvaluator:
    """
    Compare two agent responses and determine which is better.
    Useful for A/B testing different agent versions.
    """
    
    def __init__(self, model: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model, temperature=0)
    
    def compare(
        self,
        question: str,
        response_a: str,
        response_b: str,
        criteria: list[str] | None = None,
        context: str | None = None
    ) -> dict:
        """
        Compare two responses and determine which is better.
        
        Args:
            question: The original question/query
            response_a: First response (e.g., from agent version A)
            response_b: Second response (e.g., from agent version B)
            criteria: Specific criteria to compare on
            context: Additional context for evaluation
        
        Returns:
            Comparison result with winner and reasoning
        """
        criteria = criteria or ["accuracy", "helpfulness", "clarity", "completeness"]
        criteria_str = ", ".join(criteria)
        
        system_prompt = f"""You are an expert evaluator comparing two AI assistant responses.

Your task is to determine which response is better based on these criteria: {criteria_str}

Be objective and thorough. Consider all criteria equally unless one response has a critical flaw.

Respond in exactly this format:
WINNER: [A or B or TIE]
CONFIDENCE: [HIGH, MEDIUM, or LOW]
SUMMARY: [One sentence summary of the decision]

RESPONSE_A_STRENGTHS:
- [strength 1]
- [strength 2]

RESPONSE_A_WEAKNESSES:
- [weakness 1]
- [weakness 2]

RESPONSE_B_STRENGTHS:
- [strength 1]
- [strength 2]

RESPONSE_B_WEAKNESSES:
- [weakness 1]
- [weakness 2]

DETAILED_REASONING:
[Paragraph explaining the decision, comparing specific aspects]"""

        comparison_prompt = f"""QUESTION:
{question}

RESPONSE A:
{response_a}

RESPONSE B:
{response_b}
"""
        if context:
            comparison_prompt += f"\nCONTEXT:\n{context}"
        
        comparison_prompt += f"\n\nCompare these responses based on: {criteria_str}"
        
        result = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=comparison_prompt)
        ])
        
        return self._parse_comparison(result.content, response_a, response_b)
    
    def _parse_comparison(self, content: str, response_a: str, response_b: str) -> dict:
        """Parse the comparison result."""
        result = {
            "response_a_preview": response_a[:150] + "..." if len(response_a) > 150 else response_a,
            "response_b_preview": response_b[:150] + "..." if len(response_b) > 150 else response_b,
            "winner": "TIE",
            "confidence": "MEDIUM",
            "summary": "",
            "response_a_strengths": [],
            "response_a_weaknesses": [],
            "response_b_strengths": [],
            "response_b_weaknesses": [],
            "detailed_reasoning": ""
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('WINNER:'):
                winner = line.split(':')[1].strip().upper()
                if winner in ['A', 'B', 'TIE']:
                    result["winner"] = winner
            elif line.startswith('CONFIDENCE:'):
                conf = line.split(':')[1].strip().upper()
                if conf in ['HIGH', 'MEDIUM', 'LOW']:
                    result["confidence"] = conf
            elif line.startswith('SUMMARY:'):
                result["summary"] = line.split(':', 1)[1].strip()
            elif line.startswith('RESPONSE_A_STRENGTHS:'):
                current_section = "response_a_strengths"
            elif line.startswith('RESPONSE_A_WEAKNESSES:'):
                current_section = "response_a_weaknesses"
            elif line.startswith('RESPONSE_B_STRENGTHS:'):
                current_section = "response_b_strengths"
            elif line.startswith('RESPONSE_B_WEAKNESSES:'):
                current_section = "response_b_weaknesses"
            elif line.startswith('DETAILED_REASONING:'):
                current_section = "detailed_reasoning"
            elif line.startswith('- ') and current_section in [
                "response_a_strengths", "response_a_weaknesses",
                "response_b_strengths", "response_b_weaknesses"
            ]:
                result[current_section].append(line[2:])
            elif current_section == "detailed_reasoning" and line:
                result["detailed_reasoning"] += line + " "
        
        result["detailed_reasoning"] = result["detailed_reasoning"].strip()
        
        return result
    
    def batch_compare(
        self,
        comparisons: list[dict]
    ) -> dict:
        """
        Run multiple comparisons and aggregate results.
        
        Args:
            comparisons: List of dicts with 'question', 'response_a', 'response_b'
        
        Returns:
            Aggregated comparison results
        """
        results = []
        a_wins = 0
        b_wins = 0
        ties = 0
        
        for comp in comparisons:
            result = self.compare(
                question=comp["question"],
                response_a=comp["response_a"],
                response_b=comp["response_b"],
                criteria=comp.get("criteria"),
                context=comp.get("context")
            )
            results.append(result)
            
            if result["winner"] == "A":
                a_wins += 1
            elif result["winner"] == "B":
                b_wins += 1
            else:
                ties += 1
        
        total = len(comparisons)
        
        return {
            "individual_results": results,
            "aggregate": {
                "total_comparisons": total,
                "a_wins": a_wins,
                "b_wins": b_wins,
                "ties": ties,
                "a_win_rate": a_wins / total if total > 0 else 0,
                "b_win_rate": b_wins / total if total > 0 else 0,
                "tie_rate": ties / total if total > 0 else 0,
                "recommendation": self._get_recommendation(a_wins, b_wins, ties)
            }
        }
    
    def _get_recommendation(self, a_wins: int, b_wins: int, ties: int) -> str:
        """Generate recommendation based on results."""
        total = a_wins + b_wins + ties
        if total == 0:
            return "No comparisons to analyze"
        
        a_rate = a_wins / total
        b_rate = b_wins / total
        
        if a_rate > 0.6:
            return "Strong preference for Response A (version A recommended)"
        elif b_rate > 0.6:
            return "Strong preference for Response B (version B recommended)"
        elif a_rate > b_rate + 0.1:
            return "Slight preference for Response A (more testing recommended)"
        elif b_rate > a_rate + 0.1:
            return "Slight preference for Response B (more testing recommended)"
        else:
            return "No clear winner (responses are comparable)"


# Example usage
if __name__ == "__main__":
    evaluator = ComparativeEvaluator()
    
    result = evaluator.compare(
        question="How do I reset my password?",
        response_a="Go to settings and click reset password.",
        response_b="To reset your password: 1) Click your profile icon in the top right, 2) Select 'Settings', 3) Under 'Security', click 'Reset Password', 4) Check your email for a reset link. The link expires in 24 hours. Need help? Reply to this message!",
        criteria=["completeness", "clarity", "helpfulness"]
    )
    
    print(f"Winner: {result['winner']} (Confidence: {result['confidence']})")
    print(f"Summary: {result['summary']}")
