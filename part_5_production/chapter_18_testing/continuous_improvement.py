# From: AI Agents Book, Chapter 18, Section 18.7
# File: continuous_improvement.py
# Description: Tools for continuous improvement workflows - scheduled evaluation, monitoring, reporting

import json
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable
from collections import defaultdict


@dataclass
class EvaluationRun:
    """Record of a single evaluation run."""
    timestamp: str
    version: str
    overall_score: float
    pass_rate: float
    total_cases: int
    by_category: dict = field(default_factory=dict)
    failures: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


class QualityTracker:
    """
    Track quality metrics over time for continuous improvement.
    
    Implements the measurement and analysis phases of the improvement cycle.
    """
    
    def __init__(self, storage_path: str = "quality_history.json"):
        self.storage_path = Path(storage_path)
        self.history: list[EvaluationRun] = []
        self._load()
    
    def _load(self) -> None:
        """Load history from storage."""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.history = [EvaluationRun(**run) for run in data]
    
    def _save(self) -> None:
        """Save history to storage."""
        data = [
            {
                "timestamp": run.timestamp,
                "version": run.version,
                "overall_score": run.overall_score,
                "pass_rate": run.pass_rate,
                "total_cases": run.total_cases,
                "by_category": run.by_category,
                "failures": run.failures,
                "metadata": run.metadata
            }
            for run in self.history
        ]
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def record_run(self, run: EvaluationRun) -> None:
        """Record an evaluation run."""
        self.history.append(run)
        self._save()
    
    def record(
        self,
        version: str,
        overall_score: float,
        pass_rate: float,
        total_cases: int,
        by_category: dict | None = None,
        failures: list | None = None,
        **metadata
    ) -> EvaluationRun:
        """Convenience method to record a run."""
        run = EvaluationRun(
            timestamp=datetime.now().isoformat(),
            version=version,
            overall_score=overall_score,
            pass_rate=pass_rate,
            total_cases=total_cases,
            by_category=by_category or {},
            failures=failures or [],
            metadata=metadata
        )
        self.record_run(run)
        return run
    
    def get_latest(self) -> EvaluationRun | None:
        """Get the most recent evaluation run."""
        return self.history[-1] if self.history else None
    
    def get_trend(self, metric: str = "pass_rate", days: int = 30) -> list[tuple[str, float]]:
        """Get trend data for a metric over time."""
        cutoff = datetime.now() - timedelta(days=days)
        
        trend = []
        for run in self.history:
            run_time = datetime.fromisoformat(run.timestamp)
            if run_time >= cutoff:
                value = getattr(run, metric, None)
                if value is not None:
                    trend.append((run.timestamp[:10], value))
        
        return trend
    
    def compare_to_baseline(self, baseline_version: str) -> dict | None:
        """Compare latest results to a baseline version."""
        # Find baseline
        baseline = None
        for run in self.history:
            if run.version == baseline_version:
                baseline = run
                break
        
        if not baseline:
            return None
        
        latest = self.get_latest()
        if not latest:
            return None
        
        return {
            "baseline": {
                "version": baseline.version,
                "pass_rate": baseline.pass_rate,
                "overall_score": baseline.overall_score
            },
            "current": {
                "version": latest.version,
                "pass_rate": latest.pass_rate,
                "overall_score": latest.overall_score
            },
            "change": {
                "pass_rate": latest.pass_rate - baseline.pass_rate,
                "overall_score": latest.overall_score - baseline.overall_score
            },
            "improved": latest.pass_rate > baseline.pass_rate
        }
    
    def detect_regression(self, threshold: float = 0.05) -> dict | None:
        """
        Detect if recent performance has regressed.
        
        Args:
            threshold: Minimum drop to consider a regression
        
        Returns:
            Regression info if detected, None otherwise
        """
        if len(self.history) < 2:
            return None
        
        # Compare last run to average of previous 5
        recent = self.history[-1]
        previous = self.history[-6:-1] if len(self.history) >= 6 else self.history[:-1]
        
        avg_pass_rate = sum(r.pass_rate for r in previous) / len(previous)
        
        drop = avg_pass_rate - recent.pass_rate
        
        if drop > threshold:
            return {
                "detected": True,
                "current_pass_rate": recent.pass_rate,
                "average_pass_rate": avg_pass_rate,
                "drop": drop,
                "version": recent.version,
                "message": f"⚠️ Regression detected: {drop:.1%} drop from recent average"
            }
        
        return {"detected": False}


