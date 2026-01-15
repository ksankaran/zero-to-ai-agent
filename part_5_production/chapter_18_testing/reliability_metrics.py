# From: AI Agents Book, Chapter 18, Section 18.5
# File: reliability_metrics.py
# Description: Measure reliability through consistency, multiple runs, and statistical comparison

from dataclasses import dataclass
import math
from collections import defaultdict


@dataclass 
class RunResult:
    """Result of a single run of a test case."""
    case_id: str
    run_number: int
    passed: bool
    score: float = 0.0


class ReliabilityAnalyzer:
    """
    Analyze reliability through consistency and multiple runs.
    
    Implements concepts from Section 18.5:
    - Multiple runs per test case
    - Consistency measurement
    - Statistical significance testing
    """
    
    def __init__(self):
        self.runs: dict[str, list[RunResult]] = defaultdict(list)
    
    def add_run(self, result: RunResult) -> None:
        """Add a run result for a test case."""
        self.runs[result.case_id].append(result)
    
    def add_runs(self, results: list[RunResult]) -> None:
        """Add multiple run results."""
        for result in results:
            self.add_run(result)
    
    def consistency_score(self, case_id: str) -> float:
        """
        Calculate consistency for a specific test case.
        
        Returns 1.0 if all runs have same outcome, 0.0 if split 50/50.
        """
        runs = self.runs.get(case_id, [])
        if len(runs) < 2:
            return 1.0  # Can't measure consistency with < 2 runs
        
        pass_count = sum(1 for r in runs if r.passed)
        pass_rate = pass_count / len(runs)
        
        # Consistency is distance from 50/50
        return abs(pass_rate - 0.5) * 2
    
    def overall_consistency(self) -> float:
        """Calculate average consistency across all test cases."""
        if not self.runs:
            return 0.0
        
        consistencies = [self.consistency_score(case_id) 
                        for case_id in self.runs.keys()]
        return sum(consistencies) / len(consistencies)
    
    def pass_rate_per_case(self) -> dict[str, float]:
        """Calculate pass rate for each test case across runs."""
        rates = {}
        for case_id, runs in self.runs.items():
            if runs:
                rates[case_id] = sum(1 for r in runs if r.passed) / len(runs)
        return rates
    
    def aggregate_pass_rate(self) -> float:
        """Calculate overall pass rate across all runs."""
        all_runs = [r for runs in self.runs.values() for r in runs]
        if not all_runs:
            return 0.0
        return sum(1 for r in all_runs if r.passed) / len(all_runs)
    
    def worst_case_accuracy(self) -> float:
        """
        Calculate accuracy using worst run for each case.
        
        Conservative estimate - if any run fails, case counts as failed.
        """
        if not self.runs:
            return 0.0
        
        worst_pass = 0
        for case_id, runs in self.runs.items():
            # Case passes only if ALL runs pass
            if all(r.passed for r in runs):
                worst_pass += 1
        
        return worst_pass / len(self.runs)
    
    def best_case_accuracy(self) -> float:
        """
        Calculate accuracy using best run for each case.
        
        Optimistic estimate - if any run passes, case counts as passed.
        """
        if not self.runs:
            return 0.0
        
        best_pass = 0
        for case_id, runs in self.runs.items():
            # Case passes if ANY run passes
            if any(r.passed for r in runs):
                best_pass += 1
        
        return best_pass / len(self.runs)
    
    def flaky_cases(self, threshold: float = 0.8) -> list[str]:
        """
        Identify flaky test cases (inconsistent results).
        
        Args:
            threshold: Consistency below this is considered flaky
        
        Returns:
            List of case IDs that are flaky
        """
        flaky = []
        for case_id in self.runs.keys():
            if self.consistency_score(case_id) < threshold:
                flaky.append(case_id)
        return flaky
    
    def summary(self) -> dict:
        """Generate reliability summary."""
        return {
            "total_cases": len(self.runs),
            "total_runs": sum(len(runs) for runs in self.runs.values()),
            "aggregate_pass_rate": self.aggregate_pass_rate(),
            "worst_case_accuracy": self.worst_case_accuracy(),
            "best_case_accuracy": self.best_case_accuracy(),
            "overall_consistency": self.overall_consistency(),
            "flaky_cases": self.flaky_cases()
        }
    
    def print_report(self) -> None:
        """Print a formatted reliability report."""
        summary = self.summary()
        
        print("\n" + "=" * 60)
        print("RELIABILITY REPORT")
        print("=" * 60)
        
        print(f"\nTest Cases: {summary['total_cases']}")
        print(f"Total Runs: {summary['total_runs']}")
        avg_runs = summary['total_runs'] / summary['total_cases'] if summary['total_cases'] > 0 else 0
        print(f"Average Runs per Case: {avg_runs:.1f}")
        
        print(f"\nAggregate Pass Rate: {summary['aggregate_pass_rate']:.1%}")
        print(f"Worst-Case Accuracy: {summary['worst_case_accuracy']:.1%}")
        print(f"Best-Case Accuracy: {summary['best_case_accuracy']:.1%}")
        print(f"Overall Consistency: {summary['overall_consistency']:.1%}")
        
        if summary['flaky_cases']:
            print(f"\n⚠️  Flaky Cases ({len(summary['flaky_cases'])}):")
            for case_id in summary['flaky_cases'][:5]:  # Show first 5
                rates = self.pass_rate_per_case()
                print(f"    {case_id}: {rates[case_id]:.0%} pass rate")
            if len(summary['flaky_cases']) > 5:
                print(f"    ... and {len(summary['flaky_cases']) - 5} more")
        else:
            print("\n✅ No flaky cases detected")
        
        print("=" * 60)


