# From: AI Agents Book, Chapter 18, Section 18.3
# File: exercise_3_18_3_solution.py
# Description: Exercise 3 Solution - Evaluation dashboard with summary reports

from datetime import datetime
from typing import Any


class EvaluationDashboard:
    """
    Generate summary reports from evaluation results.
    Provides insights for debugging and tracking improvements.
    """
    
    def __init__(self, history: list[dict] | None = None):
        """
        Initialize with optional historical data.
        
        Args:
            history: List of past evaluation results for trend analysis
        """
        self.history = history or []
    
    def generate_report(
        self,
        evaluation_results: dict,
        version: str = "current",
        include_details: bool = True
    ) -> str:
        """
        Generate a formatted evaluation report.
        
        Args:
            evaluation_results: Results from an evaluation pipeline run
            version: Version identifier for tracking
            include_details: Whether to include detailed case analysis
        
        Returns:
            Formatted report string
        """
        report_lines = []
        
        # Header
        report_lines.append("=" * 60)
        report_lines.append("AGENT EVALUATION REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Version: {version}")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Total Test Cases: {evaluation_results.get('total_cases', 0)}")
        report_lines.append("")
        
        # Overall Summary
        aggregate = evaluation_results.get("aggregate", {})
        report_lines.append("-" * 40)
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 40)
        
        pass_rate = aggregate.get("pass_rate", 0) * 100
        avg_score = aggregate.get("average_score", 0) * 100
        
        report_lines.append(f"Pass Rate: {pass_rate:.1f}% ({aggregate.get('passed_count', 0)}/{evaluation_results.get('total_cases', 0)})")
        report_lines.append(f"Average Score: {avg_score:.1f}%")
        report_lines.append(self._get_grade(avg_score))
        report_lines.append("")
        
        # Breakdown by Criterion
        report_lines.append("-" * 40)
        report_lines.append("BREAKDOWN BY CRITERION")
        report_lines.append("-" * 40)
        
        criterion_stats = self._calculate_criterion_stats(evaluation_results.get("cases", []))
        
        for criterion, stats in sorted(criterion_stats.items(), key=lambda x: x[1]["avg"], reverse=True):
            bar = self._score_bar(stats["avg"])
            report_lines.append(f"{criterion:20} {bar} {stats['avg']*100:.1f}% (pass: {stats['pass_rate']*100:.0f}%)")
        
        report_lines.append("")
        
        # Worst Performing Cases
        report_lines.append("-" * 40)
        report_lines.append("CASES NEEDING ATTENTION")
        report_lines.append("-" * 40)
        
        worst_cases = self._get_worst_cases(evaluation_results.get("cases", []), n=5)
        
        if worst_cases:
            for i, case in enumerate(worst_cases, 1):
                report_lines.append(f"\n{i}. Case: {case.get('case_id', 'unknown')}")
                report_lines.append(f"   Score: {case['summary']['average_score']*100:.1f}%")
                report_lines.append(f"   Question: {case.get('question', 'N/A')[:60]}...")
                
                failed = [c for c, e in case.get('evaluations', {}).items() 
                         if not e.get('passed', True)]
                if failed:
                    report_lines.append(f"   Failed criteria: {', '.join(failed)}")
        else:
            report_lines.append("All cases passed! 🎉")
        
        report_lines.append("")
        
        # Trend Analysis
        if self.history:
            report_lines.append("-" * 40)
            report_lines.append("TREND ANALYSIS")
            report_lines.append("-" * 40)
            
            trend = self._analyze_trend()
            report_lines.append(f"Evaluations in history: {len(self.history)}")
            report_lines.append(f"Score trend: {trend['direction']}")
            
            if trend['recent_change'] is not None:
                sign = "+" if trend['recent_change'] > 0 else ""
                report_lines.append(f"Recent change: {sign}{trend['recent_change']*100:.1f}%")
        
        report_lines.append("")
        
        # Detailed Case Analysis (optional)
        if include_details and evaluation_results.get("cases"):
            report_lines.append("-" * 40)
            report_lines.append("DETAILED CASE RESULTS")
            report_lines.append("-" * 40)
            
            for case in evaluation_results["cases"][:10]:  # Limit to first 10
                report_lines.append(f"\nCase: {case.get('case_id', 'unknown')}")
                report_lines.append(f"  Overall: {'PASS' if case['summary']['all_passed'] else 'FAIL'} ({case['summary']['average_score']*100:.1f}%)")
                
                for criterion, eval_data in case.get("evaluations", {}).items():
                    status = "✓" if eval_data.get("passed", True) else "✗"
                    score = eval_data.get("normalized_score", eval_data.get("score", 0))
                    if isinstance(score, float) and score <= 1:
                        score_str = f"{score*100:.0f}%"
                    else:
                        score_str = str(score)
                    report_lines.append(f"  {status} {criterion}: {score_str}")
        
        # Footer
        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def _calculate_criterion_stats(self, cases: list[dict]) -> dict:
        """Calculate statistics for each evaluation criterion."""
        criterion_scores = {}
        
        for case in cases:
            for criterion, eval_data in case.get("evaluations", {}).items():
                if criterion not in criterion_scores:
                    criterion_scores[criterion] = {"scores": [], "passed": []}
                
                score = eval_data.get("normalized_score", eval_data.get("score", 0))
                if isinstance(score, (int, float)):
                    if score > 1:  # Assume it's a 1-5 scale
                        score = score / 5.0
                    criterion_scores[criterion]["scores"].append(score)
                    criterion_scores[criterion]["passed"].append(eval_data.get("passed", True))
        
        stats = {}
        for criterion, data in criterion_scores.items():
            scores = data["scores"]
            passed = data["passed"]
            stats[criterion] = {
                "avg": sum(scores) / len(scores) if scores else 0,
                "min": min(scores) if scores else 0,
                "max": max(scores) if scores else 0,
                "pass_rate": sum(passed) / len(passed) if passed else 0
            }
        
        return stats
    
    def _get_worst_cases(self, cases: list[dict], n: int = 5) -> list[dict]:
        """Get the n worst performing cases."""
        sorted_cases = sorted(
            cases,
            key=lambda c: c.get("summary", {}).get("average_score", 1)
        )
        return sorted_cases[:n]
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade with emoji."""
        if score >= 90:
            return "Grade: A 🌟"
        elif score >= 80:
            return "Grade: B ✓"
        elif score >= 70:
            return "Grade: C ⚠️"
        elif score >= 60:
            return "Grade: D ⚠️"
        else:
            return "Grade: F ❌"
    
    def _score_bar(self, score: float, width: int = 20) -> str:
        """Create a visual score bar."""
        filled = int(score * width)
        empty = width - filled
        return f"[{'█' * filled}{'░' * empty}]"
    
    def _analyze_trend(self) -> dict:
        """Analyze score trends from history."""
        if len(self.history) < 2:
            return {"direction": "Not enough data", "recent_change": None}
        
        scores = [r.get("aggregate", {}).get("average_score", 0) for r in self.history]
        
        recent_change = scores[-1] - scores[-2] if len(scores) >= 2 else None
        
        # Simple trend direction
        if len(scores) >= 3:
            recent_avg = sum(scores[-3:]) / 3
            older_avg = sum(scores[:-3]) / (len(scores) - 3) if len(scores) > 3 else scores[0]
            
            if recent_avg > older_avg + 0.05:
                direction = "📈 Improving"
            elif recent_avg < older_avg - 0.05:
                direction = "📉 Declining"
            else:
                direction = "➡️ Stable"
        else:
            direction = "➡️ Stable"
        
        return {
            "direction": direction,
            "recent_change": recent_change
        }


# Example usage
if __name__ == "__main__":
    # Sample evaluation results
    sample_results = {
        "total_cases": 10,
        "aggregate": {
            "pass_rate": 0.8,
            "average_score": 0.75,
            "passed_count": 8,
            "failed_count": 2
        },
        "cases": [
            {
                "case_id": "test_001",
                "question": "How do I reset my password?",
                "summary": {"average_score": 0.9, "all_passed": True},
                "evaluations": {
                    "accuracy": {"normalized_score": 0.9, "passed": True},
                    "helpfulness": {"normalized_score": 0.85, "passed": True}
                }
            },
            {
                "case_id": "test_002",
                "question": "What is your refund policy for digital products?",
                "summary": {"average_score": 0.5, "all_passed": False},
                "evaluations": {
                    "accuracy": {"normalized_score": 0.4, "passed": False},
                    "helpfulness": {"normalized_score": 0.6, "passed": True}
                }
            }
        ]
    }
    
    # Sample history for trend analysis
    history = [
        {"aggregate": {"average_score": 0.65}},
        {"aggregate": {"average_score": 0.70}},
        {"aggregate": {"average_score": 0.75}},
    ]
    
    dashboard = EvaluationDashboard(history=history)
    report = dashboard.generate_report(sample_results, version="v2.1.0")
    print(report)
