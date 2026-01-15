# From: Zero to AI Agent, Chapter 17, Section 17.3
# Save as: exercise_3_17_3_solution.py
# Exercise 3: Competitive Analysis System

import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

class MainState(TypedDict):
    company: str
    company_context: str
    competitors: list[str]
    analyses: Annotated[list[dict], operator.add]
    comparative_matrix: str
    recommendations: str

class CompetitorState(TypedDict):
    company: str
    company_context: str
    competitor: str

def distribute_competitors(state: MainState) -> list[Send]:
    """Send each competitor for parallel analysis."""
    return [
        Send("analyze_competitor", {
            "company": state["company"],
            "company_context": state["company_context"],
            "competitor": competitor
        })
        for competitor in state["competitors"]
    ]

def analyze_competitor(state: CompetitorState) -> dict:
    """Analyze a single competitor."""
    
    response = llm.invoke(
        f"You are a competitive intelligence analyst.\n\n"
        f"Your company: {state['company']}\n"
        f"Context: {state['company_context']}\n"
        f"Competitor to analyze: {state['competitor']}\n\n"
        f"Provide a structured analysis:\n"
        f"1. STRENGTHS (3 key strengths)\n"
        f"2. WEAKNESSES (3 key weaknesses)\n"
        f"3. MARKET POSITION (Brief assessment)\n"
        f"4. THREAT LEVEL (1-10 scale)\n"
        f"5. KEY DIFFERENTIATOR (What makes them unique)\n\n"
        f"Format as:\n"
        f"STRENGTHS: strength1; strength2; strength3\n"
        f"WEAKNESSES: weakness1; weakness2; weakness3\n"
        f"MARKET POSITION: [assessment]\n"
        f"THREAT LEVEL: [1-10]\n"
        f"DIFFERENTIATOR: [key differentiator]"
    )
    
    content = response.content
    
    # Parse structured response
    strengths = []
    weaknesses = []
    market_position = ""
    threat_level = 5
    differentiator = ""
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('STRENGTHS:'):
            strengths = [s.strip() for s in line[10:].split(';') if s.strip()]
        elif line.startswith('WEAKNESSES:'):
            weaknesses = [w.strip() for w in line[11:].split(';') if w.strip()]
        elif line.startswith('MARKET POSITION:'):
            market_position = line[16:].strip()
        elif line.startswith('THREAT LEVEL:'):
            try:
                threat_level = int(''.join(filter(str.isdigit, line[13:])))
                threat_level = max(1, min(10, threat_level))
            except:
                threat_level = 5
        elif line.startswith('DIFFERENTIATOR:'):
            differentiator = line[15:].strip()
    
    print(f"🔍 Analyzed: {state['competitor']} (Threat: {threat_level}/10)")
    
    return {"analyses": [{
        "competitor": state["competitor"],
        "strengths": strengths,
        "weaknesses": weaknesses,
        "market_position": market_position,
        "threat_level": threat_level,
        "differentiator": differentiator,
        "raw_analysis": content
    }]}

def build_comparative_matrix(state: MainState) -> dict:
    """Build a comparative matrix from all analyses."""
    
    analyses = state["analyses"]
    
    # Sort by threat level (highest first)
    sorted_analyses = sorted(analyses, key=lambda x: x["threat_level"], reverse=True)
    
    matrix_parts = []
    matrix_parts.append("=" * 70)
    matrix_parts.append(f"COMPETITIVE ANALYSIS: {state['company']}")
    matrix_parts.append("=" * 70)
    
    # Summary table
    matrix_parts.append("\n📊 COMPETITOR RANKING (by threat level):\n")
    matrix_parts.append(f"{'Rank':<5} {'Competitor':<20} {'Threat':<8} {'Key Strength':<30}")
    matrix_parts.append("-" * 70)
    
    for i, analysis in enumerate(sorted_analyses, 1):
        top_strength = analysis["strengths"][0] if analysis["strengths"] else "N/A"
        matrix_parts.append(
            f"{i:<5} {analysis['competitor']:<20} {analysis['threat_level']}/10    {top_strength[:28]:<30}"
        )
    
    # Detailed comparison
    matrix_parts.append("\n\n📋 DETAILED COMPARISON:\n")
    
    for analysis in sorted_analyses:
        matrix_parts.append(f"\n{'─' * 50}")
        matrix_parts.append(f"🏢 {analysis['competitor']} (Threat Level: {analysis['threat_level']}/10)")
        matrix_parts.append(f"{'─' * 50}")
        
        matrix_parts.append("\n   💪 Strengths:")
        for s in analysis["strengths"][:3]:
            matrix_parts.append(f"      • {s}")
        
        matrix_parts.append("\n   ⚠️ Weaknesses:")
        for w in analysis["weaknesses"][:3]:
            matrix_parts.append(f"      • {w}")
        
        matrix_parts.append(f"\n   📍 Market Position: {analysis['market_position']}")
        matrix_parts.append(f"   ⭐ Differentiator: {analysis['differentiator']}")
    
    return {"comparative_matrix": "\n".join(matrix_parts)}

