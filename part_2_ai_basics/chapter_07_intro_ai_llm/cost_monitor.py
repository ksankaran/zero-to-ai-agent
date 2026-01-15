# From: Zero to AI Agent, Chapter 7, Section 7.7
# File: cost_monitor.py

"""
Monitor and control API spending with budgets and alerts.
Includes free alternatives for students and hobbyists.
"""

from datetime import datetime, date
from typing import Dict, List, Optional
import json
from pathlib import Path


class CostMonitor:
    """
    Monitor and control API spending with comprehensive tracking
    """
    
    def __init__(self, daily_budget: float = 10.0, alert_threshold: float = 0.8):
        """
        Initialize cost monitor
        
        Args:
            daily_budget: Maximum daily spending allowed
            alert_threshold: Alert when this fraction of budget is used
        """
        self.daily_budget = daily_budget
        self.alert_threshold = alert_threshold
        
        # Track costs by date
        self.daily_costs = {}
        
        # Track by model
        self.model_costs = {}
        
        # Overall statistics
        self.total_spent = 0.0
        self.request_count = 0
        self.total_tokens = 0
        
        # Alerts
        self.alerts_triggered = []
        
    def track_request(self, cost: float, model: str, tokens: int) -> Dict:
        """
        Track a request and check budget
        
        Args:
            cost: Cost of this request
            model: Model used
            tokens: Tokens used
        
        Returns:
            Status dictionary with budget information
        
        Raises:
            Exception: If daily budget is exceeded
        """
        today = datetime.now().date()
        
        # Initialize today's tracking if needed
        if today not in self.daily_costs:
            self.daily_costs[today] = {
                "cost": 0,
                "requests": 0,
                "tokens": 0,
                "models": {}
            }
        
        # Update daily totals
        self.daily_costs[today]["cost"] += cost
        self.daily_costs[today]["requests"] += 1
        self.daily_costs[today]["tokens"] += tokens
        
        # Track by model
        if model not in self.daily_costs[today]["models"]:
            self.daily_costs[today]["models"][model] = {"cost": 0, "requests": 0}
        
        self.daily_costs[today]["models"][model]["cost"] += cost
        self.daily_costs[today]["models"][model]["requests"] += 1
        
        # Update global tracking
        self.total_spent += cost
        self.request_count += 1
        self.total_tokens += tokens
        
        if model not in self.model_costs:
            self.model_costs[model] = {"cost": 0, "requests": 0, "tokens": 0}
        
        self.model_costs[model]["cost"] += cost
        self.model_costs[model]["requests"] += 1
        self.model_costs[model]["tokens"] += tokens
        
        # Check budget
        daily_spent = self.daily_costs[today]["cost"]
        budget_percent = daily_spent / self.daily_budget
        
        status = {
            "daily_spent": daily_spent,
            "daily_budget": self.daily_budget,
            "remaining": self.daily_budget - daily_spent,
            "percent_used": budget_percent * 100,
            "status": "OK"
        }
        
        # Check if budget exceeded
        if daily_spent > self.daily_budget:
            status["status"] = "EXCEEDED"
            alert = f"❌ Daily budget exceeded! Spent ${daily_spent:.2f} / ${self.daily_budget:.2f}"
            self.alerts_triggered.append({"time": datetime.now(), "message": alert})
            raise Exception(alert)
        
        # Check if approaching limit
        elif budget_percent > self.alert_threshold:
            status["status"] = "WARNING"
            alert = f"⚠️ Warning: {budget_percent*100:.0f}% of daily budget used"
            print(alert)
            self.alerts_triggered.append({"time": datetime.now(), "message": alert})
        
        return status
    
    def get_daily_report(self, date: Optional[date] = None) -> str:
        """
        Get spending report for a specific day
        
        Args:
            date: Date to report on (None for today)
        
        Returns:
            Formatted report string
        """
        target_date = date or datetime.now().date()
        
        if target_date not in self.daily_costs:
            return f"No data for {target_date}"
        
        data = self.daily_costs[target_date]
        
        report = []
        report.append(f"Daily Report: {target_date}")
        report.append("=" * 50)
        report.append(f"Total Cost: ${data['cost']:.2f} / ${self.daily_budget:.2f}")
        report.append(f"Requests: {data['requests']}")
        report.append(f"Tokens: {data['tokens']:,}")
        
        if data['requests'] > 0:
            report.append(f"Avg cost/request: ${data['cost']/data['requests']:.4f}")
            report.append(f"Avg tokens/request: {data['tokens']/data['requests']:.0f}")
        
        if data["models"]:
            report.append("\nBy Model:")
            for model, stats in data["models"].items():
                report.append(f"  {model}:")
                report.append(f"    Cost: ${stats['cost']:.4f}")
                report.append(f"    Requests: {stats['requests']}")
        
        return "\n".join(report)
    
    def get_full_report(self) -> str:
        """Generate comprehensive spending report"""
        
        report = []
        report.append("="*60)
        report.append("API SPENDING REPORT")
        report.append("="*60)
        
        # Summary
        report.append(f"\n📊 SUMMARY")
        report.append(f"Total Spent: ${self.total_spent:.2f}")
        report.append(f"Total Requests: {self.request_count}")
        report.append(f"Total Tokens: {self.total_tokens:,}")
        
        if self.request_count > 0:
            report.append(f"Average Cost: ${self.total_spent/self.request_count:.4f}/request")
            report.append(f"Average Tokens: {self.total_tokens/self.request_count:.0f}/request")
        
        # Daily breakdown
        report.append(f"\n📅 DAILY BREAKDOWN")
        for day, data in sorted(self.daily_costs.items(), reverse=True)[:7]:  # Last 7 days
            budget_percent = (data['cost'] / self.daily_budget) * 100
            status = "✅" if budget_percent < 80 else "⚠️" if budget_percent < 100 else "❌"
            report.append(f"\n{day}: {status}")
            report.append(f"  Cost: ${data['cost']:.2f} ({budget_percent:.0f}% of budget)")
            report.append(f"  Requests: {data['requests']}")
        
        # Model breakdown
        if self.model_costs:
            report.append(f"\n🤖 MODEL USAGE")
            sorted_models = sorted(self.model_costs.items(), 
                                 key=lambda x: x[1]["cost"], reverse=True)
            
            for model, stats in sorted_models:
                cost_percent = (stats["cost"] / self.total_spent) * 100
                report.append(f"\n{model}:")
                report.append(f"  Cost: ${stats['cost']:.2f} ({cost_percent:.1f}% of total)")
                report.append(f"  Requests: {stats['requests']}")
                report.append(f"  Avg: ${stats['cost']/stats['requests']:.4f}/request")
        
        # Recent alerts
        if self.alerts_triggered:
            report.append(f"\n⚠️ RECENT ALERTS")
            for alert in self.alerts_triggered[-5:]:
                report.append(f"  {alert['time'].strftime('%Y-%m-%d %H:%M')}: {alert['message']}")
        
        # Recommendations
        report.append(f"\n💡 RECOMMENDATIONS")
        if self.total_spent > 0:
            # Find most expensive model
            if self.model_costs:
                most_expensive = max(self.model_costs.items(), key=lambda x: x[1]["cost"])
                if most_expensive[1]["cost"] / self.total_spent > 0.5:
                    report.append(f"  • Consider using cheaper models (50%+ spent on {most_expensive[0]})")
            
            # Check daily patterns
            avg_daily = self.total_spent / len(self.daily_costs)
            if avg_daily > self.daily_budget * 0.8:
                report.append(f"  • Average daily spend (${avg_daily:.2f}) approaching budget")
        
        return "\n".join(report)
    
    def export_data(self, filename: str = "cost_data.json"):
        """Export cost data to JSON file"""
        
        data = {
            "export_time": datetime.now().isoformat(),
            "total_spent": self.total_spent,
            "request_count": self.request_count,
            "total_tokens": self.total_tokens,
            "daily_budget": self.daily_budget,
            "daily_costs": {
                str(day): info for day, info in self.daily_costs.items()
            },
            "model_costs": self.model_costs,
            "alerts": [
                {"time": alert["time"].isoformat(), "message": alert["message"]}
                for alert in self.alerts_triggered
            ]
        }
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"📁 Cost data exported to {filename}")
    
    def predict_monthly_cost(self) -> float:
        """Predict monthly cost based on current usage"""
        
        if not self.daily_costs:
            return 0
        
        # Calculate average daily spend
        avg_daily = self.total_spent / len(self.daily_costs)
        
        # Project to 30 days
        projected = avg_daily * 30
        
        return projected


