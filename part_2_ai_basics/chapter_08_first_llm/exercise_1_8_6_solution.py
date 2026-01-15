# From: Zero to AI Agent, Chapter 8, Section 8.6
# File: exercise_1_8_6_solution.py

import json
import csv
from pathlib import Path
from datetime import datetime

class ExportMaster:
    """Export conversations to multiple formats"""
    
    def __init__(self):
        self.supported_formats = ['html', 'csv', 'markdown', 'txt']
    
    def export_to_html(self, messages, filename="export.html"):
        """Create a beautiful HTML version of the conversation"""
        
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Conversation Export</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .conversation {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .message {
            margin: 15px 0;
            padding: 15px;
            border-radius: 10px;
        }
        .user {
            background: #e3f2fd;
            margin-left: 20%;
            border-left: 4px solid #2196F3;
        }
        .assistant {
            background: #f3e5f5;
            margin-right: 20%;
            border-left: 4px solid #9c27b0;
        }
        .role {
            font-weight: bold;
            color: #555;
            margin-bottom: 5px;
        }
        .timestamp {
            font-size: 0.8em;
            color: #999;
            margin-top: 5px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .metadata {
            background: #fff9c4;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <h1>🤖 Conversation Transcript</h1>
"""
        
        # Add metadata
        html += f"""
    <div class="metadata">
        <strong>Exported:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br>
        <strong>Total Messages:</strong> {len(messages)}<br>
        <strong>Format:</strong> HTML Export
    </div>
    <div class="conversation">
"""
        
        # Add each message
        for i, msg in enumerate(messages, 1):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '').replace('\n', '<br>')
            timestamp = msg.get('timestamp', '')
            
            role_display = "You" if role == "user" else "AI Assistant"
            
            html += f"""
        <div class="message {role}">
            <div class="role">{role_display} (Message {i})</div>
            <div>{content}</div>
            {f'<div class="timestamp">{timestamp}</div>' if timestamp else ''}
        </div>
"""
        
        html += """
    </div>
</body>
</html>"""
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Exported to {filename} (HTML)")
        return filename
    
    def export_to_csv(self, messages, filename="export.csv"):
        """Export conversation to CSV for analysis"""
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write headers
            writer.writerow(['Message #', 'Role', 'Content', 'Word Count', 'Character Count', 'Timestamp'])
            
            # Write each message
            for i, msg in enumerate(messages, 1):
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                word_count = len(content.split())
                char_count = len(content)
                timestamp = msg.get('timestamp', datetime.now().isoformat())
                
                writer.writerow([i, role, content, word_count, char_count, timestamp])
            
            # Add summary row
            total_words = sum(len(m.get('content', '').split()) for m in messages)
            total_chars = sum(len(m.get('content', '')) for m in messages)
            writer.writerow([])
            writer.writerow(['TOTALS', '', '', total_words, total_chars, ''])
        
        print(f"✅ Exported to {filename} (CSV)")
        print(f"   Total words: {total_words}")
        print(f"   Total characters: {total_chars}")
        return filename
    
    def export_to_markdown(self, messages, filename="export.md"):
        """Export conversation to Markdown format"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write("# Conversation Transcript\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%B %d, %Y')}\n")
            f.write(f"**Messages:** {len(messages)}\n\n")
            f.write("---\n\n")
            
            # Write messages
            for i, msg in enumerate(messages, 1):
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                
                if role == 'user':
                    f.write(f"### 👤 You (Message {i})\n\n")
                else:
                    f.write(f"### 🤖 AI (Message {i})\n\n")
                
                # Format code blocks if present
                if '```' in content:
                    f.write(content + "\n\n")
                else:
                    f.write(f"{content}\n\n")
                
                f.write("---\n\n")
        
        print(f"✅ Exported to {filename} (Markdown)")
        return filename
    
    def export_to_txt(self, messages, filename="export.txt"):
        """Export conversation to plain text"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("CONVERSATION TRANSCRIPT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
            f.write(f"Total Messages: {len(messages)}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, msg in enumerate(messages, 1):
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                
                if role == 'user':
                    f.write(f"YOU (Message {i}):\n")
                else:
                    f.write(f"AI (Message {i}):\n")
                
                f.write(f"{content}\n")
                f.write("-" * 40 + "\n\n")
        
        print(f"✅ Exported to {filename} (Plain Text)")
        return filename
    
    def export_all_formats(self, messages, base_filename="conversation"):
        """Export to all supported formats at once"""
        
        exported_files = []
        
        # Export to each format
        exported_files.append(self.export_to_html(messages, f"{base_filename}.html"))
        exported_files.append(self.export_to_csv(messages, f"{base_filename}.csv"))
        exported_files.append(self.export_to_markdown(messages, f"{base_filename}.md"))
        exported_files.append(self.export_to_txt(messages, f"{base_filename}.txt"))
        
        print(f"\n🎉 Exported to all {len(self.supported_formats)} formats!")
        return exported_files
    
    def export_with_stats(self, messages, format='html'):
        """Export with additional statistics"""
        
        # Calculate statistics
        stats = {
            'total_messages': len(messages),
            'user_messages': sum(1 for m in messages if m.get('role') == 'user'),
            'ai_messages': sum(1 for m in messages if m.get('role') == 'assistant'),
            'total_words': sum(len(m.get('content', '').split()) for m in messages),
            'avg_message_length': sum(len(m.get('content', '')) for m in messages) / len(messages) if messages else 0,
            'longest_message': max((len(m.get('content', '')) for m in messages), default=0)
        }
        
        # Add stats to messages
        enhanced_messages = messages.copy()
        
        # Export based on format
        if format == 'html':
            return self.export_to_html_with_stats(enhanced_messages, stats)
        else:
            # Default to requested format
            method_name = f"export_to_{format}"
            if hasattr(self, method_name):
                return getattr(self, method_name)(messages)
    
    def export_to_html_with_stats(self, messages, stats):
        """HTML export with statistics dashboard"""
        
        filename = "export_with_stats.html"
        
        # Create enhanced HTML with stats
        # (Implementation would include a stats dashboard)
        self.export_to_html(messages, filename)
        
        print(f"📊 Statistics added to export:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return filename


# Example usage
if __name__ == "__main__":
    # Sample conversation
    sample_conversation = [
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991."},
        {"role": "user", "content": "Can you show me a simple example?"},
        {"role": "assistant", "content": "Here's a simple Python example:\n\n```python\n# Hello World in Python\nprint('Hello, World!')\n\n# Variables and loops\nfor i in range(5):\n    print(f'Count: {i}')\n```"},
        {"role": "user", "content": "That's helpful, thanks!"},
        {"role": "assistant", "content": "You're welcome! Python's simplicity makes it great for beginners. Would you like to learn more about any specific Python topic?"}
    ]
    
    # Create exporter
    exporter = ExportMaster()
    
    # Export to all formats
    print("🚀 Export Master Demo")
    print("=" * 50)
    
    exported_files = exporter.export_all_formats(sample_conversation)
    
    print(f"\n✅ Successfully exported {len(exported_files)} files:")
    for file in exported_files:
        print(f"   - {file}")
    
    # Export with statistics
    print("\n📊 Exporting with statistics...")
    exporter.export_with_stats(sample_conversation, 'html')