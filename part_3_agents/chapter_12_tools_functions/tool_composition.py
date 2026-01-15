# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: tool_composition.py

from langchain_core.tools import Tool
import json

# Tool 1: Fetches data
def fetch_data(source: str) -> str:
    """Fetch data from a source."""
    # Simulated data fetching
    data = {
        "sales": [100, 150, 120, 180, 200],
        "costs": [80, 90, 85, 95, 100]
    }
    return json.dumps(data)

# Tool 2: Analyzes data
def analyze_data(json_data: str) -> str:
    """Analyze data and return insights."""
    try:
        data = json.loads(json_data)
        sales = data.get("sales", [])
        costs = data.get("costs", [])
        
        total_sales = sum(sales)
        total_costs = sum(costs)
        profit = total_sales - total_costs
        margin = (profit / total_sales * 100) if total_sales > 0 else 0
        
        return f"Analysis: Total Sales: ${total_sales}, Total Costs: ${total_costs}, Profit: ${profit}, Margin: {margin:.1f}%"
    except:
        return "Error: Invalid data format for analysis"

# Tool 3: Formats reports
def format_report(analysis: str) -> str:
    """Format analysis into a nice report."""
    if "Error" in analysis:
        return analysis
    
    report = f"""
    📊 BUSINESS REPORT
    ==================
    {analysis}
    
    Status: ✅ Profitable
    Recommendation: Continue current strategy
    """
    return report.strip()

# Create the tool chain
fetch_tool = Tool(name="DataFetcher", func=fetch_data, 
                  description="Fetch business data from a source")
analyze_tool = Tool(name="DataAnalyzer", func=analyze_data,
                    description="Analyze JSON data and return insights")
format_tool = Tool(name="ReportFormatter", func=format_report,
                   description="Format analysis into a professional report")

# These tools naturally work together:
# 1. Fetch data → 2. Analyze it → 3. Format report
# The LLM orchestrates this flow automatically!
