# From: Zero to AI Agent, Chapter 12, Section 12.6
# File: tool_logging.py

from langchain_core.tools import Tool
import logging
from datetime import datetime
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ToolMonitor:
    """Simple tool monitoring system."""
    
    def __init__(self):
        self.stats = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "errors": []
        }
    
    def log_call(self, tool_name: str, input_data: str, result: str):
        """Log a tool call."""
        self.stats["total_calls"] += 1
        
        if result.startswith("Error"):
            self.stats["failed_calls"] += 1
            self.stats["errors"].append({
                "tool": tool_name,
                "input": input_data,
                "error": result,
                "time": datetime.now().isoformat()
            })
            logging.error(f"Tool {tool_name} failed: {result}")
        else:
            self.stats["successful_calls"] += 1
            logging.info(f"Tool {tool_name} succeeded")
    
    def get_report(self):
        """Get monitoring report."""
        success_rate = (
            self.stats["successful_calls"] / self.stats["total_calls"] * 100
            if self.stats["total_calls"] > 0 else 0
        )
        
        return f"""
Tool Monitoring Report
=====================
Total Calls: {self.stats["total_calls"]}
Successful: {self.stats["successful_calls"]}
Failed: {self.stats["failed_calls"]}
Success Rate: {success_rate:.1f}%

Recent Errors: {len(self.stats["errors"])}
"""

# Create a monitored tool
monitor = ToolMonitor()

def monitored_calculator(expression: str) -> str:
    """Calculator with monitoring."""
    tool_name = "Calculator"
    
    try:
        result = str(eval(expression))
        monitor.log_call(tool_name, expression, result)
        return result
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        monitor.log_call(tool_name, expression, error_msg)
        return error_msg

# Test monitoring
print("TOOL MONITORING EXAMPLE")
print("=" * 50)

tool = Tool(
    name="MonitoredCalc",
    func=monitored_calculator,
    description="Calculator with monitoring"
)

# Run various calculations
test_cases = [
    "10 + 5",     # Success
    "20 * 3",     # Success  
    "100 / 0",    # Error
    "50 - 30",    # Success
    "invalid",    # Error
]

for expr in test_cases:
    result = tool.func(expr)
    print(f"{expr} = {result}")

# Show monitoring report
print("\n" + monitor.get_report())
