# From: Zero to AI Agent, Chapter 11, Section 11.7
# File: exercise_1_11_7_solution.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from collections import deque

load_dotenv()

class DebugDashboard:
    def __init__(self):
        self.components = {
            "api_key": {"status": "unknown", "last_check": None},
            "llm": {"status": "unknown", "last_check": None, "model": "gpt-3.5-turbo"},
            "memory": {"status": "unknown", "size": 0},
            "chains": {"active": [], "failed": []},
            "prompts": {"loaded": 0, "errors": []}
        }
        
        self.recent_errors = deque(maxlen=10)
        self.performance_metrics = {
            "llm_calls": [],
            "chain_executions": [],
            "memory_operations": []
        }
        
        self.quick_fixes = {
            "api_key_missing": "Add OPENAI_API_KEY to your .env file",
            "import_error": "Run: pip install langchain langchain-openai",
            "rate_limit": "Wait 60 seconds or upgrade your API plan",
            "memory_overflow": "Clear memory or use ConversationSummaryMemory",
            "chain_error": "Check all required input variables are provided"
        }
    
    def check_api_key(self):
        """Check API key status"""
        key = os.getenv("OPENAI_API_KEY")
        if key and key.startswith("sk-"):
            self.components["api_key"]["status"] = "✅ Valid"
        elif key:
            self.components["api_key"]["status"] = "⚠️ Invalid format"
        else:
            self.components["api_key"]["status"] = "❌ Missing"
            self.recent_errors.append({
                "time": datetime.now(),
                "component": "api_key",
                "error": "No API key found",
                "fix": self.quick_fixes["api_key_missing"]
            })
        
        self.components["api_key"]["last_check"] = datetime.now()
    
    def check_llm(self):
        """Check LLM connectivity"""
        try:
            llm = ChatOpenAI(model=self.components["llm"]["model"])
            
            start = time.time()
            response = llm.invoke("Test")
            elapsed = time.time() - start
            
            self.components["llm"]["status"] = f"✅ Working ({elapsed:.2f}s)"
            self.performance_metrics["llm_calls"].append(elapsed)
            
        except Exception as e:
            self.components["llm"]["status"] = f"❌ Failed"
            self.recent_errors.append({
                "time": datetime.now(),
                "component": "llm",
                "error": str(e),
                "fix": self._suggest_fix(str(e))
            })
        
        self.components["llm"]["last_check"] = datetime.now()
    
    def check_memory(self):
        """Check memory status"""
        try:
            memory = ConversationBufferMemory()
            
            # Test save and load
            memory.save_context({"input": "test"}, {"output": "response"})
            history = memory.load_memory_variables({})
            
            self.components["memory"]["status"] = "✅ Working"
            self.components["memory"]["size"] = len(str(history))
            
        except Exception as e:
            self.components["memory"]["status"] = "❌ Failed"
            self.recent_errors.append({
                "time": datetime.now(),
                "component": "memory",
                "error": str(e),
                "fix": "Check memory initialization"
            })
    
    def test_chain(self, chain_name="test"):
        """Test a chain execution"""
        try:
            prompt = ChatPromptTemplate.from_template("Test: {input}")
            llm = ChatOpenAI()
            chain = prompt | llm
            
            start = time.time()
            result = chain.invoke({"input": "test"})
            elapsed = time.time() - start
            
            self.components["chains"]["active"].append(chain_name)
            self.performance_metrics["chain_executions"].append(elapsed)
            
            return True
            
        except Exception as e:
            self.components["chains"]["failed"].append(chain_name)
            self.recent_errors.append({
                "time": datetime.now(),
                "component": f"chain:{chain_name}",
                "error": str(e),
                "fix": self.quick_fixes["chain_error"]
            })
            return False
    
    def _suggest_fix(self, error_msg):
        """Suggest fix based on error"""
        error_lower = error_msg.lower()
        
        if "api" in error_lower and "key" in error_lower:
            return self.quick_fixes["api_key_missing"]
        elif "rate" in error_lower:
            return self.quick_fixes["rate_limit"]
        elif "import" in error_lower:
            return self.quick_fixes["import_error"]
        else:
            return "Check error message and documentation"
    
    def run_diagnostics(self):
        """Run all diagnostic checks"""
        print("🔍 Running diagnostics...")
        self.check_api_key()
        self.check_llm()
        self.check_memory()
        self.test_chain()
    
    def display_dashboard(self):
        """Display the dashboard"""
        print("\n" + "="*60)
        print("🎯 LANGCHAIN DEBUG DASHBOARD")
        print("="*60)
        
        # Component Status
        print("\n📊 Component Status:")
        for name, info in self.components.items():
            status = info.get("status", "unknown")
            print(f"  {name:15} {status}")
        
        # Performance Metrics
        print("\n⚡ Performance Metrics:")
        if self.performance_metrics["llm_calls"]:
            avg_llm = sum(self.performance_metrics["llm_calls"]) / len(self.performance_metrics["llm_calls"])
            print(f"  LLM Avg Response: {avg_llm:.2f}s")
        
        if self.performance_metrics["chain_executions"]:
            avg_chain = sum(self.performance_metrics["chain_executions"]) / len(self.performance_metrics["chain_executions"])
            print(f"  Chain Avg Execution: {avg_chain:.2f}s")
        
        # Recent Errors
        if self.recent_errors:
            print("\n❌ Recent Errors:")
            for error in list(self.recent_errors)[-3:]:  # Show last 3
                print(f"  [{error['time'].strftime('%H:%M:%S')}] {error['component']}")
                print(f"    Error: {error['error'][:50]}...")
                print(f"    Fix: {error['fix']}")
        
        # Quick Actions
        print("\n🔧 Quick Actions:")
        print("  1. Clear Memory: memory.clear()")
        print("  2. Restart LLM: llm = ChatOpenAI()")
        print("  3. Check Env: load_dotenv(override=True)")
        print("  4. Debug Mode: set_debug(True)")
        
        print("\n" + "="*60)

# Run the dashboard
if __name__ == "__main__":
    dashboard = DebugDashboard()
    dashboard.run_diagnostics()
    dashboard.display_dashboard()
