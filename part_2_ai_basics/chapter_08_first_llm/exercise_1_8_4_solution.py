# From: Zero to AI Agent, Chapter 8, Section 8.4
# File: exercise_1_8_4_error_logger.py

import openai
from pathlib import Path
import json
from datetime import datetime

def load_api_key():
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENAI_API_KEY='):
                    return line.split('=')[1].strip()
    return None

class ErrorLogger:
    """Log and analyze API errors"""
    
    def __init__(self, log_file="api_errors.json"):
        self.log_file = log_file
        self.current_session_errors = []
        self.load_historical_errors()
    
    def load_historical_errors(self):
        """Load existing error log"""
        if Path(self.log_file).exists():
            with open(self.log_file, 'r') as f:
                self.historical_errors = json.load(f)
        else:
            self.historical_errors = []
    
    def log_error(self, error, context=""):
        """Log an error with context"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'hour': datetime.now().hour,
            'day_of_week': datetime.now().strftime('%A'),
            'error_type': type(error).__name__,
            'error_message': str(error)[:200],
            'context': context
        }
        
        self.current_session_errors.append(error_entry)
        self.historical_errors.append(error_entry)
        
        # Save immediately
        self.save_log()
        
        return error_entry
    
    def save_log(self):
        """Save error log to file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.historical_errors, f, indent=2)
    
    def generate_report(self):
        """Generate error analysis report"""
        if not self.historical_errors:
            return "No errors logged yet!"
        
        report = []
        report.append("📊 ERROR ANALYSIS REPORT")
        report.append("=" * 50)
        
        # Count by error type
        error_counts = {}
        for error in self.historical_errors:
            error_type = error['error_type']
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        report.append("\n🔍 Error Frequency:")
        for error_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {error_type}: {count} times")
        
        # Find patterns by hour
        hour_counts = {}
        for error in self.historical_errors:
            hour = error.get('hour', 0)
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        if hour_counts:
            peak_hour = max(hour_counts.items(), key=lambda x: x[1])
            report.append(f"\n⏰ Peak Error Hour: {peak_hour[0]}:00 ({peak_hour[1]} errors)")
        
        # Find patterns by day
        day_counts = {}
        for error in self.historical_errors:
            day = error.get('day_of_week', 'Unknown')
            day_counts[day] = day_counts.get(day, 0) + 1
        
        if day_counts:
            busiest_day = max(day_counts.items(), key=lambda x: x[1])
            report.append(f"📅 Most Errors on: {busiest_day[0]} ({busiest_day[1]} errors)")
        
        # Recent errors
        recent = self.historical_errors[-5:]
        report.append("\n📜 Recent Errors:")
        for error in recent:
            time_str = error['timestamp'].split('T')[1][:8]
            report.append(f"  [{time_str}] {error['error_type']}")
        
        # Session summary
        if self.current_session_errors:
            report.append(f"\n📈 This Session: {len(self.current_session_errors)} errors")
        
        # Recommendations
        report.append("\n💡 Recommendations:")
        if 'RateLimitError' in error_counts and error_counts['RateLimitError'] > 5:
            report.append("  • Consider implementing request throttling")
        if 'APITimeoutError' in error_counts:
            report.append("  • Consider implementing retry logic with backoff")
        if len(self.historical_errors) > 50:
            report.append("  • Consider archiving old error logs")
        
        return "\n".join(report)

def make_logged_request(client, messages, logger):
    """Make request with error logging"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content, None
    
    except Exception as e:
        # Log the error
        error_info = logger.log_error(e, f"Message: {messages[-1]['content'][:50]}...")
        return None, error_info

# Setup
api_key = load_api_key()
if not api_key:
    print("❌ No API key found!")
    exit()

client = openai.OpenAI(api_key=api_key)
logger = ErrorLogger()

print("📝 Error Logger Demo")
print("=" * 50)
print("All errors are logged for analysis!")
print("Commands: 'report', 'test_errors', 'quit'")
print("-" * 50)

while True:
    user_input = input("\nYour message: ").strip()
    
    if user_input.lower() == 'quit':
        # Show final report
        print("\n" + logger.generate_report())
        break
    
    elif user_input.lower() == 'report':
        print("\n" + logger.generate_report())
        continue
    
    elif user_input.lower() == 'test_errors':
        # Intentionally trigger various errors
        print("\n🧪 Testing error logging...")
        
        # Test 1: Bad model
        try:
            client.chat.completions.create(
                model="invalid-model",
                messages=[{"role": "user", "content": "Test"}]
            )
        except Exception as e:
            logger.log_error(e, "Invalid model test")
            print(f"  Logged: {type(e).__name__}")
        
        # Test 2: Invalid temperature
        try:
            client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                temperature=10.0
            )
        except Exception as e:
            logger.log_error(e, "Invalid temperature test")
            print(f"  Logged: {type(e).__name__}")
        
        # Test 3: Empty messages
        try:
            client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[]
            )
        except Exception as e:
            logger.log_error(e, "Empty messages test")
            print(f"  Logged: {type(e).__name__}")
        
        print("✅ Test errors logged!")
        continue
    
    # Normal request
    messages = [{"role": "user", "content": user_input}]
    response, error_info = make_logged_request(client, messages, logger)
    
    if response:
        print(f"\n🤖 {response}")
    else:
        print(f"\n❌ Error logged: {error_info['error_type']}")
        print(f"💡 Check 'report' for analysis")

print("\n💾 Error log saved to api_errors.json")
print("👋 Goodbye!")