def free_ai_options() -> Dict:
    """
    Ways to use AI without spending money
    Perfect for students and hobbyists!
    """
    
    options = {
        "Google Gemini": {
            "free_tier": "60 requests/minute",
            "limits": "1,500 requests/day",
            "good_for": "Experimentation, learning, prototyping",
            "setup": "Just need Google account",
            "how_to": """
1. Go to aistudio.google.com
2. Sign in with Google account
3. Get API key (no credit card!)
4. Start building!
            """,
            "cost": "FREE",
            "quality": "⭐⭐⭐⭐"
        },
        
        "OpenAI Free Credits": {
            "free_tier": "$5 for new accounts (sometimes)",
            "limits": "Expires after 3 months",
            "good_for": "Initial testing, learning GPT",
            "setup": "New phone number required",
            "how_to": """
1. Sign up at platform.openai.com
2. Verify phone number
3. Check for free credits
4. Use wisely - it goes fast!
            """,
            "cost": "FREE (limited)",
            "quality": "⭐⭐⭐⭐⭐"
        },
        
        "Hugging Face Inference": {
            "free_tier": "Rate-limited access to many models",
            "limits": "Slow, queued requests",
            "good_for": "Testing open models, learning",
            "setup": "Free account",
            "how_to": """
1. Create account at huggingface.co
2. Get API token
3. Use Inference API
4. Expect delays during peak times
            """,
            "cost": "FREE",
            "quality": "⭐⭐⭐"
        },
        
        "Local Open Source (Ollama)": {
            "free_tier": "Unlimited (your hardware)",
            "limits": "Need decent GPU or lots of patience",
            "good_for": "Privacy, unlimited use, learning",
            "setup": "Install Ollama",
            "how_to": """
1. Download from ollama.ai
2. Run: ollama pull llama2
3. Run: ollama run llama2
4. Use via API or CLI
            """,
            "cost": "FREE (your electricity)",
            "quality": "⭐⭐⭐ (depends on model)"
        },
        
        "Colab + Open Models": {
            "free_tier": "Free GPU time (limited)",
            "limits": "Session limits, disconnections",
            "good_for": "Experiments, learning, notebooks",
            "setup": "Google account + notebooks",
            "how_to": """
1. Go to colab.research.google.com
2. Create new notebook
3. Use Transformers library
4. Load open models
            """,
            "cost": "FREE",
            "quality": "⭐⭐⭐⭐"
        },
        
        "Replicate Free Tier": {
            "free_tier": "Free predictions for public models",
            "limits": "Very limited, mostly for testing",
            "good_for": "Trying different models",
            "setup": "GitHub account",
            "how_to": """
1. Sign up at replicate.com
2. Get API token
3. Use public models
4. Watch usage carefully
            """,
            "cost": "FREE (very limited)",
            "quality": "⭐⭐⭐⭐"
        }
    }
    
    print("="*60)
    print("🎓 FREE AI OPTIONS FOR STUDENTS")
    print("="*60)
    
    for name, info in options.items():
        print(f"\n📌 {name}")
        print(f"   Cost: {info['cost']}")
        print(f"   Quality: {info['quality']}")
        print(f"   Free Tier: {info['free_tier']}")
        print(f"   Good For: {info['good_for']}")
        print(f"   Limits: {info['limits']}")
    
    print("\n" + "="*60)
    print("💡 RECOMMENDATIONS BY USE CASE")
    print("="*60)
    
    recommendations = {
        "Just Learning": ["Google Gemini (best free option)", "Local Ollama"],
        "Building Projects": ["Google Gemini", "OpenAI free credits"],
        "Research/Experiments": ["Colab + Open Models", "Hugging Face"],
        "Production Apps": ["Start with Gemini free tier", "Then upgrade as needed"]
    }
    
    for use_case, recs in recommendations.items():
        print(f"\n{use_case}:")
        for rec in recs:
            print(f"  • {rec}")
    
    return options


