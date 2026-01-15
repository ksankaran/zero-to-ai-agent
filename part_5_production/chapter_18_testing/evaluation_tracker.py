# From: AI Agents Book, Chapter 18, Section 18.3
# File: evaluation_tracker.py
# Description: Track evaluation results over time

import json
from datetime import datetime


class EvaluationTracker:
    """Track evaluation results over time."""
    
    def __init__(self, storage_path: str = "evaluations.json"):
        self.storage_path = storage_path
        self.history = self._load_history()
    
    def _load_history(self) -> list:
        """Load evaluation history from storage."""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _save_history(self):
        """Save evaluation history to storage."""
        with open(self.storage_path, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def record(self, evaluation_result: dict, version: str = "unknown"):
        """Record an evaluation result."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "version": version,
            "aggregate": evaluation_result.get("aggregate", {}),
            "total_cases": evaluation_result.get("total_cases", 0)
        }
        self.history.append(record)
        self._save_history()
    
    def get_trend(self, metric: str = "average_score", last_n: int = 10) -> list:
        """Get trend for a specific metric."""
        recent = self.history[-last_n:]
        return [
            {
                "timestamp": r["timestamp"],
                "version": r["version"],
                "value": r["aggregate"].get(metric, 0)
            }
            for r in recent
        ]
    
    def compare_versions(self, version_a: str, version_b: str) -> dict:
        """Compare metrics between two versions."""
        results_a = [r for r in self.history if r["version"] == version_a]
        results_b = [r for r in self.history if r["version"] == version_b]
        
        if not results_a or not results_b:
            return {"error": "One or both versions not found"}
        
        # Use most recent result for each version
        latest_a = results_a[-1]["aggregate"]
        latest_b = results_b[-1]["aggregate"]
        
        comparison = {}
        for metric in latest_a.keys():
            if metric in latest_b:
                val_a = latest_a[metric]
                val_b = latest_b[metric]
                if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
                    comparison[metric] = {
                        "version_a": val_a,
                        "version_b": val_b,
                        "difference": val_b - val_a,
                        "percent_change": ((val_b - val_a) / val_a * 100) if val_a != 0 else 0
                    }
        
        return comparison


# Example usage
if __name__ == "__main__":
    tracker = EvaluationTracker("test_evaluations.json")
    
    # Record some sample evaluations
    tracker.record({
        "total_cases": 10,
        "aggregate": {"pass_rate": 0.7, "average_score": 0.65}
    }, version="v1.0")
    
    tracker.record({
        "total_cases": 10,
        "aggregate": {"pass_rate": 0.8, "average_score": 0.75}
    }, version="v1.1")
    
    # Get trend
    trend = tracker.get_trend("average_score")
    print("Score Trend:")
    for point in trend:
        print(f"  {point['version']}: {point['value']:.2f}")
    
    # Compare versions
    comparison = tracker.compare_versions("v1.0", "v1.1")
    print("\nVersion Comparison (v1.0 -> v1.1):")
    for metric, data in comparison.items():
        print(f"  {metric}: {data['percent_change']:+.1f}%")
