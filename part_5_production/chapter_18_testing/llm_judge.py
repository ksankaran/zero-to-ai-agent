# From: AI Agents Book, Chapter 18, Section 18.3
# File: llm_judge.py
# Description: Use an LLM to evaluate agent responses (LLM-as-Judge pattern)

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


class LLMJudge:
    """Use an LLM to evaluate agent responses."""
    
    def __init__(self, model: str = "gpt-4o"):
        # Use a strong model for evaluation
        self.llm = ChatOpenAI(model=model, temperature=0)
    
    def evaluate(
        self, 
        question: str, 
        response: str, 
        criteria: str,
        reference: str | None = None
    ) -> dict:
        """
        Evaluate a response using LLM judgment.
        
        Args:
            question: The original question/prompt
            response: The agent's response to evaluate
            criteria: What to evaluate (e.g., "accuracy", "helpfulness")
            reference: Optional reference answer for comparison
        """
        system_prompt = """You are an expert evaluator. Your job is to evaluate 
AI assistant responses based on specific criteria.

Be objective and consistent. Provide a score from 1-5 where:
1 = Very poor, fails to meet the criteria
2 = Poor, partially meets criteria with significant issues  
3 = Acceptable, meets basic criteria but has room for improvement
4 = Good, meets criteria well with minor issues
5 = Excellent, fully meets or exceeds criteria

Always respond in this exact format:
SCORE: [1-5]
REASONING: [Your explanation]"""

        evaluation_prompt = f"""Evaluate the following response for {criteria}.

QUESTION: {question}

RESPONSE: {response}
"""
        if reference:
            evaluation_prompt += f"\nREFERENCE ANSWER: {reference}\n"
        
        evaluation_prompt += f"\nEvaluate for: {criteria}"
        
        result = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=evaluation_prompt)
        ])
        
        # Parse the response
        content = result.content
        score = self._extract_score(content)
        reasoning = self._extract_reasoning(content)
        
        return {
            "metric": f"llm_judge_{criteria}",
            "score": score,
            "normalized_score": score / 5.0,  # Normalize to 0-1
            "reasoning": reasoning,
            "passed": score >= 3
        }
    
    def _extract_score(self, content: str) -> int:
        """Extract score from LLM response."""
        for line in content.split('\n'):
            if line.startswith('SCORE:'):
                try:
                    return int(line.split(':')[1].strip())
                except (ValueError, IndexError):
                    pass
        return 3  # Default to middle score if parsing fails
    
    def _extract_reasoning(self, content: str) -> str:
        """Extract reasoning from LLM response."""
        for i, line in enumerate(content.split('\n')):
            if line.startswith('REASONING:'):
                return '\n'.join(content.split('\n')[i:]).replace('REASONING:', '').strip()
        return content


# Example usage
if __name__ == "__main__":
    judge = LLMJudge()
    
    result = judge.evaluate(
        question="What is the capital of France?",
        response="Paris is the capital of France, located on the Seine River.",
        criteria="accuracy",
        reference="Paris"
    )
    
    print(f"Score: {result['score']}/5")
    print(f"Normalized: {result['normalized_score']:.2f}")
    print(f"Passed: {result['passed']}")
    print(f"Reasoning: {result['reasoning']}")
