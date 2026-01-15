# From: Zero to AI Agent, Chapter 15, Section 15.7
# File: exercise_3_15_7_solution.py

"""
Simple alerting system with thresholds and severity.
"""

from datetime import datetime
from enum import Enum
from dataclasses import dataclass

class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class Alert:
    severity: Severity
    metric: str
    message: str
    value: float
    threshold: float
    timestamp: str

class AlertSystem:
    """Monitor metrics and trigger alerts."""
    
    def __init__(self):
        self.thresholds = {}
        self.alerts = []
        self.metrics = {}
    
    def set_threshold(self, metric: str, warning: float, critical: float):
        """Set alert thresholds for a metric."""
        self.thresholds[metric] = {
            "warning": warning,
            "critical": critical
        }
    
    def update_metric(self, metric: str, value: float):
        """Update a metric and check for alerts."""
        self.metrics[metric] = value
        
        if metric in self.thresholds:
            t = self.thresholds[metric]
            
            if value >= t["critical"]:
                self._trigger(Severity.CRITICAL, metric, value, t["critical"])
            elif value >= t["warning"]:
                self._trigger(Severity.WARNING, metric, value, t["warning"])
    
    def _trigger(self, severity: Severity, metric: str, value: float, threshold: float):
        """Trigger an alert."""
        alert = Alert(
            severity=severity,
            metric=metric,
            message=f"{metric} is {value:.1f} (threshold: {threshold:.1f})",
            value=value,
            threshold=threshold,
            timestamp=datetime.now().isoformat()
        )
        self.alerts.append(alert)
        
        # Print immediately
        icon = "🔴" if severity == Severity.CRITICAL else "🟡"
        print(f"{icon} [{severity.value.upper()}] {alert.message}")
    
    def get_active_alerts(self) -> list[Alert]:
        """Get alerts from last hour."""
        # In real system, filter by time
        return self.alerts[-10:]  # Last 10 for demo
    
    def print_status(self):
        """Print current status."""
        print("\n" + "═" * 50)
        print("🚨 ALERT SYSTEM STATUS")
        print("═" * 50)
        
        print("\n📊 Current Metrics:")
        for metric, value in self.metrics.items():
            status = "✓"
            if metric in self.thresholds:
                t = self.thresholds[metric]
                if value >= t["critical"]:
                    status = "🔴"
                elif value >= t["warning"]:
                    status = "🟡"
            print(f"  {status} {metric}: {value:.1f}")
        
        print(f"\n📋 Alert History ({len(self.alerts)} total):")
        for alert in self.alerts[-5:]:
            icon = "🔴" if alert.severity == Severity.CRITICAL else "🟡"
            print(f"  {icon} {alert.message}")
        
        print("═" * 50)

# Demo
if __name__ == "__main__":
    alerts = AlertSystem()
    
    # Set thresholds
    alerts.set_threshold("error_rate", warning=5.0, critical=10.0)
    alerts.set_threshold("latency_ms", warning=500, critical=1000)
    alerts.set_threshold("queue_size", warning=100, critical=200)
    
    print("=== Alert System Demo ===\n")
    
    # Simulate metrics - all OK
    print("Initial metrics (all OK):")
    alerts.update_metric("error_rate", 3.0)   # OK
    alerts.update_metric("latency_ms", 250)   # OK
    alerts.update_metric("queue_size", 50)    # OK
    
    print("\n--- Situation worsens ---\n")
    
    alerts.update_metric("error_rate", 7.0)   # Warning!
    alerts.update_metric("latency_ms", 1200)  # Critical!
    alerts.update_metric("queue_size", 150)   # Warning!
    
    alerts.print_status()
