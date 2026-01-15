# From: Zero to AI Agent, Chapter 16, Section 16.7
# File: exercise_3_16_7_solution.py

"""
Exercise 3 Solution: Build a Health Check

Health check system for multi-agent pipelines.

Features:
- Register agents with test inputs
- Check individual agent health
- Check all agents at once
- Generate status report
- Flag unhealthy agents
"""

from typing import Callable
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from datetime import datetime
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("health_check")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


# =============================================================================
# HEALTH CHECKER CLASS
# =============================================================================

class AgentHealthChecker:
    """Checks health of agents in a system."""
    
    def __init__(self):
        self.agents = {}
        self.results = {}
    
    def register(self, name: str, agent_func: Callable, test_input: dict):
        """
        Register an agent for health checking.
        
        Args:
            name: Agent name for reporting
            agent_func: The agent function to test
            test_input: Simple input to test the agent with
        """
        self.agents[name] = {
            "func": agent_func,
            "test_input": test_input
        }
        logger.info(f"Registered agent: {name}")
    
    def check_agent(self, name: str) -> dict:
        """Check health of a single agent."""
        if name not in self.agents:
            return {"status": "unknown", "error": "Agent not registered"}
        
        agent = self.agents[name]
        start = datetime.now()
        
        try:
            result = agent["func"](agent["test_input"])
            duration = (datetime.now() - start).total_seconds()
            
            return {
                "status": "healthy",
                "duration": duration,
                "response_preview": str(result)[:100]
            }
        
        except Exception as e:
            duration = (datetime.now() - start).total_seconds()
            return {
                "status": "unhealthy",
                "duration": duration,
                "error": str(e)
            }
    
    def check_all(self) -> dict:
        """Check health of all registered agents."""
        logger.info("Starting health check for all agents...")
        
        results = {}
        healthy_count = 0
        
        for name in self.agents:
            logger.info(f"Checking {name}...")
            results[name] = self.check_agent(name)
            
            if results[name]["status"] == "healthy":
                healthy_count += 1
        
        self.results = results
        
        return {
            "total": len(self.agents),
            "healthy": healthy_count,
            "unhealthy": len(self.agents) - healthy_count,
            "details": results
        }
    
    def report(self):
        """Print formatted health check report."""
        if not self.results:
            self.check_all()
        
        print("\n" + "=" * 50)
        print("AGENT HEALTH CHECK REPORT")
        print("=" * 50)
        
        for name, result in self.results.items():
            status_icon = "✅" if result["status"] == "healthy" else "❌"
            print(f"\n{status_icon} {name}")
            print(f"   Status: {result['status']}")
            
            if "duration" in result:
                print(f"   Duration: {result['duration']:.2f}s")
            
            if "error" in result:
                print(f"   Error: {result['error']}")
            
            if "response_preview" in result:
                print(f"   Response: {result['response_preview'][:50]}...")
        
        # Summary
        total = len(self.results)
        healthy = sum(1 for r in self.results.values() if r["status"] == "healthy")
        
        print("\n" + "-" * 50)
        print(f"Summary: {healthy}/{total} agents healthy")
        
        if healthy < total:
            print("⚠️  Some agents need attention!")
        else:
            print("✅ All systems operational")
        
        print("=" * 50)
    
    def get_unhealthy_agents(self) -> list[str]:
        """Return list of unhealthy agent names."""
        if not self.results:
            self.check_all()
        
        return [name for name, result in self.results.items() 
                if result["status"] != "healthy"]


# =============================================================================
# SAMPLE AGENTS FOR TESTING
# =============================================================================

def working_planner(state: dict) -> dict:
    """A working agent."""
    response = llm.invoke(f"Create 1 research question about: {state['topic']}")
    return {"questions": [response.content]}


def working_researcher(state: dict) -> dict:
    """Another working agent."""
    response = llm.invoke(f"One interesting fact about: {state['topic']}")
    return {"findings": [response.content]}


def working_writer(state: dict) -> dict:
    """A working writer agent."""
    response = llm.invoke(f"Write one sentence about: {state['topic']}")
    return {"output": response.content}


def broken_agent(state: dict) -> dict:
    """Agent that always fails (for testing)."""
    raise Exception("This agent is intentionally broken!")


def slow_but_working_agent(state: dict) -> dict:
    """Agent that's slow but works."""
    import time
    time.sleep(2)  # Simulate slow processing
    response = llm.invoke(f"Quick fact: {state['topic']}")
    return {"output": response.content}


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    # Create health checker
    health = AgentHealthChecker()
    
    # Register working agents
    health.register(
        "planner", 
        working_planner, 
        {"topic": "artificial intelligence"}
    )
    
    health.register(
        "researcher", 
        working_researcher, 
        {"topic": "machine learning"}
    )
    
    health.register(
        "writer", 
        working_writer, 
        {"topic": "Python programming"}
    )
    
    # Register a broken agent
    health.register(
        "broken_agent", 
        broken_agent, 
        {"topic": "anything"}
    )
    
    # Run health check and print report
    health.check_all()
    health.report()
    
    # Show unhealthy agents
    unhealthy = health.get_unhealthy_agents()
    if unhealthy:
        print(f"\n⚠️  Agents needing attention: {unhealthy}")
