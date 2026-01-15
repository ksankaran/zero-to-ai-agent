# From: Zero to AI Agent, Chapter 19, Section 19.6
# File: exercise_3_19_6_solution.py (cost_dashboard.py)
# Description: Comprehensive cost dashboard with hourly spending, model breakdown, and projections

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List
from dataclasses import dataclass
from collections import defaultdict
from fastapi import FastAPI


@dataclass
class CostRecord:
    """Record of a single API cost."""
    timestamp: datetime
    conversation_id: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    cost: float


class CostDashboard:
    """Track and report API costs."""
    
    # Cost per 1K tokens by model
    MODEL_COSTS = {
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    }
    
    def __init__(self, daily_budget: float = 50.0):
        self.records: List[CostRecord] = []
        self.daily_budget = daily_budget
        self._lock = asyncio.Lock()
    
    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost for a request."""
        costs = self.MODEL_COSTS.get(model, {"input": 0.01, "output": 0.03})
        input_cost = (prompt_tokens / 1000) * costs["input"]
        output_cost = (completion_tokens / 1000) * costs["output"]
        return input_cost + output_cost
    
    async def record(
        self,
        conversation_id: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int
    ):
        """Record a cost event."""
        cost = self._calculate_cost(model, prompt_tokens, completion_tokens)
        
        record = CostRecord(
            timestamp=datetime.now(),
            conversation_id=conversation_id,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=cost
        )
        
        async with self._lock:
            self.records.append(record)
            # Keep only last 7 days
            cutoff = datetime.now() - timedelta(days=7)
            self.records = [r for r in self.records if r.timestamp > cutoff]
    
    async def get_hourly_spending(self, hours: int = 24) -> List[Dict]:
        """Get spending broken down by hour."""
        async with self._lock:
            now = datetime.now()
            cutoff = now - timedelta(hours=hours)
            
            hourly = defaultdict(float)
            for record in self.records:
                if record.timestamp > cutoff:
                    hour_key = record.timestamp.strftime("%Y-%m-%d %H:00")
                    hourly[hour_key] += record.cost
            
            # Fill in missing hours with 0
            result = []
            for i in range(hours):
                hour = now - timedelta(hours=i)
                hour_key = hour.strftime("%Y-%m-%d %H:00")
                result.append({
                    "hour": hour_key,
                    "cost": round(hourly.get(hour_key, 0), 4)
                })
            
            return list(reversed(result))
    
    async def get_spending_by_model(self) -> Dict[str, Dict]:
        """Get spending breakdown by model."""
        async with self._lock:
            cutoff = datetime.now() - timedelta(days=1)
            
            by_model = defaultdict(lambda: {
                "requests": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "cost": 0.0
            })
            
            for record in self.records:
                if record.timestamp > cutoff:
                    by_model[record.model]["requests"] += 1
                    by_model[record.model]["prompt_tokens"] += record.prompt_tokens
                    by_model[record.model]["completion_tokens"] += record.completion_tokens
                    by_model[record.model]["cost"] += record.cost
            
            # Round costs
            for model in by_model:
                by_model[model]["cost"] = round(by_model[model]["cost"], 4)
            
            return dict(by_model)
    
    async def get_expensive_conversations(self, limit: int = 10) -> List[Dict]:
        """Get the most expensive conversations."""
        async with self._lock:
            cutoff = datetime.now() - timedelta(days=1)
            
            by_conversation = defaultdict(lambda: {
                "requests": 0,
                "total_tokens": 0,
                "cost": 0.0
            })
            
            for record in self.records:
                if record.timestamp > cutoff:
                    conv = by_conversation[record.conversation_id]
                    conv["requests"] += 1
                    conv["total_tokens"] += record.prompt_tokens + record.completion_tokens
                    conv["cost"] += record.cost
            
            # Sort by cost and take top N
            sorted_convs = sorted(
                by_conversation.items(),
                key=lambda x: x[1]["cost"],
                reverse=True
            )[:limit]
            
            return [
                {
                    "conversation_id": conv_id,
                    "requests": data["requests"],
                    "total_tokens": data["total_tokens"],
                    "cost": round(data["cost"], 4)
                }
                for conv_id, data in sorted_convs
            ]
    
    async def get_projected_monthly(self) -> Dict:
        """Project monthly cost based on recent usage."""
        async with self._lock:
            # Get last 24 hours
            cutoff = datetime.now() - timedelta(days=1)
            daily_cost = sum(
                r.cost for r in self.records if r.timestamp > cutoff
            )
            
            # Project to monthly
            monthly_projected = daily_cost * 30
            
            return {
                "daily_actual": round(daily_cost, 2),
                "monthly_projected": round(monthly_projected, 2),
                "daily_budget": self.daily_budget,
                "monthly_budget": self.daily_budget * 30
            }
    
    async def get_budget_status(self) -> Dict:
        """Get current budget status with visual indicator."""
        async with self._lock:
            cutoff = datetime.now() - timedelta(days=1)
            spent_today = sum(
                r.cost for r in self.records if r.timestamp > cutoff
            )
            
            remaining = self.daily_budget - spent_today
            percent_used = (spent_today / self.daily_budget) * 100 if self.daily_budget > 0 else 0
            
            # Determine status
            if percent_used >= 100:
                status = "exceeded"
                indicator = "🔴"
            elif percent_used >= 80:
                status = "warning"
                indicator = "🟡"
            else:
                status = "healthy"
                indicator = "🟢"
            
            return {
                "status": status,
                "indicator": indicator,
                "spent_today": round(spent_today, 4),
                "daily_budget": self.daily_budget,
                "remaining": round(remaining, 4),
                "percent_used": round(percent_used, 1)
            }
    
    async def get_full_dashboard(self) -> Dict:
        """Get complete cost dashboard data."""
        return {
            "generated_at": datetime.now().isoformat(),
            "budget_status": await self.get_budget_status(),
            "hourly_spending": await self.get_hourly_spending(24),
            "spending_by_model": await self.get_spending_by_model(),
            "expensive_conversations": await self.get_expensive_conversations(10),
            "projections": await self.get_projected_monthly()
        }


# FastAPI integration
app = FastAPI()
costs = CostDashboard(daily_budget=10.0)


@app.get("/costs")
async def cost_dashboard():
    """Get the full cost dashboard."""
    return await costs.get_full_dashboard()


@app.get("/costs/budget")
async def budget_status():
    """Get current budget status."""
    return await costs.get_budget_status()


@app.get("/costs/hourly")
async def hourly_costs(hours: int = 24):
    """Get hourly spending breakdown."""
    return await costs.get_hourly_spending(hours)


@app.get("/costs/by-model")
async def model_costs():
    """Get spending by model."""
    return await costs.get_spending_by_model()


@app.get("/costs/expensive")
async def expensive_conversations(limit: int = 10):
    """Get most expensive conversations."""
    return await costs.get_expensive_conversations(limit)


# Simulate some data for testing
async def simulate_data():
    """Generate sample data for testing."""
    import random
    
    models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
    conversations = [f"conv-{i}" for i in range(20)]
    
    # Generate records over last 24 hours
    for i in range(100):
        await costs.record(
            conversation_id=random.choice(conversations),
            model=random.choice(models),
            prompt_tokens=random.randint(100, 2000),
            completion_tokens=random.randint(50, 1000)
        )
        # Spread timestamps
        costs.records[-1].timestamp = datetime.now() - timedelta(
            hours=random.uniform(0, 24)
        )


if __name__ == "__main__":
    # Test the dashboard
    async def main():
        await simulate_data()
        dashboard = await costs.get_full_dashboard()
        
        import json
        print(json.dumps(dashboard, indent=2, default=str))
    
    asyncio.run(main())
