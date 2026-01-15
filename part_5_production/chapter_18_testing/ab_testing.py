# From: AI Agents Book, Chapter 18, Section 18.6
# File: ab_testing.py
# Description: A/B testing framework for comparing agent variants

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable
import json
from pathlib import Path


@dataclass
class ExperimentResult:
    """Result from a single experiment trial."""
    variant: str
    success: bool
    user_id: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)


@dataclass
class ExperimentConfig:
    """Configuration for an A/B experiment."""
    name: str
    hypothesis: str
    primary_metric: str
    variants: list[str] = field(default_factory=lambda: ["A", "B"])
    target_sample_size: int = 500  # Per variant
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "hypothesis": self.hypothesis,
            "primary_metric": self.primary_metric,
            "variants": self.variants,
            "target_sample_size": self.target_sample_size
        }


def get_variant(user_id: str, experiment_name: str, variants: list[str] = ["A", "B"]) -> str:
    """
    Consistently assign a user to a variant.
    Same user always gets the same variant for a given experiment.
    
    Args:
        user_id: Unique identifier for the user
        experiment_name: Name of the experiment
        variants: List of variant names to distribute across
    
    Returns:
        The assigned variant name
    """
    # Create a hash of user_id + experiment_name
    hash_input = f"{user_id}:{experiment_name}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    
    # Map to variant
    variant_index = hash_value % len(variants)
    return variants[variant_index]


def compare_variants_simple(
    a_successes: int, 
    a_total: int, 
    b_successes: int, 
    b_total: int,
    alpha: float = 0.05
) -> dict:
    """
    Compare two variants using a simple proportion test.
    
    This is a simplified version that doesn't require scipy.
    Uses normal approximation to the binomial.
    
    Args:
        a_successes: Number of successes in variant A
        a_total: Total trials in variant A
        b_successes: Number of successes in variant B
        b_total: Total trials in variant B
        alpha: Significance level (default 0.05)
    
    Returns:
        Dictionary with comparison results
    """
    import math
    
    a_rate = a_successes / a_total if a_total > 0 else 0
    b_rate = b_successes / b_total if b_total > 0 else 0
    
    # Pooled proportion
    pooled = (a_successes + b_successes) / (a_total + b_total) if (a_total + b_total) > 0 else 0
    
    # Standard error
    se = math.sqrt(pooled * (1 - pooled) * (1/a_total + 1/b_total)) if a_total > 0 and b_total > 0 and pooled > 0 and pooled < 1 else 0
    
    # Z-score
    z_score = (b_rate - a_rate) / se if se > 0 else 0
    
    # Critical value for two-tailed test
    z_critical = {0.10: 1.645, 0.05: 1.96, 0.01: 2.576}.get(alpha, 1.96)
    
    significant = abs(z_score) > z_critical
    
    # Determine recommendation
    if significant:
        if b_rate > a_rate:
            recommendation = "B is better - consider rolling out"
        else:
            recommendation = "A is better - keep current version"
    else:
        recommendation = "No significant difference - need more data or keep A"
    
    return {
        "a_rate": a_rate,
        "a_rate_formatted": f"{a_rate:.1%}",
        "b_rate": b_rate,
        "b_rate_formatted": f"{b_rate:.1%}",
        "difference": b_rate - a_rate,
        "difference_formatted": f"{(b_rate - a_rate):+.1%}",
        "relative_improvement": ((b_rate - a_rate) / a_rate * 100) if a_rate > 0 else 0,
        "z_score": z_score,
        "significant": significant,
        "alpha": alpha,
        "recommendation": recommendation
    }


def compare_variants_scipy(
    a_successes: int, 
    a_total: int, 
    b_successes: int, 
    b_total: int
) -> dict:
    """
    Compare two variants using chi-squared test (requires scipy).
    
    Returns whether the difference is statistically significant.
    """
    try:
        from scipy import stats
    except ImportError:
        print("scipy not available, using simple comparison")
        return compare_variants_simple(a_successes, a_total, b_successes, b_total)
    
    # Build contingency table
    table = [
        [a_successes, a_total - a_successes],
        [b_successes, b_total - b_successes]
    ]
    
    chi2, p_value, dof, expected = stats.chi2_contingency(table)
    
    a_rate = a_successes / a_total
    b_rate = b_successes / b_total
    
    return {
        "a_rate": f"{a_rate:.1%}",
        "b_rate": f"{b_rate:.1%}",
        "difference": f"{(b_rate - a_rate):+.1%}",
        "chi2": chi2,
        "p_value": p_value,
        "significant": p_value < 0.05,
        "recommendation": (
            "B is better" if (p_value < 0.05 and b_rate > a_rate) 
            else "A is better" if (p_value < 0.05 and a_rate > b_rate)
            else "No significant difference"
        )
    }


