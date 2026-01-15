# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: exercise_2_8_6_solution.py

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

class SmartOrganizer:
    """Intelligently organize conversation history"""
    
    def __init__(self, storage_dir="organized_conversations"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.by_topic = self.storage_dir / "by_topic"
        self.by_date = self.storage_dir / "by_date"
        self.summaries = self.storage_dir / "summaries"
        
        for dir in [self.by_topic, self.by_date, self.summaries]:
            dir.mkdir(exist_ok=True)
    
    def detect_topic(self, messages):
        """Detect the main topic of a conversation"""
        
        # Keywords for different topics
        topic_keywords = {
            'programming': ['code', 'python', 'function', 'variable', 'programming', 'debug', 'error'],
            'learning': ['learn', 'teach', 'explain', 'understand', 'what is', 'how to'],
            'creative': ['story', 'write', 'creative', 'imagine', 'design', 'create'],
            'data': ['data', 'analysis', 'database', 'sql', 'pandas', 'excel'],
            'ai': ['ai', 'machine learning', 'neural', 'model', 'training', 'artificial'],
            'general': []  # Default category
        }
        
        # Count keyword matches
        topic_scores = defaultdict(int)
        
        for msg in messages:
            if msg.get('role') == 'user':
                content_lower = msg.get('content', '').lower()
                for topic, keywords in topic_keywords.items():
                    for keyword in keywords:
                        if keyword in content_lower:
                            topic_scores[topic] += 1
        
        # Return highest scoring topic
        if topic_scores:
            return max(topic_scores, key=topic_scores.get)
        return 'general'
    
    def suggest_title(self, messages):
        """Suggest a title based on conversation content"""
        
        # Look at first user message for context
        for msg in messages:
            if msg.get('role') == 'user':
                first_question = msg.get('content', '')[:50]
                
                # Clean up for title
                title = first_question.replace('?', '')
                title = title.replace('\n', ' ')
                
                # Shorten if needed
                if len(title) > 30:
                    title = title[:27] + "..."
                
                return title
        
        return f"Conversation {datetime.now().strftime('%H:%M')}"
    
    def organize_by_topic(self, messages, filename=None):
        """Save conversation organized by topic"""
        
        topic = self.detect_topic(messages)
        topic_dir = self.by_topic / topic
        topic_dir.mkdir(exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conv_{topic}_{timestamp}.json"
        
        filepath = topic_dir / filename
        
        data = {
            'topic': topic,
            'title': self.suggest_title(messages),
            'saved_at': datetime.now().isoformat(),
            'message_count': len(messages),
            'messages': messages
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📁 Organized in topic: {topic}")
        print(f"💾 Saved as: {data['title']}")
        return filepath
    
    def organize_by_date(self, messages):
        """Save conversation organized by date"""
        
        today = datetime.now()
        year = today.strftime("%Y")
        month = today.strftime("%m-%B")
        day = today.strftime("%d")
        
        date_dir = self.by_date / year / month / day
        date_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = today.strftime("%H%M%S")
        filename = f"conv_{timestamp}.json"
        filepath = date_dir / filename
        
        data = {
            'date': today.isoformat(),
            'title': self.suggest_title(messages),
            'messages': messages
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📅 Organized by date: {year}/{month}/{day}")
        return filepath
    
    def create_daily_summary(self):
        """Create a summary of today's conversations"""
        
        today = datetime.now()
        today_str = today.strftime("%Y/%m-%B/%d")
        today_path = self.by_date / today_str
        
        if not today_path.exists():
            print("No conversations today yet!")
            return None
        
        summary = {
            'date': today.strftime("%Y-%m-%d"),
            'conversations': [],
            'total_messages': 0,
            'topics': defaultdict(int)
        }
        
        # Analyze all conversations from today
        for conv_file in today_path.glob("conv_*.json"):
            with open(conv_file, 'r') as f:
                data = json.load(f)
            
            # Detect topic for summary
            topic = self.detect_topic(data['messages'])
            
            summary['conversations'].append({
                'title': data.get('title', 'Untitled'),
                'time': conv_file.stem.split('_')[1],
                'messages': len(data['messages']),
                'topic': topic
            })
            
            summary['total_messages'] += len(data['messages'])
            summary['topics'][topic] += 1
        
        # Convert defaultdict to regular dict for JSON
        summary['topics'] = dict(summary['topics'])
        
        # Save summary
        summary_file = self.summaries / f"daily_{today.strftime('%Y%m%d')}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📊 Daily Summary for {today.strftime('%B %d, %Y')}:")
        print(f"  Conversations: {len(summary['conversations'])}")
        print(f"  Total messages: {summary['total_messages']}")
        print(f"  Topics: {summary['topics']}")
        
        return summary_file
    
    def group_related_conversations(self):
        """Find and group related conversations"""
        
        groups = defaultdict(list)
        
        # Scan all topic directories
        for topic_dir in self.by_topic.iterdir():
            if topic_dir.is_dir():
                topic = topic_dir.name
                
                # Collect all conversations for this topic
                for conv_file in topic_dir.glob("*.json"):
                    with open(conv_file, 'r') as f:
                        data = json.load(f)
                    
                    groups[topic].append({
                        'file': conv_file.name,
                        'title': data.get('title', 'Untitled'),
                        'date': data.get('saved_at', 'Unknown'),
                        'messages': data.get('message_count', 0)
                    })
        
        # Display groups
        print("\n🔗 Related Conversation Groups:")
        for topic, convs in groups.items():
            print(f"\n📌 {topic.upper()} ({len(convs)} conversations)")
            for conv in convs[-3:]:  # Show last 3
                print(f"  • {conv['title']}")
                print(f"    {conv['messages']} messages - {conv['date'][:10]}")
        
        return groups

# Demo usage
if __name__ == "__main__":
    organizer = SmartOrganizer()
    
    print("🧠 Smart Organizer Demo")
    print("=" * 50)
    
    # Sample conversations with different topics
    sample_conversations = [
        [
            {"role": "user", "content": "How do I write a Python function?"},
            {"role": "assistant", "content": "Here's how to write a Python function..."},
            {"role": "user", "content": "Can you show me an example with parameters?"},
            {"role": "assistant", "content": "Sure! Here's an example..."}
        ],
        [
            {"role": "user", "content": "Tell me a creative story"},
            {"role": "assistant", "content": "Once upon a time..."},
            {"role": "user", "content": "Make it more exciting!"},
            {"role": "assistant", "content": "Suddenly, a dragon appeared..."}
        ],
        [
            {"role": "user", "content": "Explain machine learning"},
            {"role": "assistant", "content": "Machine learning is a type of AI..."},
            {"role": "user", "content": "What about neural networks?"},
            {"role": "assistant", "content": "Neural networks are inspired by the brain..."}
        ]
    ]
    
    # Organize each conversation
    for conv in sample_conversations:
        print("\n" + "-" * 40)
        organizer.organize_by_topic(conv)
        organizer.organize_by_date(conv)
    
    # Create daily summary
    print("\n" + "=" * 50)
    organizer.create_daily_summary()
    
    # Show grouped conversations
    print("\n" + "=" * 50)
    organizer.group_related_conversations()
