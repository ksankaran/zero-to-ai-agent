# From: AI Agents Book, Chapter 18, Section 18.5
# File: accuracy_calculator.py
# Description: Calculate accuracy metrics with severity weighting and category breakdown

from dataclasses import dataclass
from collections import defaultdict
import math


@dataclass
class EvaluationResult:
    """Result of a single evaluation."""
    case_id: str
    passed: bool
    category: str
    severity: str = "minor"  # critical, major, minor, trivial
    score: float = 0.0  # 0.0 to 1.0


class AccuracyCalculator:
    """
    Calculate accuracy metrics with severity weighting and category breakdown.
    
    Implements concepts from Section 18.5:
    - Weighted accuracy by error severity
    - Category-specific breakdowns
    - Confidence intervals
    """
    
    # Default severity weights (higher = more impactful)
    DEFAULT_WEIGHTS = {
        "critical": 10.0,
        "major": 5.0,
        "minor": 2.0,
        "trivial": 1.0
    }
    
    def __init__(self, severity_weights: dict | None = None):
        """
        Initialize calculator.
        
        Args:
            severity_weights: Custom weights for severity levels
        """
        self.weights = severity_weights or self.DEFAULT_WEIGHTS
        self.results: list[EvaluationResult] = []
    
    def add_result(self, result: EvaluationResult) -> None:
        """Add an evaluation result."""
        self.results.append(result)
    
    def add_results(self, results: list[EvaluationResult]) -> None:
        """Add multiple evaluation results."""
        self.results.extend(results)
    
    def overall_accuracy(self) -> float:
        """Calculate simple overall accuracy (pass rate)."""
        if not self.results:
            return 0.0
        passed = sum(1 for r in self.results if r.passed)
        return passed / len(self.results)
    
    def weighted_accuracy(self) -> float:
        """
        Calculate weighted accuracy considering error severity.
        
        Errors with higher severity have more impact on the score.
        """
        if not self.results:
            return 0.0
        
        total_weight = 0.0
        weighted_pass = 0.0
        
        for r in self.results:
            weight = self.weights.get(r.severity, 1.0)
            total_weight += weight
            if r.passed:
                weighted_pass += weight
        
        return weighted_pass / total_weight if total_weight > 0 else 0.0
    
    def accuracy_by_category(self) -> dict[str, dict]:
        """
        Break down accuracy by category.
        
        Returns dict with category -> {accuracy, count, passed, failed}
        """
        categories = defaultdict(lambda: {"passed": 0, "failed": 0})
        
        for r in self.results:
            if r.passed:
                categories[r.category]["passed"] += 1
            else:
                categories[r.category]["failed"] += 1
        
        breakdown = {}
        for cat, counts in categories.items():
            total = counts["passed"] + counts["failed"]
            breakdown[cat] = {
                "accuracy": counts["passed"] / total if total > 0 else 0.0,
                "count": total,
                "passed": counts["passed"],
                "failed": counts["failed"]
            }
        
        return breakdown
    
    def accuracy_by_severity(self) -> dict[str, dict]:
        """Break down accuracy by error severity level."""
        severities = defaultdict(lambda: {"passed": 0, "failed": 0})
        
        for r in self.results:
            if r.passed:
                severities[r.severity]["passed"] += 1
            else:
                severities[r.severity]["failed"] += 1
        
        breakdown = {}
        for sev, counts in severities.items():
            total = counts["passed"] + counts["failed"]
            breakdown[sev] = {
                "accuracy": counts["passed"] / total if total > 0 else 0.0,
                "count": total,
                "error_rate": counts["failed"] / total if total > 0 else 0.0
            }
        
        return breakdown
    
    def critical_error_rate(self) -> float:
        """Calculate the rate of critical errors specifically."""
        critical_results = [r for r in self.results if r.severity == "critical"]
        if not critical_results:
            return 0.0
        failed = sum(1 for r in critical_results if not r.passed)
        return failed / len(critical_results)
    
    def confidence_interval(self, confidence: float = 0.95) -> tuple[float, float]:
        """
        Calculate confidence interval for overall accuracy.
        
        Uses normal approximation to binomial.
        
        Args:
            confidence: Confidence level (default 0.95 for 95% CI)
        
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        n = len(self.results)
        if n == 0:
            return (0.0, 0.0)
        
        p = self.overall_accuracy()
        
        # Z-score for confidence level
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(confidence, 1.96)
        
        # Standard error
        se = math.sqrt(p * (1 - p) / n)
        
        # Confidence interval
        margin = z * se
        lower = max(0.0, p - margin)
        upper = min(1.0, p + margin)
        
        return (lower, upper)
    
    def summary(self) -> dict:
        """Generate a complete summary of accuracy metrics."""
        ci_lower, ci_upper = self.confidence_interval()
        
        return {
            "total_cases": len(self.results),
            "overall_accuracy": self.overall_accuracy(),
            "weighted_accuracy": self.weighted_accuracy(),
            "confidence_interval_95": {
                "lower": ci_lower,
                "upper": ci_upper
            },
            "critical_error_rate": self.critical_error_rate(),
            "by_category": self.accuracy_by_category(),
            "by_severity": self.accuracy_by_severity()
        }
    
    def print_report(self) -> None:
        """Print a formatted accuracy report."""
        summary = self.summary()
        
        print("\n" + "=" * 60)
        print("ACCURACY REPORT")
        print("=" * 60)
        
        print(f"\nTotal Cases: {summary['total_cases']}")
        print(f"Overall Accuracy: {summary['overall_accuracy']:.1%}")
        print(f"Weighted Accuracy: {summary['weighted_accuracy']:.1%}")
        
        ci = summary['confidence_interval_95']
        print(f"95% Confidence Interval: [{ci['lower']:.1%}, {ci['upper']:.1%}]")
        
        print(f"\nCritical Error Rate: {summary['critical_error_rate']:.1%}")
        
        print("\n--- By Category ---")
        for cat, stats in summary['by_category'].items():
            print(f"  {cat}: {stats['accuracy']:.1%} "
                  f"({stats['passed']}/{stats['count']})")
        
        print("\n--- By Severity ---")
        for sev in ["critical", "major", "minor", "trivial"]:
            if sev in summary['by_severity']:
                stats = summary['by_severity'][sev]
                print(f"  {sev}: {stats['accuracy']:.1%} accuracy, "
                      f"{stats['error_rate']:.1%} error rate "
                      f"(n={stats['count']})")
        
        print("=" * 60)


# Example usage
if __name__ == "__main__":
    calc = AccuracyCalculator()
    
    # Simulate evaluation results
    results = [
        # Password reset - mostly passes
        EvaluationResult("pr_001", True, "password_reset", "minor"),
        EvaluationResult("pr_002", True, "password_reset", "minor"),
        EvaluationResult("pr_003", True, "password_reset", "minor"),
        EvaluationResult("pr_004", False, "password_reset", "minor"),
        
        # Order status - good performance
        EvaluationResult("os_001", True, "order_status", "major"),
        EvaluationResult("os_002", True, "order_status", "major"),
        EvaluationResult("os_003", True, "order_status", "major"),
        EvaluationResult("os_004", True, "order_status", "major"),
        EvaluationResult("os_005", False, "order_status", "major"),
        
        # Refunds - problematic area
        EvaluationResult("rf_001", True, "refunds", "critical"),
        EvaluationResult("rf_002", False, "refunds", "critical"),
        EvaluationResult("rf_003", False, "refunds", "critical"),
        EvaluationResult("rf_004", True, "refunds", "critical"),
        
        # Technical - decent
        EvaluationResult("tech_001", True, "technical", "major"),
        EvaluationResult("tech_002", True, "technical", "major"),
        EvaluationResult("tech_003", False, "technical", "major"),
    ]
    
    calc.add_results(results)
    calc.print_report()