def compare_versions(
    version_a_results: list[tuple[str, bool]],  # (case_id, passed)
    version_b_results: list[tuple[str, bool]],
    alpha: float = 0.05
) -> dict:
    """
    Compare two versions using statistical significance testing.
    
    Uses chi-squared test for comparing pass rates.
    
    Args:
        version_a_results: List of (case_id, passed) for version A
        version_b_results: List of (case_id, passed) for version B
        alpha: Significance level (default 0.05)
    
    Returns:
        Comparison statistics and significance assessment
    """
    a_passed = sum(1 for _, p in version_a_results if p)
    a_total = len(version_a_results)
    b_passed = sum(1 for _, p in version_b_results if p)
    b_total = len(version_b_results)
    
    a_rate = a_passed / a_total if a_total > 0 else 0
    b_rate = b_passed / b_total if b_total > 0 else 0
    
    # Pooled proportion for chi-squared test
    pooled = (a_passed + b_passed) / (a_total + b_total) if (a_total + b_total) > 0 else 0
    
    # Standard error
    se = math.sqrt(pooled * (1 - pooled) * (1/a_total + 1/b_total)) if a_total > 0 and b_total > 0 else 0
    
    # Z-score
    z_score = (b_rate - a_rate) / se if se > 0 else 0
    
    # Two-tailed p-value approximation (using standard normal)
    # For simplicity, we'll just check against critical values
    z_critical = {0.10: 1.645, 0.05: 1.96, 0.01: 2.576}
    
    is_significant = abs(z_score) > z_critical.get(alpha, 1.96)
    
    return {
        "version_a": {
            "pass_rate": a_rate,
            "passed": a_passed,
            "total": a_total
        },
        "version_b": {
            "pass_rate": b_rate,
            "passed": b_passed,
            "total": b_total
        },
        "difference": b_rate - a_rate,
        "percent_change": ((b_rate - a_rate) / a_rate * 100) if a_rate > 0 else 0,
        "z_score": z_score,
        "is_significant": is_significant,
        "alpha": alpha,
        "conclusion": (
            f"Version B is {'significantly ' if is_significant else ''}{'better' if b_rate > a_rate else 'worse'} "
            f"({'p < {}'.format(alpha) if is_significant else 'not statistically significant'})"
        )
    }


# Example usage
if __name__ == "__main__":
    # Example 1: Reliability analysis with multiple runs
    print("=== Reliability Analysis ===")
    analyzer = ReliabilityAnalyzer()
    
    # Simulate multiple runs for several test cases
    test_runs = [
        # Consistent case - always passes
        RunResult("case_001", 1, True),
        RunResult("case_001", 2, True),
        RunResult("case_001", 3, True),
        
        # Consistent case - always fails  
        RunResult("case_002", 1, False),
        RunResult("case_002", 2, False),
        RunResult("case_002", 3, False),
        
        # Flaky case - inconsistent
        RunResult("case_003", 1, True),
        RunResult("case_003", 2, False),
        RunResult("case_003", 3, True),
        
        # Mostly passes
        RunResult("case_004", 1, True),
        RunResult("case_004", 2, True),
        RunResult("case_004", 3, False),
        
        # Very flaky
        RunResult("case_005", 1, True),
        RunResult("case_005", 2, False),
        RunResult("case_005", 3, False),
    ]
    
    analyzer.add_runs(test_runs)
    analyzer.print_report()
    
    # Example 2: Version comparison
    print("\n=== Version Comparison ===")
    
    # Simulated results from two versions
    version_a = [
        ("test_1", True), ("test_2", True), ("test_3", False),
        ("test_4", True), ("test_5", False), ("test_6", True),
        ("test_7", False), ("test_8", True), ("test_9", True),
        ("test_10", False),
    ] * 10  # 100 cases total
    
    version_b = [
        ("test_1", True), ("test_2", True), ("test_3", True),
        ("test_4", True), ("test_5", False), ("test_6", True),
        ("test_7", True), ("test_8", True), ("test_9", True),
        ("test_10", False),
    ] * 10  # 100 cases total
    
    comparison = compare_versions(version_a, version_b)
    
    print(f"Version A: {comparison['version_a']['pass_rate']:.1%}")
    print(f"Version B: {comparison['version_b']['pass_rate']:.1%}")
    print(f"Difference: {comparison['difference']:+.1%}")
    print(f"Z-score: {comparison['z_score']:.2f}")
    print(f"Conclusion: {comparison['conclusion']}")
