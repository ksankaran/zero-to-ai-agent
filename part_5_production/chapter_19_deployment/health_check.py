# From: Zero to AI Agent, Chapter 19, Section 19.4
# File: health_check.py

from dotenv import load_dotenv
from datetime import datetime
from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Import metrics from your metrics module
# from metrics_collector import metrics

app = FastAPI()

# Placeholder for metrics (in real app, import from metrics_collector)
class MockMetrics:
    def get_summary(self):
        return {"success_rate": 95.0}

metrics = MockMetrics()


@app.get("/health")
async def health_check():
    """
    Comprehensive health check.
    Returns 200 if healthy, 503 if unhealthy.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "checks": {}
    }
    
    # Check 1: Can we reach the LLM?
    try:
        # Quick test call (consider caching this result)
        llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=5)
        llm.invoke("Hi")
        health_status["checks"]["llm"] = "ok"
    except Exception as e:
        health_status["checks"]["llm"] = f"failed: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check 2: Are we within acceptable error rates?
    summary = metrics.get_summary()
    if summary.get("success_rate", 100) < 90:
        health_status["checks"]["error_rate"] = "high error rate"
        health_status["status"] = "degraded"
    else:
        health_status["checks"]["error_rate"] = "ok"
    
    # Return appropriate status code
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status


@app.get("/health/simple")
async def simple_health():
    """Simple health check for basic uptime monitoring."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
