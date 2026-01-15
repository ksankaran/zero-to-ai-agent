# From: Zero to AI Agent, Chapter 19, Section 19.4
# File: exercise_3_19_4_solution.py
# Exercise 3: Automated Alerting System

import asyncio
import httpx
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
from dataclasses import dataclass
from collections import deque

logger = logging.getLogger("agent_api.alerts")


@dataclass
class Alert:
    """Represents an alert."""
    alert_type: str
    message: str
    severity: str  # "warning", "error", "critical"
    timestamp: datetime
    metadata: Dict = None


class AlertManager:
    """Manage and rate-limit alerts."""
    
    def __init__(
        self,
        webhook_url: Optional[str] = None,
        rate_limit_minutes: int = 5
    ):
        self.webhook_url = webhook_url or os.getenv("ALERT_WEBHOOK_URL")
        self.rate_limit_minutes = rate_limit_minutes
        
        # Track recent alerts for rate limiting
        self.recent_alerts: Dict[str, datetime] = {}
        
        # Track recent requests for threshold calculations
        self.recent_requests: deque = deque(maxlen=100)
    
    def _is_rate_limited(self, alert_type: str) -> bool:
        """Check if this alert type is rate limited."""
        if alert_type not in self.recent_alerts:
            return False
        
        last_sent = self.recent_alerts[alert_type]
        cooldown = timedelta(minutes=self.rate_limit_minutes)
        
        return datetime.now() - last_sent < cooldown
    
    def _record_alert_sent(self, alert_type: str):
        """Record that an alert was sent."""
        self.recent_alerts[alert_type] = datetime.now()
    
    async def send_alert(self, alert: Alert) -> bool:
        """Send an alert if not rate limited."""
        # Check rate limit
        if self._is_rate_limited(alert.alert_type):
            logger.debug(f"Alert rate limited: {alert.alert_type}")
            return False
        
        # Log the alert
        logger.warning(
            f"ALERT [{alert.severity.upper()}] {alert.alert_type}: {alert.message}"
        )
        
        # Send to webhook if configured
        if self.webhook_url:
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(
                        self.webhook_url,
                        json={
                            "alert_type": alert.alert_type,
                            "message": alert.message,
                            "severity": alert.severity,
                            "timestamp": alert.timestamp.isoformat(),
                            "metadata": alert.metadata or {}
                        },
                        timeout=5.0
                    )
            except Exception as e:
                logger.error(f"Failed to send alert to webhook: {e}")
        
        # Record that we sent this alert
        self._record_alert_sent(alert.alert_type)
        return True
    
    def record_request(self, success: bool, duration_ms: int):
        """Record a request for threshold monitoring."""
        self.recent_requests.append({
            "success": success,
            "duration_ms": duration_ms,
            "timestamp": datetime.now()
        })
    
    async def check_thresholds(self):
        """Check if any thresholds are exceeded and send alerts."""
        if len(self.recent_requests) < 10:
            return  # Not enough data
        
        # Get last 10 requests
        recent = list(self.recent_requests)[-10:]
        
        # Check error rate (threshold: 20%)
        error_count = sum(1 for r in recent if not r["success"])
        error_rate = error_count / len(recent) * 100
        
        if error_rate > 20:
            await self.send_alert(Alert(
                alert_type="high_error_rate",
                message=f"Error rate is {error_rate:.1f}% (threshold: 20%)",
                severity="error",
                timestamp=datetime.now(),
                metadata={"error_rate": error_rate, "sample_size": len(recent)}
            ))
        
        # Check response time (threshold: 10 seconds)
        avg_duration = sum(r["duration_ms"] for r in recent) / len(recent)
        
        if avg_duration > 10000:  # 10 seconds in ms
            await self.send_alert(Alert(
                alert_type="high_latency",
                message=f"Average response time is {avg_duration/1000:.1f}s (threshold: 10s)",
                severity="warning",
                timestamp=datetime.now(),
                metadata={"avg_duration_ms": avg_duration, "sample_size": len(recent)}
            ))


# Global alert manager
alerts = AlertManager(rate_limit_minutes=5)


# Example FastAPI integration
from fastapi import FastAPI, Depends

app = FastAPI()

async def verify_api_key():
    return "test-key"


@app.post("/v1/chat")
async def chat(message: str, api_key: str = Depends(verify_api_key)):
    start_time = datetime.now()
    success = False
    duration_ms = 0
    
    try:
        # Simulate agent processing
        await asyncio.sleep(0.1)
        success = True
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return {"response": "Simulated response", "duration_ms": duration_ms}
        
    except Exception as e:
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        raise
        
    finally:
        # Record for threshold monitoring
        alerts.record_request(success, duration_ms)
        
        # Check thresholds (non-blocking)
        asyncio.create_task(alerts.check_thresholds())


# Test the alerting system
async def test_alerts():
    """Test the alerting system."""
    print("Testing high error rate alert...")
    
    # Simulate high error rate
    for i in range(10):
        alerts.record_request(success=False, duration_ms=500)
    
    await alerts.check_thresholds()
    # Should trigger high_error_rate alert
    
    print("\nTesting rate limiting (same alert shouldn't fire twice)...")
    await alerts.check_thresholds()
    # Should be rate limited
    
    print("\nTesting high latency alert...")
    # Clear and simulate high latency
    alerts.recent_requests.clear()
    for i in range(10):
        alerts.record_request(success=True, duration_ms=15000)  # 15 seconds
    
    # Use a different alert manager to avoid rate limiting
    alerts2 = AlertManager(rate_limit_minutes=0)
    alerts2.recent_requests = alerts.recent_requests
    await alerts2.check_thresholds()
    # Should trigger high_latency alert


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(test_alerts())
