# From: AI Agents Book, Chapter 18, Section 18.3
# File: tool_evaluator.py
# Description: Evaluate how well an agent uses its tools


class ToolUsageEvaluator:
    """Evaluate how well an agent uses its tools."""
    
    def evaluate_tool_selection(
        self,
        query: str,
        tools_used: list[str],
        expected_tools: list[str]
    ) -> dict:
        """Evaluate if the agent selected appropriate tools."""
        used_set = set(tools_used)
        expected_set = set(expected_tools)
        
        correct = used_set & expected_set  # Tools correctly used
        missed = expected_set - used_set    # Tools that should have been used
        extra = used_set - expected_set     # Tools used unnecessarily
        
        # Precision: of tools used, how many were correct?
        precision = len(correct) / len(used_set) if used_set else 1.0
        
        # Recall: of tools needed, how many were used?
        recall = len(correct) / len(expected_set) if expected_set else 1.0
        
        # F1 score balances precision and recall
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "metric": "tool_selection",
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "correct_tools": list(correct),
            "missed_tools": list(missed),
            "extra_tools": list(extra),
            "passed": recall >= 0.8 and precision >= 0.5
        }
    
    def evaluate_tool_arguments(
        self,
        tool_calls: list[dict],
        expected_calls: list[dict]
    ) -> dict:
        """Evaluate if tools were called with correct arguments."""
        if not expected_calls:
            return {"metric": "tool_arguments", "score": 1.0, "passed": True}
        
        correct_count = 0
        details = []
        
        for expected in expected_calls:
            # Find matching tool call
            matching = [
                tc for tc in tool_calls 
                if tc.get("tool") == expected.get("tool")
            ]
            
            if not matching:
                details.append({
                    "tool": expected["tool"],
                    "status": "not_called",
                    "correct": False
                })
                continue
            
            # Check arguments
            actual = matching[0]
            args_match = self._compare_arguments(
                actual.get("arguments", {}),
                expected.get("arguments", {})
            )
            
            if args_match:
                correct_count += 1
            
            details.append({
                "tool": expected["tool"],
                "status": "correct" if args_match else "wrong_arguments",
                "expected_args": expected.get("arguments"),
                "actual_args": actual.get("arguments"),
                "correct": args_match
            })
        
        score = correct_count / len(expected_calls)
        
        return {
            "metric": "tool_arguments",
            "score": score,
            "details": details,
            "passed": score >= 0.8
        }
    
    def _compare_arguments(self, actual: dict, expected: dict) -> bool:
        """Compare tool arguments, allowing for minor variations."""
        for key, expected_value in expected.items():
            if key not in actual:
                return False
            
            actual_value = actual[key]
            
            # String comparison (case-insensitive, stripped)
            if isinstance(expected_value, str) and isinstance(actual_value, str):
                if expected_value.strip().lower() != actual_value.strip().lower():
                    return False
            # Numeric comparison (allow small differences)
            elif isinstance(expected_value, (int, float)) and isinstance(actual_value, (int, float)):
                if abs(expected_value - actual_value) > 0.01:
                    return False
            # Exact comparison for other types
            elif expected_value != actual_value:
                return False
        
        return True


# Example usage
if __name__ == "__main__":
    evaluator = ToolUsageEvaluator()
    
    # Test tool selection
    result = evaluator.evaluate_tool_selection(
        query="What's the weather in Paris?",
        tools_used=["weather_api", "location_lookup"],
        expected_tools=["weather_api"]
    )
    print(f"Tool selection: F1={result['f1_score']:.2f}, Passed={result['passed']}")
    
    # Test tool arguments
    result = evaluator.evaluate_tool_arguments(
        tool_calls=[
            {"tool": "weather_api", "arguments": {"city": "Paris", "units": "celsius"}}
        ],
        expected_calls=[
            {"tool": "weather_api", "arguments": {"city": "paris", "units": "celsius"}}
        ]
    )
    print(f"Tool arguments: Score={result['score']:.2f}, Passed={result['passed']}")