def student_budget_strategies():
    """Budget-conscious strategies for students"""
    
    print("\n" + "="*60)
    print("💰 STUDENT BUDGET STRATEGIES")
    print("="*60)
    
    strategies = [
        {
            "strategy": "Start Free, Upgrade Later",
            "how": "Use Google Gemini free tier until you hit limits",
            "savings": "$50-100/month"
        },
        {
            "strategy": "Cache Everything",
            "how": "Never make the same API call twice",
            "savings": "50-70% reduction"
        },
        {
            "strategy": "Use Cheap Models First",
            "how": "Try Gemini/Haiku before GPT-4",
            "savings": "10-100x cost difference"
        },
        {
            "strategy": "Batch Requests",
            "how": "Process multiple items per API call",
            "savings": "30-50% reduction"
        },
        {
            "strategy": "Local for Development",
            "how": "Use Ollama locally, API for production",
            "savings": "$20-50/month"
        },
        {
            "strategy": "Share API Keys (Carefully!)",
            "how": "Team projects can share costs",
            "savings": "Split costs 3-4 ways"
        },
        {
            "strategy": "Use University Resources",
            "how": "Many universities provide compute credits",
            "savings": "$100-500/month"
        }
    ]
    
    for s in strategies:
        print(f"\n📋 {s['strategy']}")
        print(f"   How: {s['how']}")
        print(f"   Potential Savings: {s['savings']}")
    
    print("\n" + "="*60)
    print("📚 STUDENT STARTER STACK (All Free!)")
    print("="*60)
    print("""
1. Development: Google Gemini (free tier)
2. Experiments: Colab notebooks
3. Local testing: Ollama with Llama 2
4. Version control: GitHub (free)
5. Deployment: Vercel/Netlify (free tier)

Total Cost: $0/month
Capabilities: Build full AI applications!
    """)


