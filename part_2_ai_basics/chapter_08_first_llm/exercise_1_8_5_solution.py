# From: Zero to AI Agent, Chapter 8, Section 8.5
# File: exercise_1_8_5_solution.py

"""Track conversation topics"""

from collections import Counter
import re

class TopicTracker:
    """Track and analyze conversation topics"""
    
    def __init__(self):
        self.topics = Counter()
        self.topic_keywords = {
            'programming': ['code', 'python', 'function', 'variable', 'loop', 'class'],
            'data': ['data', 'database', 'sql', 'table', 'query', 'analysis'],
            'ai': ['ai', 'machine learning', 'neural', 'model', 'training'],
            'math': ['calculate', 'number', 'equation', 'formula', 'math'],
            'general': []  # Default category
        }
    
    def analyze_message(self, message):
        """Detect topics in a message"""
        message_lower = message.lower()
        detected_topics = []
        
        for topic, keywords in self.topic_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    detected_topics.append(topic)
                    break
        
        if not detected_topics:
            detected_topics.append('general')
        
        # Update counters
        for topic in detected_topics:
            self.topics[topic] += 1
        
        return detected_topics
    
    def get_report(self):
        """Get topic analysis report"""
        if not self.topics:
            return "No topics tracked yet"
        
        total = sum(self.topics.values())
        report = ["📊 Topic Analysis:"]
        
        for topic, count in self.topics.most_common():
            percentage = (count / total) * 100
            bar = '█' * int(percentage / 10)
            report.append(f"  {topic:12} {bar} {percentage:.1f}%")
        
        return "\n".join(report)
    
    def get_dominant_topic(self):
        """Get the most discussed topic"""
        if not self.topics:
            return "general"
        return self.topics.most_common(1)[0][0]
