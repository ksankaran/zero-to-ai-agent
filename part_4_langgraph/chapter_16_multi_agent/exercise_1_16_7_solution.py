# From: Zero to AI Agent, Chapter 16, Section 16.7
# File: exercise_1_16_7_solution.py

"""
Exercise 1 Solution: Add Monitoring

Research team with logging and metrics tracking.
Demonstrates:
- Structured logging for each agent
- Metrics collection (calls, duration, errors)
- Final metrics report
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from datetime import datetime
import logging

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("research_team")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


# =============================================================================
# METRICS COLLECTOR
# =============================================================================

class MetricsCollector:
    """Collects metrics for all agents."""
    
    def __init__(self):
        self.data = {}
    
    def record(self, agent: str, duration: float, success: bool):
        if agent not in self.data:
            self.data[agent] = {"calls": 0, "durations": [], "errors": 0}
        
        self.data[agent]["calls"] += 1
        self.data[agent]["durations"].append(duration)
        if not success:
            self.data[agent]["errors"] += 1
    
    def report(self):
        print("\n" + "=" * 50)
        print("AGENT METRICS REPORT")
        print("=" * 50)
        
        total_time = 0
        for agent, stats in self.data.items():
            avg = sum(stats["durations"]) / len(stats["durations"])
            total_time += sum(stats["durations"])
            error_rate = stats["errors"] / stats["calls"] * 100
            
            print(f"\n{agent}:")
            print(f"  Calls: {stats['calls']}")
            print(f"  Avg Duration: {avg:.2f}s")
            print(f"  Error Rate: {error_rate:.1f}%")
        
        print(f"\nTotal Pipeline Time: {total_time:.2f}s")
        print("=" * 50)


# Global metrics collector
metrics = MetricsCollector()


# =============================================================================
# STATE
# =============================================================================

class ResearchState(TypedDict):
    topic: str
    questions: list[str]
    findings: list[str]
    insights: str
    report: str


# =============================================================================
# AGENTS WITH LOGGING
# =============================================================================

def planner(state: ResearchState) -> dict:
    agent_name = "planner"
    start = datetime.now()
    logger.info(f"[{agent_name}] Starting - topic: {state['topic'][:30]}...")
    
    try:
        prompt = f"Create 3 research questions for: {state['topic']}"
        response = llm.invoke(prompt)
        questions = [line.strip()[3:] for line in response.content.split('\n') 
                     if line.strip() and line.strip()[0].isdigit()][:3]
        
        if not questions:
            questions = [f"What is {state['topic']}?",
                        f"Why is {state['topic']} important?",
                        f"How does {state['topic']} work?"]
        
        duration = (datetime.now() - start).total_seconds()
        metrics.record(agent_name, duration, True)
        logger.info(f"[{agent_name}] Completed in {duration:.2f}s - {len(questions)} questions")
        
        return {"questions": questions}
    
    except Exception as e:
        duration = (datetime.now() - start).total_seconds()
        metrics.record(agent_name, duration, False)
        logger.error(f"[{agent_name}] Failed: {e}")
        raise


def researcher(state: ResearchState) -> dict:
    agent_name = "researcher"
    start = datetime.now()
    logger.info(f"[{agent_name}] Starting - {len(state['questions'])} questions")
    
    try:
        findings = []
        for i, q in enumerate(state['questions'], 1):
            response = llm.invoke(f"Answer briefly (2-3 sentences): {q}")
            findings.append(f"Q{i}: {q}\nA: {response.content}")
            logger.info(f"[{agent_name}] Question {i} complete")
        
        duration = (datetime.now() - start).total_seconds()
        metrics.record(agent_name, duration, True)
        logger.info(f"[{agent_name}] Completed in {duration:.2f}s")
        
        return {"findings": findings}
    
    except Exception as e:
        duration = (datetime.now() - start).total_seconds()
        metrics.record(agent_name, duration, False)
        logger.error(f"[{agent_name}] Failed: {e}")
        raise


def analyst(state: ResearchState) -> dict:
    agent_name = "analyst"
    start = datetime.now()
    logger.info(f"[{agent_name}] Starting - analyzing {len(state['findings'])} findings")
    
    try:
        findings_text = "\n\n".join(state['findings'])
        prompt = f"Give 3 key insights from:\n{findings_text}"
        response = llm.invoke(prompt)
        
        duration = (datetime.now() - start).total_seconds()
        metrics.record(agent_name, duration, True)
        logger.info(f"[{agent_name}] Completed in {duration:.2f}s")
        
        return {"insights": response.content}
    
    except Exception as e:
        duration = (datetime.now() - start).total_seconds()
        metrics.record(agent_name, duration, False)
        logger.error(f"[{agent_name}] Failed: {e}")
        raise


def writer(state: ResearchState) -> dict:
    agent_name = "writer"
    start = datetime.now()
    logger.info(f"[{agent_name}] Starting - writing report")
    
    try:
        prompt = f"""Write a brief research report on: {state['topic']}
        
KEY INSIGHTS:
{state['insights']}

Include an introduction, main findings, and conclusion."""
        response = llm.invoke(prompt)
        
        duration = (datetime.now() - start).total_seconds()
        metrics.record(agent_name, duration, True)
        logger.info(f"[{agent_name}] Completed in {duration:.2f}s")
        
        return {"report": response.content}
    
    except Exception as e:
        duration = (datetime.now() - start).total_seconds()
        metrics.record(agent_name, duration, False)
        logger.error(f"[{agent_name}] Failed: {e}")
        raise


# =============================================================================
# BUILD WORKFLOW
# =============================================================================

workflow = StateGraph(ResearchState)

workflow.add_node("planner", planner)
workflow.add_node("researcher", researcher)
workflow.add_node("analyst", analyst)
workflow.add_node("writer", writer)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

research_team = workflow.compile()


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    logger.info("Starting research pipeline")
    
    result = research_team.invoke({
        "topic": "Benefits of regular exercise",
        "questions": [],
        "findings": [],
        "insights": "",
        "report": ""
    })
    
    # Print metrics report
    metrics.report()
    
    print("\n" + "=" * 50)
    print("FINAL REPORT")
    print("=" * 50)
    print(result["report"])
