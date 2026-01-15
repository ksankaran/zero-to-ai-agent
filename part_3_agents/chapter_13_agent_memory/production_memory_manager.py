# From: AI Agents Book - Chapter 13, Section 13.7
# File: production_memory_manager.py

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta
import sqlite3
import json
from langchain_core.messages import HumanMessage, AIMessage

# Import from other files in this section
from pii_filter import PIIFilter
from memory_monitoring import MemoryMonitor


class ProductionMemoryManager:
    """Complete production-ready memory manager.
    
    Combines:
    - PII filtering
    - Retention policies with timestamps
    - Monitoring
    - GDPR compliance (export/delete)
    
    Note: This uses a custom schema with timestamps rather than
    the default SQLChatMessageHistory which lacks timestamp support.
    """
    
    def __init__(self, db_path="prod_memory.db", retention_days=30):
        self.db_path = db_path
        self.retention_days = retention_days
        self.pii_filter = PIIFilter()
        self.monitor = MemoryMonitor()
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
        
        # Create indexes for efficient queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session_id 
            ON message_store(session_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON message_store(timestamp)
        """)
        
        conn.commit()
        conn.close()
    
    def get_session_history(self, session_id: str):
        """Get message history for a session."""
        self.monitor.log_access(session_id, is_cache_hit=False)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT message_type, content FROM message_store
            WHERE session_id = ?
            ORDER BY timestamp
        """, (session_id,))
        
        messages = []
        for msg_type, content in cursor.fetchall():
            if msg_type == "human":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(AIMessage(content=content))
        
        conn.close()
        return messages
    
    def add_user_message(self, session_id: str, message: str):
        """Add message with PII filtering."""
        # Filter PII before storing
        filtered_message = self.pii_filter.filter_message(message)
        
        if filtered_message != message:
            print(f"[INFO] PII detected and filtered for session {session_id}")
        
        self._store_message(session_id, "human", filtered_message)
        self.monitor.log_storage_operation()
    
    def add_ai_message(self, session_id: str, message: str):
        """Add AI response to history."""
        self._store_message(session_id, "ai", message)
        self.monitor.log_storage_operation()
    
    def _store_message(self, session_id: str, message_type: str, content: str):
        """Store a message with timestamp."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO message_store (session_id, message_type, content, timestamp)
            VALUES (?, ?, ?, ?)
        """, (session_id, message_type, content, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def run_maintenance(self):
        """Run periodic maintenance tasks."""
        # Clean old data
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        deleted = self._cleanup_old_data(cutoff)
        
        # Get metrics
        report = self.monitor.get_report()
        
        return {
            "deleted_messages": deleted,
            "metrics": report,
            "timestamp": datetime.now().isoformat()
        }
    
    def _cleanup_old_data(self, cutoff_date):
        """Delete messages older than cutoff date."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM message_store WHERE timestamp < ?", 
                (cutoff_date,)
            )
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            return deleted
        except Exception as e:
            self.monitor.log_error()
            print(f"[ERROR] Cleanup failed: {e}")
            return 0
    
    def export_user_data(self, session_id: str):
        """Export all user data (GDPR compliance)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT message_type, content, timestamp FROM message_store
            WHERE session_id = ?
            ORDER BY timestamp
        """, (session_id,))
        
        messages = [
            {"type": row[0], "content": row[1], "timestamp": str(row[2])}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            "session_id": session_id,
            "messages": messages,
            "export_date": datetime.now().isoformat()
        }
    
    def delete_user_data(self, session_id: str):
        """Delete all user data (GDPR right to erasure)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM message_store WHERE session_id = ?", 
                (session_id,)
            )
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            return deleted
        except Exception as e:
            self.monitor.log_error()
            print(f"[ERROR] Delete failed: {e}")
            return 0
    
    def get_metrics(self):
        """Get current system metrics."""
        return self.monitor.get_report()
    
    def get_stats(self):
        """Get database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM message_store")
        total_messages = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM message_store")
        total_sessions = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_messages": total_messages,
            "total_sessions": total_sessions
        }


# Usage
if __name__ == "__main__":
    manager = ProductionMemoryManager(retention_days=30)
    
    # Normal operation - PII is filtered
    print("Adding messages with PII filtering...")
    manager.add_user_message(
        "user_123", 
        "My email is sensitive@example.com and I need help"
    )
    manager.add_ai_message(
        "user_123",
        "I'd be happy to help! What do you need?"
    )
    
    # Add another user
    manager.add_user_message("user_456", "Hello there!")
    manager.add_ai_message("user_456", "Hi! How can I assist you?")
    
    # Check stats
    print("\nDatabase stats:")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Check metrics
    print("\nSystem metrics:")
    metrics = manager.get_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Periodic maintenance (run daily via cron)
    report = manager.run_maintenance()
    print(f"\nMaintenance: deleted {report['deleted_messages']} old messages")
    
    # Handle GDPR requests
    print("\n--- GDPR Export ---")
    user_data = manager.export_user_data("user_123")
    print(f"Exported {len(user_data['messages'])} messages for user_123")
    print(json.dumps(user_data, indent=2))
    
    print("\n--- GDPR Delete ---")
    deleted = manager.delete_user_data("user_456")
    print(f"Deleted {deleted} messages for user_456")
    
    # Final stats
    print("\nFinal stats:")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")