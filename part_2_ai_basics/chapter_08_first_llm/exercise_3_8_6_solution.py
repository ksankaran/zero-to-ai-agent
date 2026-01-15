# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: exercise_3_8_6_solution.py

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import statistics

class HistoryAnalytics:
    """Analyze conversation history for insights"""
    
    def __init__(self, storage_dir="conversations"):
        self.storage_dir = Path(storage_dir)
        self.conversations = []
        self.load_all_conversations()
    
    def load_all_conversations(self):
        """Load all conversation files for analysis"""
        
        for conv_file in self.storage_dir.rglob("*.json"):
            try:
                with open(conv_file, 'r') as f:
                    data = json.load(f)
                    self.conversations.append(data)
            except:
                continue
        
        print(f"📊 Loaded {len(self.conversations)} conversations for analysis")
    
    def analyze_common_topics(self):
        """Find the most common topics discussed"""
        
        # Words that indicate topics (excluding common words)
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
                     'in', 'with', 'to', 'for', 'of', 'as', 'by', 'that', 'this',
                     'it', 'from', 'what', 'how', 'why', 'when', 'where', 'who',
                     'can', 'could', 'would', 'should', 'will', 'do', 'does', 'did',
                     'have', 'has', 'had', 'be', 'been', 'being', 'was', 'were', 'are'}
        
        word_counter = Counter()
        
        for conv in self.conversations:
            messages = conv.get('messages', [])
            for msg in messages:
                if msg.get('role') == 'user':
                    # Extract meaningful words
                    words = msg.get('content', '').lower().split()
                    meaningful_words = [w.strip('.,!?;:') for w in words 
                                       if len(w) > 3 and w not in stop_words]
                    word_counter.update(meaningful_words)
        
        # Get top topics
        top_topics = word_counter.most_common(15)
        
        print("\n🏷️ Most Common Topics:")
        for word, count in top_topics:
            bar = '█' * min(count, 20)
            print(f"  {word:15} {bar} ({count})")
        
        return top_topics
    
    def analyze_conversation_lengths(self):
        """Analyze conversation length patterns"""
        
        lengths = []
        for conv in self.conversations:
            message_count = conv.get('message_count', len(conv.get('messages', [])))
            lengths.append(message_count)
        
        if not lengths:
            print("No conversation data available")
            return
        
        stats = {
            'average': statistics.mean(lengths),
            'median': statistics.median(lengths),
            'shortest': min(lengths),
            'longest': max(lengths),
            'total_messages': sum(lengths)
        }
        
        print("\n📏 Conversation Length Analysis:")
        print(f"  Average length: {stats['average']:.1f} messages")
        print(f"  Median length: {stats['median']} messages")
        print(f"  Shortest: {stats['shortest']} messages")
        print(f"  Longest: {stats['longest']} messages")
        print(f"  Total messages: {stats['total_messages']:,}")
        
        # Length distribution
        print("\n📊 Length Distribution:")
        ranges = [(0, 5), (6, 10), (11, 20), (21, 50), (51, float('inf'))]
        for min_len, max_len in ranges:
            count = sum(1 for l in lengths if min_len <= l <= max_len)
            percentage = (count / len(lengths)) * 100 if lengths else 0
            label = f"{min_len}-{max_len}" if max_len != float('inf') else f"{min_len}+"
            bar = '█' * int(percentage / 5)
            print(f"  {label:6} msgs: {bar} {percentage:.1f}%")
        
        return stats
    
    def analyze_active_times(self):
        """Find most active times for conversations"""
        
        hour_counter = Counter()
        day_counter = Counter()
        
        for conv in self.conversations:
            # Try to get timestamp
            timestamp_str = conv.get('saved_at') or conv.get('timestamp') or conv.get('date')
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    hour_counter[timestamp.hour] += 1
                    day_counter[timestamp.strftime('%A')] += 1
                except:
                    continue
        
        print("\n🕐 Most Active Times:")
        
        if hour_counter:
            # Find peak hours
            peak_hours = hour_counter.most_common(3)
            print("  Peak hours:")
            for hour, count in peak_hours:
                time_str = f"{hour:02d}:00-{(hour+1)%24:02d}:00"
                print(f"    {time_str}: {count} conversations")
        
        if day_counter:
            # Find busiest days
            print("\n  Activity by day:")
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for day in days_order:
                if day in day_counter:
                    count = day_counter[day]
                    bar = '█' * min(count * 2, 20)
                    print(f"    {day:10} {bar} ({count})")
        
        return hour_counter, day_counter
    
    def analyze_trends(self, days=30):
        """Analyze conversation trends over time"""
        
        cutoff = datetime.now() - timedelta(days=days)
        daily_counts = defaultdict(int)
        
        for conv in self.conversations:
            timestamp_str = conv.get('saved_at') or conv.get('timestamp') or conv.get('date')
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    if timestamp > cutoff:
                        date_key = timestamp.strftime('%Y-%m-%d')
                        daily_counts[date_key] += 1
                except:
                    continue
        
        if daily_counts:
            print(f"\n📈 Trends (Last {days} days):")
            
            # Calculate average
            avg_daily = sum(daily_counts.values()) / len(daily_counts)
            print(f"  Average conversations per day: {avg_daily:.1f}")
            
            # Show recent activity
            recent_dates = sorted(daily_counts.keys())[-7:]
            print("\n  Last 7 days:")
            for date in recent_dates:
                count = daily_counts[date]
                bar = '█' * min(count * 3, 20)
                print(f"    {date}: {bar} ({count})")
            
            # Trend direction
            if len(recent_dates) >= 2:
                first_half = recent_dates[:len(recent_dates)//2]
                second_half = recent_dates[len(recent_dates)//2:]
                
                first_avg = sum(daily_counts[d] for d in first_half) / len(first_half)
                second_avg = sum(daily_counts[d] for d in second_half) / len(second_half)
                
                if second_avg > first_avg * 1.2:
                    trend = "📈 Increasing"
                elif second_avg < first_avg * 0.8:
                    trend = "📉 Decreasing"
                else:
                    trend = "➡️ Stable"
                
                print(f"\n  Trend: {trend}")
        
        return daily_counts
    
    def generate_full_report(self):
        """Generate a comprehensive analytics report"""
        
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE CONVERSATION ANALYTICS")
        print("=" * 60)
        
        # Run all analyses
        self.analyze_common_topics()
        self.analyze_conversation_lengths()
        self.analyze_active_times()
        self.analyze_trends()
        
        print("\n" + "=" * 60)
        print("💡 Insights Complete!")
        
        # Save report to file
        report_file = f"analytics_report_{datetime.now().strftime('%Y%m%d')}.txt"
        print(f"📄 Report saved to {report_file}")

# Demo usage
if __name__ == "__main__":
    # Create sample data for demo
    sample_dir = Path("sample_analytics")
    sample_dir.mkdir(exist_ok=True)
    
    # Generate varied sample conversations
    sample_topics = ["python", "data", "machine learning", "code", "debug", "function"]
    
    for i in range(20):
        timestamp = datetime.now() - timedelta(days=i//2, hours=i)
        length = 5 + (i % 10)
        
        messages = []
        for j in range(length):
            if j % 2 == 0:
                content = f"Question about {sample_topics[i % len(sample_topics)]}"
                messages.append({"role": "user", "content": content})
            else:
                messages.append({"role": "assistant", "content": "Here's the answer..."})
        
        data = {
            "saved_at": timestamp.isoformat(),
            "message_count": len(messages),
            "messages": messages
        }
        
        with open(sample_dir / f"conv_{i:03d}.json", 'w') as f:
            json.dump(data, f)
    
    # Run analytics
    analytics = HistoryAnalytics(storage_dir=sample_dir)
    analytics.generate_full_report()