def generate_recommendations(state: MainState) -> dict:
    """Generate strategic recommendations based on analysis."""
    
    analyses = state["analyses"]
    
    # Find top threats
    top_threats = sorted(analyses, key=lambda x: x["threat_level"], reverse=True)[:3]
    
    # Aggregate competitor weaknesses (potential opportunities)
    all_weaknesses = []
    for a in analyses:
        all_weaknesses.extend(a["weaknesses"])
    
    # Build context for LLM
    threat_summary = "\n".join([
        f"- {a['competitor']}: Threat {a['threat_level']}/10, Differentiator: {a['differentiator']}"
        for a in top_threats
    ])
    
    response = llm.invoke(
        f"Based on competitive analysis for {state['company']}:\n\n"
        f"Company Context: {state['company_context']}\n\n"
        f"Top Competitive Threats:\n{threat_summary}\n\n"
        f"Common Competitor Weaknesses:\n{', '.join(all_weaknesses[:6])}\n\n"
        f"Provide 5 strategic recommendations to improve competitive position. "
        f"For each recommendation, explain:\n"
        f"1. The action to take\n"
        f"2. Which competitor threat it addresses\n"
        f"3. Expected impact (High/Medium/Low)\n\n"
        f"Be specific and actionable."
    )
    
    recommendations = (
        "\n" + "=" * 70 + "\n"
        "🎯 STRATEGIC RECOMMENDATIONS\n"
        + "=" * 70 + "\n\n"
        + response.content
    )
    
    return {"recommendations": recommendations}

def build_competitive_analysis_graph():
    workflow = StateGraph(MainState)
    
    workflow.add_node("distribute", lambda state: {})
    workflow.add_node("analyze_competitor", analyze_competitor)
    workflow.add_node("build_matrix", build_comparative_matrix)
    workflow.add_node("recommend", generate_recommendations)
    
    workflow.add_edge(START, "distribute")
    
    workflow.add_conditional_edges(
        "distribute",
        distribute_competitors,
        ["analyze_competitor"]
    )
    
    workflow.add_edge("analyze_competitor", "build_matrix")
    workflow.add_edge("build_matrix", "recommend")
    workflow.add_edge("recommend", END)
    
    return workflow.compile()

def run_competitive_analysis():
    graph = build_competitive_analysis_graph()
    
    # Example: Tech company analyzing competitors
    initial_state = {
        "company": "TechCorp",
        "company_context": "B2B SaaS company providing project management tools. "
                          "Founded 5 years ago, 500 employees, $50M ARR. "
                          "Strong in mid-market segment, looking to move upmarket.",
        "competitors": [
            "Asana",
            "Monday.com",
            "Jira",
            "Notion",
            "ClickUp"
        ],
        "analyses": [],
        "comparative_matrix": "",
        "recommendations": ""
    }
    
    print(f"🏢 Competitive Analysis for: {initial_state['company']}")
    print(f"📋 Analyzing {len(initial_state['competitors'])} competitors in parallel...\n")
    print("=" * 70 + "\n")
    
    result = graph.invoke(initial_state)
    
    # Display results
    print(result["comparative_matrix"])
    print(result["recommendations"])

if __name__ == "__main__":
    run_competitive_analysis()
