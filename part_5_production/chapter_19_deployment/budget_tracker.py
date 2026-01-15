# From: Zero to AI Agent, Chapter 19, Section 19.6
# File: budget_tracker.py
# Description: Track and limit API spending

import asyncio
from datetime import datetime, timedelta
class BudgetTracker:
    """Track and limit API spending."""

    # Cost per 1K tokens by model (average of input/output)
    COST_PER_1K = {
        "gpt-4o": 0.01,
        "gpt-4o-mini": 0.0004,
        "gpt-3.5-turbo": 0.001,
        "gpt-4-turbo": 0.02,
    }

    def __init__(self, daily_budget: float = 10.0):
        self.daily_budget = daily_budget
        self.spending: list[tuple[datetime, float]] = []
        self._lock = asyncio.Lock()
    
    async def record_cost(self, tokens: int, model: str):
        """Record spending from a request."""
        cost_per_1k = self.COST_PER_1K.get(model, 0.01)
        cost = (tokens / 1000) * cost_per_1k
        
        async with self._lock:
            self.spending.append((datetime.now(), cost))
            # Clean old entries (older than 24 hours)
            cutoff = datetime.now() - timedelta(days=1)
            self.spending = [(t, c) for t, c in self.spending if t > cutoff]
    
    async def get_daily_spending(self) -> float:
        """Get total spending in last 24 hours."""
        async with self._lock:
            cutoff = datetime.now() - timedelta(days=1)
            return sum(c for t, c in self.spending if t > cutoff)
    
    async def check_budget(self) -> tuple[bool, float]:
        """
        Check if within budget.
        
        Returns:
            Tuple of (allowed, remaining_budget)
        """
        spent = await self.get_daily_spending()
        remaining = self.daily_budget - spent
        return remaining > 0, remaining
    
    async def get_stats(self) -> dict:
        """Get budget statistics."""
        spent = await self.get_daily_spending()
        remaining = self.daily_budget - spent
        percent_used = (spent / self.daily_budget) * 100 if self.daily_budget > 0 else 0
        
        # Determine status
        if percent_used >= 100:
            status = "exceeded"
        elif percent_used >= 80:
            status = "warning"
        else:
            status = "healthy"
        
        return {
            "daily_budget": self.daily_budget,
            "spent_today": round(spent, 4),
            "remaining": round(remaining, 4),
            "percent_used": round(percent_used, 1),
            "status": status
        }


# Global budget tracker
budget = BudgetTracker(daily_budget=10.0)


# Example usage with FastAPI
"""
from fastapi import FastAPI, HTTPException

@app.post("/v1/chat")
async def chat(request: ChatRequest):
    # Check budget before processing
    allowed, remaining = await budget.check_budget()
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Daily budget exceeded. Try again tomorrow."
        )
    
    # Warn if budget is low
    if remaining < 1.0:
        logger.warning(f"Budget low: ${remaining:.2f} remaining")
    
    # Process request...
    result = await agent.ainvoke(...)
    
    # Record cost (get actual token count from response)
    await budget.record_cost(tokens=500, model="gpt-4o-mini")
    
    return ChatResponse(...)
"""


if __name__ == "__main__":
    async def test_budget():
        tracker = BudgetTracker(daily_budget=1.0)
        
        # Simulate some requests
        for i in range(10):
            await tracker.record_cost(tokens=1000, model="gpt-4o-mini")
            allowed, remaining = await tracker.check_budget()
            stats = await tracker.get_stats()
            print(f"Request {i+1}: allowed={allowed}, remaining=${remaining:.4f}, status={stats['status']}")
    
    asyncio.run(test_budget())