class QualityReporter:
    """Generate quality reports from tracking data."""
    
    def __init__(self, tracker: QualityTracker):
        self.tracker = tracker
    
    def weekly_report(self) -> str:
        """Generate a weekly quality report."""
        # Get runs from last 7 days
        cutoff = datetime.now() - timedelta(days=7)
        recent_runs = [
            run for run in self.tracker.history
            if datetime.fromisoformat(run.timestamp) >= cutoff
        ]
        
        if not recent_runs:
            return "No evaluation runs in the past week."
        
        # Calculate statistics
        pass_rates = [r.pass_rate for r in recent_runs]
        scores = [r.overall_score for r in recent_runs]
        
        avg_pass_rate = sum(pass_rates) / len(pass_rates)
        avg_score = sum(scores) / len(scores)
        latest = recent_runs[-1]
        
        # Collect all failures
        all_failures = []
        for run in recent_runs:
            all_failures.extend(run.failures)
        
        # Count failure frequency
        failure_counts = defaultdict(int)
        for failure in all_failures:
            failure_id = failure.get('case_id', str(failure))
            failure_counts[failure_id] += 1
        
        # Build report
        lines = [
            "=" * 60,
            "WEEKLY QUALITY REPORT",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "=" * 60,
            "",
            "📊 SUMMARY",
            f"  Evaluation runs: {len(recent_runs)}",
            f"  Average pass rate: {avg_pass_rate:.1%}",
            f"  Average score: {avg_score:.2f}",
            "",
            "📈 LATEST RUN",
            f"  Version: {latest.version}",
            f"  Pass rate: {latest.pass_rate:.1%}",
            f"  Score: {latest.overall_score:.2f}",
            f"  Cases: {latest.total_cases}",
        ]
        
        # Category breakdown
        if latest.by_category:
            lines.append("")
            lines.append("📁 BY CATEGORY")
            for cat, stats in latest.by_category.items():
                rate = stats.get('pass_rate', stats.get('accuracy', 0))
                lines.append(f"  {cat}: {rate:.1%}")
        
        # Top failures
        if failure_counts:
            lines.append("")
            lines.append("❌ FREQUENT FAILURES")
            top_failures = sorted(failure_counts.items(), key=lambda x: -x[1])[:5]
            for failure_id, count in top_failures:
                lines.append(f"  {failure_id}: {count} times")
        
        # Trend
        trend = self.tracker.get_trend("pass_rate", days=7)
        if len(trend) >= 2:
            first_rate = trend[0][1]
            last_rate = trend[-1][1]
            change = last_rate - first_rate
            
            lines.append("")
            lines.append("📉 TREND")
            if change > 0.01:
                lines.append(f"  ✅ Improving: +{change:.1%} over the week")
            elif change < -0.01:
                lines.append(f"  ⚠️ Declining: {change:.1%} over the week")
            else:
                lines.append(f"  ➡️ Stable: {change:+.1%} over the week")
        
        # Regression check
        regression = self.tracker.detect_regression()
        if regression and regression.get("detected"):
            lines.append("")
            lines.append("🚨 ALERT")
            lines.append(f"  {regression['message']}")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def improvement_priorities(self) -> list[dict]:
        """
        Identify improvement priorities based on recent data.
        
        Returns list sorted by estimated impact.
        """
        latest = self.tracker.get_latest()
        if not latest:
            return []
        
        priorities = []
        
        # Analyze category performance
        for cat, stats in latest.by_category.items():
            rate = stats.get('pass_rate', stats.get('accuracy', 0))
            count = stats.get('count', stats.get('total', 0))
            
            # Impact = volume * failure rate
            failure_rate = 1 - rate
            impact = count * failure_rate
            
            if failure_rate > 0.1:  # Only flag categories with >10% failure
                priorities.append({
                    "category": cat,
                    "pass_rate": rate,
                    "failure_rate": failure_rate,
                    "volume": count,
                    "estimated_impact": impact,
                    "recommendation": f"Improve {cat} handling (currently {rate:.0%} pass rate)"
                })
        
        # Sort by impact
        priorities.sort(key=lambda x: -x["estimated_impact"])
        
        return priorities