class ABExperiment:
    """
    Manage an A/B testing experiment.
    
    Handles:
    - Variant assignment
    - Result collection
    - Statistical analysis
    - Result persistence
    """
    
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.results: list[ExperimentResult] = []
        self.start_time = datetime.now()
    
    def assign_variant(self, user_id: str) -> str:
        """Assign a user to a variant."""
        return get_variant(user_id, self.config.name, self.config.variants)
    
    def record_result(self, result: ExperimentResult) -> None:
        """Record a result from the experiment."""
        self.results.append(result)
    
    def record(self, variant: str, success: bool, user_id: str | None = None, **metadata) -> None:
        """Convenience method to record a result."""
        self.record_result(ExperimentResult(
            variant=variant,
            success=success,
            user_id=user_id,
            metadata=metadata
        ))
    
    def get_counts(self) -> dict[str, dict]:
        """Get success/failure counts per variant."""
        counts = {v: {"successes": 0, "failures": 0, "total": 0} 
                  for v in self.config.variants}
        
        for result in self.results:
            if result.variant in counts:
                counts[result.variant]["total"] += 1
                if result.success:
                    counts[result.variant]["successes"] += 1
                else:
                    counts[result.variant]["failures"] += 1
        
        return counts
    
    def progress(self) -> dict:
        """Check experiment progress toward target sample size."""
        counts = self.get_counts()
        
        progress = {}
        for variant, data in counts.items():
            progress[variant] = {
                "current": data["total"],
                "target": self.config.target_sample_size,
                "percent_complete": data["total"] / self.config.target_sample_size * 100
            }
        
        all_complete = all(
            data["total"] >= self.config.target_sample_size 
            for data in counts.values()
        )
        
        return {
            "by_variant": progress,
            "complete": all_complete,
            "total_results": len(self.results)
        }
    
    def analyze(self) -> dict:
        """Analyze experiment results."""
        counts = self.get_counts()
        
        # For two variants, do direct comparison
        if len(self.config.variants) == 2:
            v_a, v_b = self.config.variants
            comparison = compare_variants_simple(
                counts[v_a]["successes"], counts[v_a]["total"],
                counts[v_b]["successes"], counts[v_b]["total"]
            )
        else:
            comparison = None
        
        # Calculate rates for each variant
        rates = {}
        for variant, data in counts.items():
            rate = data["successes"] / data["total"] if data["total"] > 0 else 0
            rates[variant] = {
                "rate": rate,
                "rate_formatted": f"{rate:.1%}",
                "successes": data["successes"],
                "total": data["total"]
            }
        
        return {
            "experiment": self.config.name,
            "hypothesis": self.config.hypothesis,
            "primary_metric": self.config.primary_metric,
            "rates": rates,
            "comparison": comparison,
            "progress": self.progress()
        }
    
    def print_report(self) -> None:
        """Print a formatted experiment report."""
        analysis = self.analyze()
        
        print("\n" + "=" * 60)
        print(f"A/B EXPERIMENT: {analysis['experiment']}")
        print("=" * 60)
        
        print(f"\nHypothesis: {analysis['hypothesis']}")
        print(f"Primary Metric: {analysis['primary_metric']}")
        
        print("\n--- Results by Variant ---")
        for variant, data in analysis['rates'].items():
            bar_len = int(data['rate'] * 30)
            bar = "█" * bar_len + "░" * (30 - bar_len)
            print(f"  {variant}: {data['rate_formatted']} [{bar}]")
            print(f"      ({data['successes']}/{data['total']} successes)")
        
        if analysis['comparison']:
            comp = analysis['comparison']
            print("\n--- Statistical Analysis ---")
            print(f"  Difference: {comp['difference_formatted']}")
            print(f"  Relative improvement: {comp['relative_improvement']:+.1f}%")
            print(f"  Z-score: {comp['z_score']:.2f}")
            print(f"  Significant (α={comp['alpha']}): {'Yes ✓' if comp['significant'] else 'No'}")
            print(f"\n  📊 Recommendation: {comp['recommendation']}")
        
        prog = analysis['progress']
        print("\n--- Progress ---")
        for variant, data in prog['by_variant'].items():
            print(f"  {variant}: {data['current']}/{data['target']} ({data['percent_complete']:.0f}%)")
        
        status = "✅ Complete" if prog['complete'] else "⏳ In Progress"
        print(f"\n  Status: {status}")
        print("=" * 60)
    
    def save(self, path: str) -> None:
        """Save experiment state to JSON."""
        data = {
            "config": self.config.to_dict(),
            "start_time": self.start_time.isoformat(),
            "results": [
                {
                    "variant": r.variant,
                    "success": r.success,
                    "user_id": r.user_id,
                    "timestamp": r.timestamp,
                    "metadata": r.metadata
                }
                for r in self.results
            ]
        }
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Experiment saved to {path}")
    
    @classmethod
    def load(cls, path: str) -> "ABExperiment":
        """Load experiment from JSON."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        config = ExperimentConfig(**data["config"])
        experiment = cls(config)
        experiment.start_time = datetime.fromisoformat(data["start_time"])
        
        for r in data["results"]:
            experiment.results.append(ExperimentResult(
                variant=r["variant"],
                success=r["success"],
                user_id=r["user_id"],
                timestamp=r["timestamp"],
                metadata=r["metadata"]
            ))
        
        return experiment


# Example usage
if __name__ == "__main__":
    import random
    
    # Create an experiment
    config = ExperimentConfig(
        name="prompt_v2_test",
        hypothesis="A more detailed system prompt will increase task completion from 75% to 85%",
        primary_metric="task_completion_rate",
        target_sample_size=100  # Small for demo
    )
    
    experiment = ABExperiment(config)
    
    # Simulate running the experiment
    print("Simulating experiment...")
    
    # Simulate 200 users
    for i in range(200):
        user_id = f"user_{i}"
        variant = experiment.assign_variant(user_id)
        
        # Simulate different success rates
        # A has 75% success, B has 85% success
        if variant == "A":
            success = random.random() < 0.75
        else:
            success = random.random() < 0.85
        
        experiment.record(variant=variant, success=success, user_id=user_id)
    
    # Print results
    experiment.print_report()
    
    # Demonstrate variant assignment consistency
    print("\n--- Variant Assignment Demo ---")
    test_user = "user_12345"
    for _ in range(5):
        v = get_variant(test_user, "prompt_v2_test")
        print(f"  {test_user} -> {v}")
    print("  (Same user always gets same variant)")
