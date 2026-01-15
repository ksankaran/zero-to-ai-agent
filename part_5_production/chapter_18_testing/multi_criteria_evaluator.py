# From: AI Agents Book, Chapter 18, Section 18.3
# File: multi_criteria_evaluator.py
# Description: Evaluate responses across multiple criteria

from llm_judge import LLMJudge
from semantic_evaluator import SemanticEvaluator


class MultiCriteriaEvaluator:
    """Evaluate responses across multiple criteria."""
    
    def __init__(self):
        self.judge = LLMJudge()
        self.semantic = SemanticEvaluator()
    
    def evaluate(
        self,
        question: str,
        response: str,
        reference: str | None = None,
        criteria: list[str] | None = None
    ) -> dict:
        """Run comprehensive evaluation."""
        
        criteria = criteria or ["accuracy", "helpfulness", "clarity"]
        
        results = {
            "question": question,
            "response": response[:200] + "..." if len(response) > 200 else response,
            "evaluations": {},
            "summary": {}
        }
        
        # Run LLM judge for each criterion
        for criterion in criteria:
            eval_result = self.judge.evaluate(
                question=question,
                response=response,
                criteria=criterion,
                reference=reference
            )
            results["evaluations"][criterion] = eval_result
        
        # Add semantic similarity if reference provided
        if reference:
            semantic_result = self.semantic.evaluate(response, reference)
            results["evaluations"]["semantic_similarity"] = semantic_result
        
        # Calculate summary statistics
        scores = [
            e["normalized_score"] 
            for e in results["evaluations"].values() 
            if "normalized_score" in e
        ]
        
        results["summary"] = {
            "average_score": sum(scores) / len(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
            "all_passed": all(
                e.get("passed", True) 
                for e in results["evaluations"].values()
            )
        }
        
        return results


# Example usage
if __name__ == "__main__":
    evaluator = MultiCriteriaEvaluator()
    
    result = evaluator.evaluate(
        question="How do I reset my password?",
        response="To reset your password, go to Settings > Security > Reset Password. You'll receive an email with a reset link.",
        reference="Navigate to Settings, then Security, and click Reset Password.",
        criteria=["accuracy", "helpfulness", "clarity"]
    )
    
    print("Evaluation Results:")
    print(f"Average Score: {result['summary']['average_score']:.2f}")
    print(f"All Passed: {result['summary']['all_passed']}")
    
    for criterion, eval_data in result["evaluations"].items():
        print(f"  {criterion}: {eval_data.get('normalized_score', eval_data.get('score', 'N/A'))}")
