# From: AI Agents Book - Chapter 13, Section 13.7
# File: retention_policy.py

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta
import sqlite3
import json


class RetentionPolicy:
    """Manage conversation data retention and GDPR compliance.
    
    This class creates its own table schema with timestamps for proper
    retention management. The default LangChain SQLChatMessageHistory
    doesn't include timestamps, so we manage our own schema here.
    """
    
    def __init__(self, db_path="retention_demo.db", retention_days=30):
        self.db_path = db_path
        self.retention_days = retention_days
        self._init_db()
    
    def _init_db(self):
        """Initialize database with timestamp-enabled schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table with timestamp column
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS message_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index for efficient cleanup queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON message_store(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_id 
            ON message_store(session_id)
        """)
        
        conn.commit()
        conn.close()
    
    def add_message(self, session_id: str, message_type: str, content: str):
        """Add a message with automatic timestamp."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO message_store (session_id, message_type, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (session_id, message_type, content, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def cleanup_old_conversations(self):
        """Delete conversations older than retention period."""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete old messages
        cursor.execute("""
            DELETE FROM message_store 
            WHERE timestamp < ?
        """, (cutoff_date,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def get_user_data(self, session_id: str):
        """Retrieve all data for a specific user (GDPR data export)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, session_id, message_type, content, timestamp 
            FROM message_store 
            WHERE session_id = ?
            ORDER BY timestamp
        """, (session_id,))
        
        columns = ['id', 'session_id', 'message_type', 'content', 'timestamp']
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return data
    
    def export_user_data_json(self, session_id: str) -> str:
        """Export user data as JSON (GDPR compliance)."""
        data = self.get_user_data(session_id)
        # Convert datetime objects to strings
        for record in data:
            if record['timestamp']:
                record['timestamp'] = str(record['timestamp'])
        return json.dumps(data, indent=2)
    
    def delete_user_data(self, session_id: str):
        """Delete all data for a specific user (GDPR right to erasure)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM message_store 
            WHERE session_id = ?
        """, (session_id,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def get_stats(self):
        """Get database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM message_store")
        total_messages = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM message_store")
        total_sessions = cursor.fetchone()[0]
        
        cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM message_store")
        date_range = cursor.fetchone()
        
        conn.close()
        
        return {
            "total_messages": total_messages,
            "total_sessions": total_sessions,
            "oldest_message": date_range[0],
            "newest_message": date_range[1]
        }


# Usage
if __name__ == "__main__":
    policy = RetentionPolicy(db_path="retention_demo.db", retention_days=30)
    
    # Add some sample messages
    print("Adding sample messages...")
    policy.add_message("user_123", "human", "Hello, I need help with my account")
    policy.add_message("user_123", "ai", "I'd be happy to help! What do you need?")
    policy.add_message("user_456", "human", "What's the weather like?")
    policy.add_message("user_456", "ai", "I don't have access to weather data.")
    
    # Show stats
    stats = policy.get_stats()
    print(f"\nDatabase stats: {stats}")
    
    # Export user data (GDPR)
    print(f"\nUser data for user_123:")
    print(policy.export_user_data_json("user_123"))
    
    # Run cleanup (in production, use a scheduled job)
    deleted = policy.cleanup_old_conversations()
    print(f"\nCleaned up {deleted} old messages (older than 30 days)")
    
    # Handle user deletion request (GDPR right to erasure)
    deleted_user = policy.delete_user_data("user_456")
    print(f"Deleted {deleted_user} messages for user_456")
    
    # Show final stats
    stats = policy.get_stats()
    print(f"\nFinal stats: {stats}")