class ScheduledEvaluator:
    """
    Run evaluations on a schedule.
    
    In production, this would be triggered by cron or a task scheduler.
    This class provides the logic for what to run.
    """
    
    def __init__(
        self,
        tracker: QualityTracker,
        evaluate_fn: Callable[[], dict],
        version: str = "current"
    ):
        """
        Args:
            tracker: QualityTracker to record results
            evaluate_fn: Function that runs evaluation and returns results dict
                        Expected format: {"pass_rate": float, "overall_score": float, 
                                         "total_cases": int, "by_category": dict, "failures": list}
            version: Version identifier for this agent
        """
        self.tracker = tracker
        self.evaluate_fn = evaluate_fn
        self.version = version
    
    def run_evaluation(self) -> EvaluationRun:
        """Run evaluation and record results."""
        print(f"🔄 Running evaluation for version {self.version}...")
        
        results = self.evaluate_fn()
        
        run = self.tracker.record(
            version=self.version,
            overall_score=results.get("overall_score", 0),
            pass_rate=results.get("pass_rate", 0),
            total_cases=results.get("total_cases", 0),
            by_category=results.get("by_category", {}),
            failures=results.get("failures", [])
        )
        
        print(f"✅ Evaluation complete: {run.pass_rate:.1%} pass rate")
        
        # Check for regression
        regression = self.tracker.detect_regression()
        if regression and regression.get("detected"):
            print(f"🚨 {regression['message']}")
        
        return run
    
    def should_run(self, schedule: str = "daily") -> bool:
        """
        Check if evaluation should run based on schedule.
        
        Args:
            schedule: "daily", "weekly", or "hourly"
        """
        latest = self.tracker.get_latest()
        if not latest:
            return True  # Never run before
        
        last_run = datetime.fromisoformat(latest.timestamp)
        now = datetime.now()
        
        if schedule == "hourly":
            return (now - last_run) >= timedelta(hours=1)
        elif schedule == "daily":
            return (now - last_run) >= timedelta(days=1)
        elif schedule == "weekly":
            return (now - last_run) >= timedelta(weeks=1)
        
        return True


# Example usage
if __name__ == "__main__":
    import random
    
    # Initialize tracker
    tracker = QualityTracker("demo_quality_history.json")
    
    # Simulate some historical evaluation runs
    print("Simulating evaluation history...")
    
    categories = ["password_reset", "order_status", "refunds", "technical"]
    
    for i in range(10):
        # Simulate gradually improving performance
        base_rate = 0.75 + (i * 0.015) + random.uniform(-0.03, 0.03)
        
        by_category = {}
        for cat in categories:
            cat_rate = base_rate + random.uniform(-0.1, 0.1)
            cat_rate = max(0.5, min(1.0, cat_rate))
            by_category[cat] = {
                "pass_rate": cat_rate,
                "count": random.randint(20, 50)
            }
        
        failures = []
        if random.random() > base_rate:
            failures.append({"case_id": f"case_{random.randint(1, 100)}"})
        
        tracker.record(
            version=f"v1.{i}",
            overall_score=base_rate * 5,  # Score out of 5
            pass_rate=base_rate,
            total_cases=100,
            by_category=by_category,
            failures=failures
        )
    
    # Generate reports
    reporter = QualityReporter(tracker)
    
    print("\n" + reporter.weekly_report())
    
    # Show improvement priorities
    print("\n📋 IMPROVEMENT PRIORITIES")
    print("-" * 40)
    priorities = reporter.improvement_priorities()
    for i, p in enumerate(priorities[:3], 1):
        print(f"{i}. {p['recommendation']}")
        print(f"   Impact score: {p['estimated_impact']:.1f}")
    
    # Compare to baseline
    print("\n📊 COMPARISON TO BASELINE")
    print("-" * 40)
    comparison = tracker.compare_to_baseline("v1.0")
    if comparison:
        print(f"Baseline (v1.0): {comparison['baseline']['pass_rate']:.1%}")
        print(f"Current: {comparison['current']['pass_rate']:.1%}")
        print(f"Change: {comparison['change']['pass_rate']:+.1%}")
        status = "✅ Improved!" if comparison['improved'] else "⚠️ Declined"
        print(f"Status: {status}")
    
    # Clean up demo file
    Path("demo_quality_history.json").unlink(missing_ok=True)
