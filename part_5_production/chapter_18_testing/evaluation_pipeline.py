# From: AI Agents Book, Chapter 18, Section 18.3
# File: evaluation_pipeline.py
# Description: Run systematic evaluations across test cases

from dataclasses import dataclass
from datetime import datetime
import json

from multi_criteria_evaluator import MultiCriteriaEvaluator
from tool_usage_evaluator import ToolUsageEvaluator


@dataclass
class EvaluationCase:
    """A single evaluation test case."""
    id: str
    question: str
    expected_response: str | None = None
    expected_tools: list[str] | None = None
    criteria: list[str] | None = None
    metadata: dict | None = None


class EvaluationPipeline:
    """Run systematic evaluations across test cases."""
    
    def __init__(self, agent_fn):
        """
        Initialize with a function that takes a question and returns a response.
        
        agent_fn should return a dict with at least:
        - "response": str
        - "tools_used": list[str] (optional)
        """
        self.agent_fn = agent_fn
        self.multi_evaluator = MultiCriteriaEvaluator()
        self.tool_evaluator = ToolUsageEvaluator()
    
    def run(self, test_cases: list[EvaluationCase]) -> dict:
        """Run evaluation on all test cases."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_cases": len(test_cases),
            "cases": [],
            "aggregate": {}
        }
        
        all_scores = []
        passed_count = 0
        
        for case in test_cases:
            case_result = self._evaluate_case(case)
            results["cases"].append(case_result)
            
            if case_result["summary"]["all_passed"]:
                passed_count += 1
            
            all_scores.append(case_result["summary"]["average_score"])
        
        # Aggregate statistics
        results["aggregate"] = {
            "pass_rate": passed_count / len(test_cases) if test_cases else 0,
            "average_score": sum(all_scores) / len(all_scores) if all_scores else 0,
            "passed_count": passed_count,
            "failed_count": len(test_cases) - passed_count
        }
        
        return results
    
    def _evaluate_case(self, case: EvaluationCase) -> dict:
        """Evaluate a single test case."""
        # Get agent response
        agent_result = self.agent_fn(case.question)
        response = agent_result.get("response", "")
        tools_used = agent_result.get("tools_used", [])
        
        # Run multi-criteria evaluation
        eval_result = self.multi_evaluator.evaluate(
            question=case.question,
            response=response,
            reference=case.expected_response,
            criteria=case.criteria
        )
        
        # Add tool evaluation if expected tools specified
        if case.expected_tools:
            tool_result = self.tool_evaluator.evaluate_tool_selection(
                query=case.question,
                tools_used=tools_used,
                expected_tools=case.expected_tools
            )
            eval_result["evaluations"]["tool_selection"] = tool_result
        
        eval_result["case_id"] = case.id
        return eval_result


# Example usage
if __name__ == "__main__":
    # Mock agent function for demonstration
    def mock_agent(question: str) -> dict:
        return {
            "response": f"This is a mock response to: {question}",
            "tools_used": ["search", "calculator"]
        }
    
    # Create test cases
    test_cases = [
        EvaluationCase(
            id="test_001",
            question="What is 2 + 2?",
            expected_response="4",
            expected_tools=["calculator"],
            criteria=["accuracy", "clarity"]
        ),
        EvaluationCase(
            id="test_002",
            question="What is the capital of France?",
            expected_response="Paris",
            criteria=["accuracy", "helpfulness"]
        )
    ]
    
    # Run pipeline
    pipeline = EvaluationPipeline(mock_agent)
    results = pipeline.run(test_cases)
    
    print(f"Total Cases: {results['total_cases']}")
    print(f"Pass Rate: {results['aggregate']['pass_rate']:.1%}")
    print(f"Average Score: {results['aggregate']['average_score']:.2f}")
