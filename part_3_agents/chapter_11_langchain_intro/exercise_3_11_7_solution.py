# From: Zero to AI Agent, Chapter 11, Section 11.7
# File: exercise_3_11_7_solution.py

import time
import json
from typing import Callable, Dict
from datetime import datetime

class ErrorRecoverySystem:
    def __init__(self):
        self.error_log = []
        self.recovery_strategies = {
            "api_key": self.recover_api_key,
            "rate_limit": self.recover_rate_limit,
            "timeout": self.recover_timeout,
            "model_error": self.recover_model_error,
            "memory_error": self.recover_memory_error
        }
        self.max_retries = 3
        self.backoff_factor = 2
    
    def detect_error_type(self, error: Exception) -> str:
        """Detect error type from exception"""
        error_str = str(error).lower()
        
        if "api" in error_str and "key" in error_str:
            return "api_key"
        elif "rate limit" in error_str:
            return "rate_limit"
        elif "timeout" in error_str:
            return "timeout"
        elif "model" in error_str:
            return "model_error"
        elif "memory" in error_str:
            return "memory_error"
        else:
            return "unknown"
    
    def recover_api_key(self, context: Dict) -> Callable:
        """Recover from API key errors"""
        print("🔧 Recovering from API key error...")
        from dotenv import load_dotenv
        import os
        
        # Try reloading environment
        load_dotenv(override=True)
        
        # Try alternative API key
        if not os.getenv("OPENAI_API_KEY"):
            # Try fallback to free model
            from langchain_community.llms import Ollama
            print("✅ Falling back to local model")
            return lambda: Ollama(model="llama2")
        
        from langchain_openai import ChatOpenAI
        return lambda: ChatOpenAI()
    
    def recover_rate_limit(self, context: Dict) -> Callable:
        """Recover from rate limit errors"""
        print("🔧 Recovering from rate limit...")
        wait_time = min(60 * (context.get("attempt", 1)), 300)
        print(f"⏳ Waiting {wait_time}s...")
        time.sleep(wait_time)
        
        # Return original function
        return context.get("original_func")
    
    def recover_timeout(self, context: Dict) -> Callable:
        """Recover from timeout errors"""
        print("🔧 Recovering from timeout...")
        
        # Return a simpler version
        def simple_version(*args, **kwargs):
            # Reduce complexity
            if "max_tokens" in kwargs:
                kwargs["max_tokens"] = min(kwargs["max_tokens"], 100)
            if "temperature" in kwargs:
                kwargs["temperature"] = 0
            return context["original_func"](*args, **kwargs)
        
        return simple_version
    
    def recover_model_error(self, context: Dict) -> Callable:
        """Recover from model errors"""
        print("🔧 Recovering from model error...")
        
        # Try fallback model
        from langchain_openai import ChatOpenAI
        
        def fallback_model(*args, **kwargs):
            # Use simpler model
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            return llm.invoke(*args, **kwargs)
        
        return fallback_model
    
    def recover_memory_error(self, context: Dict) -> Callable:
        """Recover from memory errors"""
        print("🔧 Recovering from memory error...")
        
        # Return function with cleared memory
        def cleared_memory(*args, **kwargs):
            if "memory" in kwargs:
                kwargs["memory"].clear()
            return context["original_func"](*args, **kwargs)
        
        return cleared_memory
    
    def exponential_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay"""
        return min(self.backoff_factor ** attempt, 60)
    
    def execute_with_recovery(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with automatic error recovery"""
        
        attempt = 0
        last_error = None
        
        while attempt < self.max_retries:
            attempt += 1
            
            try:
                print(f"\n🔄 Attempt {attempt}/{self.max_retries}")
                result = func(*args, **kwargs)
                
                if attempt > 1:
                    print(f"✅ Succeeded after recovery")
                    self.log_recovery(func.__name__, attempt, "success", None)
                
                return result
                
            except Exception as e:
                last_error = e
                error_type = self.detect_error_type(e)
                
                print(f"❌ Error: {str(e)[:100]}")
                print(f"🔍 Error type: {error_type}")
                
                self.log_recovery(func.__name__, attempt, "error", error_type)
                
                if error_type in self.recovery_strategies:
                    context = {
                        "error": e,
                        "attempt": attempt,
                        "original_func": func,
                        "args": args,
                        "kwargs": kwargs
                    }
                    
                    # Apply recovery strategy
                    recovered_func = self.recovery_strategies[error_type](context)
                    
                    if recovered_func:
                        func = recovered_func
                        print(f"✅ Recovery strategy applied")
                    else:
                        print(f"❌ Recovery failed")
                
                if attempt < self.max_retries:
                    delay = self.exponential_backoff(attempt)
                    print(f"⏳ Waiting {delay:.1f}s before retry...")
                    time.sleep(delay)
        
        # All attempts failed
        self.log_recovery(func.__name__, attempt, "failed", str(last_error))
        
        # Try final fallback
        print("\n🚨 Attempting final fallback...")
        return self.final_fallback(*args, **kwargs)
    
    def final_fallback(self, *args, **kwargs):
        """Final fallback when all else fails"""
        return {
            "status": "failed",
            "message": "All recovery attempts failed. Please check logs.",
            "fallback": True
        }
    
    def log_recovery(self, function: str, attempt: int, status: str, error_type: str):
        """Log recovery attempts"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "function": function,
            "attempt": attempt,
            "status": status,
            "error_type": error_type
        }
        
        self.error_log.append(log_entry)
    
    def export_logs(self, filename="recovery_log.json"):
        """Export recovery logs"""
        with open(filename, 'w') as f:
            json.dump(self.error_log, f, indent=2)
        print(f"📁 Recovery log saved to {filename}")
    
    def show_statistics(self):
        """Show recovery statistics"""
        if not self.error_log:
            print("No recovery attempts yet")
            return
        
        total = len(self.error_log)
        successful = sum(1 for log in self.error_log if log["status"] == "success")
        failed = sum(1 for log in self.error_log if log["status"] == "failed")
        
        print("\n📊 Recovery Statistics:")
        print(f"  Total attempts: {total}")
        print(f"  Successful recoveries: {successful}")
        print(f"  Failed recoveries: {failed}")
        print(f"  Success rate: {(successful/total*100):.1f}%")
        
        # Error type breakdown
        error_types = {}
        for log in self.error_log:
            if log["error_type"]:
                error_types[log["error_type"]] = error_types.get(log["error_type"], 0) + 1
        
        if error_types:
            print("\n  Error types:")
            for error_type, count in error_types.items():
                print(f"    {error_type}: {count}")

# Test functions
def test_function_that_fails():
    """Function that might fail"""
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise Exception("Random failure for testing")
    return "Success!"

# Demo
if __name__ == "__main__":
    recovery = ErrorRecoverySystem()
    
    print("🛡️ Error Recovery System Demo")
    print("="*60)
    
    # Test recovery
    result = recovery.execute_with_recovery(test_function_that_fails)
    print(f"\nFinal result: {result}")
    
    # Show statistics
    recovery.show_statistics()
    
    # Export logs
    recovery.export_logs()