def demonstrate_cost_monitoring():
    """Demonstrate cost monitoring in action"""
    
    print("="*60)
    print("COST MONITORING DEMONSTRATION")
    print("="*60)
    
    # Create monitor
    monitor = CostMonitor(daily_budget=5.0)
    
    # Simulate some API calls
    api_calls = [
        {"cost": 0.002, "model": "gpt-3.5-turbo", "tokens": 150},
        {"cost": 0.003, "model": "gpt-3.5-turbo", "tokens": 200},
        {"cost": 0.09, "model": "gpt-4", "tokens": 1000},
        {"cost": 0.001, "model": "gemini-pro", "tokens": 100},
        {"cost": 0.002, "model": "gpt-3.5-turbo", "tokens": 150},
        {"cost": 0.05, "model": "gpt-4", "tokens": 500},
        {"cost": 0.0005, "model": "gemini-pro", "tokens": 50},
        {"cost": 0.002, "model": "gpt-3.5-turbo", "tokens": 150},
    ]
    
    print("\n📊 Tracking API Calls:")
    for i, call in enumerate(api_calls, 1):
        print(f"\nCall {i}: {call['model']} (${call['cost']:.4f})")
        
        try:
            status = monitor.track_request(call["cost"], call["model"], call["tokens"])
            print(f"  Budget: ${status['daily_spent']:.4f} / ${status['daily_budget']:.2f}")
            print(f"  Status: {status['status']}")
        except Exception as e:
            print(f"  {e}")
            break
    
    # Show reports
    print("\n" + monitor.get_daily_report())
    print("\n" + monitor.get_full_report())
    
    # Predict monthly cost
    projected = monitor.predict_monthly_cost()
    print(f"\n📈 Projected Monthly Cost: ${projected:.2f}")
    
    # Export data
    monitor.export_data("demo_cost_data.json")


if __name__ == "__main__":
    # Show free options
    free_ai_options()
    
    # Student strategies
    student_budget_strategies()
    
    # Demonstrate monitoring
    print("\n")
    demonstrate_cost_monitoring()
