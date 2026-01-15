# From: Zero to AI Agent, Chapter 17, Section 17.5
# Save as: exercise_1_17_5_solution.py
# Exercise 1: Configurable Report Generator

from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

class ReportState(TypedDict):
    input_data: str
    title: str
    # Section outputs
    executive_summary: str
    data_analysis: str
    visualizations: str
    recommendations: str
    appendix: str
    # Final
    final_report: str

# Available sections
def generate_executive_summary(state: ReportState) -> dict:
    response = llm.invoke(
        f"Write a brief executive summary (3-4 sentences) for a report about:\n"
        f"{state['input_data'][:500]}"
    )
    return {"executive_summary": response.content}

def generate_data_analysis(state: ReportState) -> dict:
    response = llm.invoke(
        f"Provide data analysis insights for:\n{state['input_data'][:500]}\n\n"
        f"Include: key metrics, trends, and patterns observed."
    )
    return {"data_analysis": response.content}

def generate_visualizations(state: ReportState) -> dict:
    response = llm.invoke(
        f"Describe what visualizations (charts, graphs) would be useful for:\n"
        f"{state['input_data'][:500]}\n\n"
        f"List 2-3 recommended charts with descriptions."
    )
    return {"visualizations": response.content}

def generate_recommendations(state: ReportState) -> dict:
    response = llm.invoke(
        f"Based on this data, provide 3-5 actionable recommendations:\n"
        f"{state['input_data'][:500]}"
    )
    return {"recommendations": response.content}

def generate_appendix(state: ReportState) -> dict:
    response = llm.invoke(
        f"Create a brief appendix noting methodology and data sources for:\n"
        f"{state['input_data'][:300]}"
    )
    return {"appendix": response.content}

def compile_report(state: ReportState) -> dict:
    """Compile all sections into final report."""
    sections = []
    
    sections.append(f"# {state['title']}")
    sections.append("=" * 60)
    
    if state.get("executive_summary"):
        sections.append("\n## Executive Summary")
        sections.append(state["executive_summary"])
    
    # Data analysis is always included
    sections.append("\n## Data Analysis")
    sections.append(state["data_analysis"])
    
    if state.get("visualizations"):
        sections.append("\n## Recommended Visualizations")
        sections.append(state["visualizations"])
    
    if state.get("recommendations"):
        sections.append("\n## Recommendations")
        sections.append(state["recommendations"])
    
    if state.get("appendix"):
        sections.append("\n## Appendix")
        sections.append(state["appendix"])
    
    sections.append("\n" + "=" * 60)
    sections.append("End of Report")
    
    return {"final_report": "\n".join(sections)}

# Section registry
SECTIONS = {
    "summary": generate_executive_summary,
    "analysis": generate_data_analysis,
    "visualizations": generate_visualizations,
    "recommendations": generate_recommendations,
    "appendix": generate_appendix
}

def build_report_generator(config: dict):
    """
    Build report generator from configuration.
    
    Config format:
    {
        "sections": ["summary", "analysis", "recommendations"],
        "title": "Report Title"
    }
    
    Note: "analysis" is always included even if not specified.
    """
    sections = config.get("sections", [])
    
    # Handle empty config gracefully - just include analysis
    if not sections:
        sections = ["analysis"]
    
    # Ensure analysis is always included
    if "analysis" not in sections:
        sections.append("analysis")
    
    # Validate sections
    for section in sections:
        if section not in SECTIONS:
            print(f"Warning: Unknown section '{section}' - skipping")
    
    valid_sections = [s for s in sections if s in SECTIONS]
    
    # Build graph
    graph = StateGraph(ReportState)
    
    # Add nodes for each section
    for section in valid_sections:
        graph.add_node(section, SECTIONS[section])
    
    # Add compile node
    graph.add_node("compile", compile_report)
    
    # Connect all sections from START (parallel)
    for section in valid_sections:
        graph.add_edge(START, section)
    
    # All sections lead to compile
    for section in valid_sections:
        graph.add_edge(section, "compile")
    
    graph.add_edge("compile", END)
    
    return graph.compile()

def test_report_generator():
    sample_data = """
    Q3 2024 Sales Performance Data:
    - Total revenue: $4.2M (up 15% YoY)
    - New customers: 347 (up 23% YoY)
    - Customer retention: 89% (up 3%)
    - Product A sales: $2.1M
    - Product B sales: $1.5M
    - Product C sales: $0.6M
    - Top regions: West (35%), East (30%), Central (25%), South (10%)
    - Average deal size: $12,100
    """
    
    initial_state = {
        "input_data": sample_data,
        "title": "Q3 2024 Sales Report",
        "executive_summary": "",
        "data_analysis": "",
        "visualizations": "",
        "recommendations": "",
        "appendix": "",
        "final_report": ""
    }
    
    # Test 1: Full report
    print("📊 Test 1: Full Report (all sections)")
    print("=" * 60)
    
    full_report = build_report_generator({
        "sections": ["summary", "analysis", "visualizations", "recommendations", "appendix"],
        "title": "Q3 2024 Sales Report"
    })
    result = full_report.invoke(initial_state)
    print(result["final_report"])
    
    # Test 2: Minimal report
    print("\n\n" + "=" * 60)
    print("📊 Test 2: Minimal Report (analysis only)")
    print("=" * 60)
    
    minimal_report = build_report_generator({
        "sections": [],  # Empty = just analysis
        "title": "Quick Analysis"
    })
    initial_state["title"] = "Quick Analysis"
    result = minimal_report.invoke(initial_state)
    print(result["final_report"])
    
    # Test 3: Custom selection
    print("\n\n" + "=" * 60)
    print("📊 Test 3: Custom Selection (summary + recommendations)")
    print("=" * 60)
    
    custom_report = build_report_generator({
        "sections": ["summary", "recommendations"],
        "title": "Executive Brief"
    })
    initial_state["title"] = "Executive Brief"
    result = custom_report.invoke(initial_state)
    print(result["final_report"])

if __name__ == "__main__":
    test_report_generator()
