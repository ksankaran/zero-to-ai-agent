# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: ultimate_modular_bot.py

"""Combine all modules into one powerful chatbot"""

from api_helper import get_client
from topic_tracker import TopicTracker
from response_timer import ResponseTimer
from mood_detector import MoodDetector
from memory_manager import MemoryManager

class UltimateBot:
    """Chatbot with all features combined"""
    
    def __init__(self, client):
        self.client = client
        self.messages = []
        
        # Initialize all modules
        self.topic_tracker = TopicTracker()
        self.timer = ResponseTimer()
        self.mood_detector = MoodDetector()
        self.memory = MemoryManager(max_messages=15)
    
    def chat(self, user_message):
        """Chat with all features"""
        # Track topics
        topics = self.topic_tracker.analyze_message(user_message)
        
        # Detect mood
        mood = self.mood_detector.detect_mood(user_message)
        
        # Build context with memory management
        self.messages.append({"role": "user", "content": user_message})
        context = self.memory.get_context(self.messages)
        
        # Add mood-aware system prompt
        style = self.mood_detector.get_response_style()
        context.insert(0, {
            "role": "system",
            "content": f"You are a helpful assistant. Be {style}."
        })
        
        # Time the response
        start = self.timer.start()
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context
        )
        
        elapsed = self.timer.end(start)
        
        # Extract response
        ai_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": ai_message})
        
        # Track AI response topics
        self.topic_tracker.analyze_message(ai_message)
        
        return {
            'message': ai_message,
            'mood': mood,
            'topics': topics,
            'response_time': elapsed,
            'context_truncated': self.memory.should_truncate(self.messages)
        }
    
    def get_full_stats(self):
        """Get combined statistics"""
        return {
            'topics': self.topic_tracker.get_report(),
            'timing': self.timer.format_stats(),
            'mood': self.mood_detector.current_mood,
            'messages': len(self.messages)
        }

def main():
    client = get_client()
    bot = UltimateBot(client)
    
    print("🚀 Ultimate Modular Chatbot")
    print("All features combined in one bot!")
    print("Commands: 'stats', 'quit'")
    print("-" * 40)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            stats = bot.get_full_stats()
            print("\n📊 Final Statistics:")
            for key, value in stats.items():
                print(f"\n{value}")
            break
        
        elif user_input.lower() == 'stats':
            stats = bot.get_full_stats()
            for key, value in stats.items():
                print(f"\n{value}")
            continue
        
        # Get response with all features
        result = bot.chat(user_input)
        
        # Display response
        print(f"Bot: {result['message']}")
        
        # Show metadata
        metadata = []
        if result['mood'] != 'neutral':
            metadata.append(f"mood:{result['mood']}")
        if result['topics'] != ['general']:
            metadata.append(f"topics:{','.join(result['topics'])}")
        metadata.append(f"time:{result['response_time']:.2f}s")
        
        print(f"[{' | '.join(metadata)}]")

if __name__ == "__main__":
    main()
